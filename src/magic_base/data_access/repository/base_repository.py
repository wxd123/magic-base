# magicm_base/data_access/repository/base_repository.py

from abc import ABC
from typing import Dict, List, Optional, TypeVar, Generic, Type, Any, get_origin, get_args
from sqlalchemy.orm import Session
from sqlalchemy import inspect, text
from magic_base.data_access.manager.base_database_manager import MagicDatabaseManager, DatabaseManagerBase


T = TypeVar('T')


class BaseRepository(Generic[T]):
    """
    混合 Repository 基类（抽象基类，只能通过继承使用）
    
    - CUD (创建/更新/删除): 使用 ORM
    - R (查询): 使用原生 SQL
    
    使用方式：
        class UserRepository(BaseRepository[User]):
            pass
        
        repo = UserRepository(session)  # 或 UserRepository()
    """
    
    def __new__(cls, *args, **kwargs):
        """在子类实例化时自动提取泛型类型"""
        if cls is BaseRepository:
            raise TypeError(f"抽象基类 {cls.__name__} 不能直接实例化，请使用子类继承")
        
        instance = super().__new__(cls)
        
        # 自动从子类的泛型参数提取模型类
        instance._model_class = cls._extract_model_class()
        
        return instance
    
    def __init__(self, session: Optional[Session] = None):
        """
        Args:
            session: 数据库会话（可选，如果不提供则自动从 db_connection 获取）
        """
        if not hasattr(self, '_model_class') or self._model_class is None:
            raise RuntimeError(
                f"{self.__class__.__name__} 未正确初始化模型类。\n"
                f"请确保继承时指定泛型：class {self.__class__.__name__}(BaseRepository[UserModel]): pass"
            )
        
        # 设置 session
        if session is not None:
            self._session = session
        else:
            self._session = None  # 延迟初始化，使用时再获取
        
        # 获取表名
        self._table_name = self._get_table_name_from_model(self._model_class)
    
    @classmethod
    def _extract_model_class(cls) -> Type[T]:
        """从泛型参数提取模型类"""
        # 检查 __orig_bases__（Python 3.8+）
        if hasattr(cls, '__orig_bases__'):
            for base in cls.__orig_bases__:
                origin = get_origin(base)
                if origin is BaseRepository:
                    args = get_args(base)
                    if args:
                        return args[0]
        
        # 检查 __bases__（兼容处理）
        for base in cls.__bases__:
            if hasattr(base, '__origin__') and base.__origin__ is BaseRepository:
                args = getattr(base, '__args__', [])
                if args:
                    return args[0]
        
        raise TypeError(
            f"{cls.__name__} 必须指定泛型类型。\n"
            f"正确用法：class {cls.__name__}(BaseRepository[UserModel]): pass"
        )
    
    def _get_session(self) -> Session:
        """获取数据库会话（延迟初始化）"""
        if self._session is None:
            self._session = DatabaseManagerBase.session()
        return self._session
    
    @property
    def session(self) -> Session:
        """获取数据库会话"""
        return self._get_session()
    
    @property
    def model_class(self) -> Type[T]:
        """获取模型类"""
        return self._model_class
    
    @property
    def table_name(self) -> str:
        """获取表名"""
        return self._table_name
    
    def _get_table_name_from_model(self, model_class: Type[T]) -> str:
        """从模型类自动获取表名"""
        # 获取表名的多种方式
        if hasattr(model_class, '__tablename__'):
            return model_class.__tablename__
        
        if hasattr(model_class, '__table__') and model_class.__table__ is not None:
            return model_class.__table__.name
        
        # 降级方案：从类名转换
        import re
        class_name = model_class.__name__
        snake_name = re.sub('(?<!^)(?=[A-Z])', '_', class_name).lower()
        if not snake_name.endswith('s'):
            snake_name += 's'
        return snake_name
    
    # ==================== ORM 部分 (CUD) ====================
    
    def create(self, **kwargs) -> T:
        """创建记录（ORM）"""
        with self._get_session() as session:
            instance = self._model_class(**kwargs)
            session.add(instance)
            session.flush()
            session.refresh(instance)  # 刷新获取自增 ID
            return instance
    
    def create_from_model(self, model: T) -> T:
        """从模型对象创建（ORM）"""
        with self._get_session() as session:
            session.add(model)
            session.flush()
            session.refresh(model)
            return model
    
    def update(self, record_id: int, **kwargs) -> bool:
        """更新记录（ORM）"""
        with self._get_session() as session:
            instance = session.query(self._model_class).get(record_id)
            if not instance:
                return False
            
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            
            session.flush()
            return True
    
    def update_from_model(self, model: T) -> bool:
        """从模型对象更新（ORM）"""
        with self._get_session() as session:
            session.merge(model)
            session.flush()
            return True
    
    def delete(self, record_id: int, soft: bool = True, active_field: str = 'is_active') -> bool:
        """删除记录（ORM）"""
        with self._get_session() as session:
            instance = session.query(self._model_class).get(record_id)
            if not instance:
                return False
            
            if soft:
                if hasattr(instance, active_field):
                    setattr(instance, active_field, False)
                else:
                    raise ValueError(f"模型缺少 {active_field} 字段")
            else:
                session.delete(instance)
            
            session.flush()
            return True
    
    def batch_create(self, models: List[T]) -> List[T]:
        """批量创建（ORM）"""
        with self._get_session() as session:
            session.bulk_save_objects(models)
            session.flush()
            session.commit()
            return models
    
    def batch_update(self, updates: Dict[int, Dict[str, Any]]) -> int:
        """批量更新（ORM）"""
        updated = 0
        with self._get_session() as session:
            for record_id, fields in updates.items():
                instance = session.query(self._model_class).get(record_id)
                if instance:
                    for key, value in fields.items():
                        if hasattr(instance, key):
                            setattr(instance, key, value)
                    updated += 1
            session.flush()
        return updated
    
    def get_orm_instance(self, record_id: int) -> Optional[T]:
        """获取 ORM 实例"""
        with self._get_session() as session:
            return session.query(self._model_class).get(record_id)
    
    # ==================== SQL 部分 (R - 查询) ====================
    
    def fetch_one(self, sql: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict]:
        """查询单条记录"""
        with self._get_session() as session:
            result = session.execute(text(sql), params or {})
            row = result.first()
            if row:
                return dict(row._mapping)
            return None
    
    def fetch_all(self, sql: str, params: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """查询多条记录"""
        with self._get_session() as session:
            result = session.execute(text(sql), params or {})
            rows = result.fetchall()
            return [dict(row._mapping) for row in rows]
    
    def get_by_id(self, record_id: int) -> Optional[Dict]:
        """根据 ID 查询（SQL）"""
        return self.fetch_one(
            f"SELECT * FROM {self._table_name} WHERE id = :id",
            {'id': record_id}
        )
    
    def get_all(self, filters: Optional[Dict[str, Any]] = None,
                order_by: Optional[str] = None,
                limit: Optional[int] = None) -> List[Dict]:
        """查询所有记录（SQL）"""
        sql = f"SELECT * FROM {self._table_name} WHERE 1=1"
        params = {}
        
        if filters:
            for key, value in filters.items():
                if value is not None:
                    sql += f" AND {key} = :{key}"
                    params[key] = value
        
        if order_by:
            sql += f" ORDER BY {order_by}"
        if limit:
            sql += " LIMIT :limit"
            params['limit'] = limit
        
        return self.fetch_all(sql, params)
    
    def find(self, conditions: Optional[Dict[str, Any]] = None,
             order_by: Optional[str] = None,
             limit: Optional[int] = None,
             offset: Optional[int] = None) -> List[Dict]:
        """动态查询（SQL）"""
        where_parts = []
        params = {}
        
        if conditions:
            for key, value in conditions.items():
                if value is not None:
                    where_parts.append(f"{key} = :{key}")
                    params[key] = value
        
        where_clause = " AND ".join(where_parts) if where_parts else "1=1"
        sql = f"SELECT * FROM {self._table_name} WHERE {where_clause}"
        
        if order_by:
            sql += f" ORDER BY {order_by}"
        if limit:
            sql += " LIMIT :limit"
            params['limit'] = limit
        if offset:
            sql += " OFFSET :offset"
            params['offset'] = offset
        
        return self.fetch_all(sql, params)
    
    def find_one(self, conditions: Dict[str, Any]) -> Optional[Dict]:
        """查询单条记录（SQL）"""
        results = self.find(conditions, limit=1)
        return results[0] if results else None
    
    def exists(self, **conditions) -> bool:
        """检查是否存在（SQL）"""
        result = self.find_one(conditions)
        return result is not None
    
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """统计数量（SQL）"""
        sql = f"SELECT COUNT(*) as total FROM {self._table_name} WHERE 1=1"
        params = {}
        
        if filters:
            for key, value in filters.items():
                if value is not None:
                    sql += f" AND {key} = :{key}"
                    params[key] = value
        
        result = self.fetch_one(sql, params)
        return result['total'] if result else 0
    
    def paginate(self, page: int = 1, per_page: int = 20,
                 conditions: Optional[Dict[str, Any]] = None,
                 order_by: str = "id DESC") -> Dict[str, Any]:
        """分页查询（SQL）"""
        offset = (page - 1) * per_page
        
        items = self.find(
            conditions=conditions,
            order_by=order_by,
            limit=per_page,
            offset=offset
        )
        
        total = self.count(conditions)
        
        return {
            'items': items,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page if total else 0,
            'has_next': page * per_page < total,
            'has_prev': page > 1
        }

class MagicBaseRepository(ABC, BaseRepository[Generic[T]]):