# magic_base/data_access/repository/sqlalchemy_repository.py
"""
SQLAlchemy 仓储实现（可选）

提供基于 SQLAlchemy 的通用 CRUD 实现，业务模块可直接继承使用。

设计原则：
- 简单 CRUD：使用 ORM，安全便捷
- 复杂查询：使用参数化原生 SQL + 白名单验证
"""

from typing import Dict, List, Optional, TypeVar, Generic, Type, Any, Callable, Generator, Set
from contextlib import contextmanager
from sqlalchemy.orm import Session, Query
from sqlalchemy import text, inspect, desc, asc

from magic_base.data_access.repository.base_repository import BaseRepository

T = TypeVar('T')


class SQLAlchemyRepository(BaseRepository[T], Generic[T]):
    """
    SQLAlchemy 仓储实现
    
    提供 ORM 和参数化 SQL 两种查询方式。
    """
    
    def __init__(
        self,
        model_class: Type[T],
        session_factory: Callable[[], Session],
        soft_field: str = 'is_active',
        allowed_columns: Optional[List[str]] = None
    ):
        """
        初始化仓储
        
        Args:
            model_class: SQLAlchemy 模型类
            session_factory: 返回数据库 session 的可调用对象
            soft_field: 软删除字段名（默认 is_active）
            allowed_columns: 允许查询的列名白名单（None 表示从模型自动获取）
        """
        self.model_class = model_class
        self.session_factory = session_factory
        self.soft_field = soft_field
        
        # 设置列名白名单
        if allowed_columns is not None:
            self._allowed_columns: Set[str] = set(allowed_columns)
        else:
            # 从模型自动获取所有列名
            self._allowed_columns = {c.name for c in inspect(model_class).mapper.columns}
    
    @contextmanager
    def _get_session(self) -> Generator[Session, None, None]:
        """获取数据库 session（上下文管理器）"""
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def _validate_column(self, column_name: str) -> None:
        """验证列名是否在白名单中"""
        if column_name not in self._allowed_columns:
            raise ValueError(f"Invalid column name: {column_name}")
    
    def _apply_filters(self, query: Query, filters: Optional[Dict]) -> Query:
        """安全应用过滤条件（ORM 方式）"""
        if not filters:
            return query
        
        for key, value in filters.items():
            if value is not None:
                self._validate_column(key)
                query = query.filter(getattr(self.model_class, key) == value)
        return query
    
    def _apply_order_by(self, query: Query, order_by: Optional[str]) -> Query:
        """安全应用排序（ORM 方式）"""
        if not order_by:
            return query
        
        parts = order_by.strip().split()
        field = parts[0]
        direction = parts[1].upper() if len(parts) > 1 else "ASC"
        
        self._validate_column(field)
        column = getattr(self.model_class, field)
        
        if direction == "DESC":
            return query.order_by(desc(column))
        else:
            return query.order_by(asc(column))
    
    def _model_to_dict(self, obj: T) -> Dict:
        """将 ORM 对象转换为 Dict"""
        return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}
    
    def _models_to_dicts(self, objs: List[T]) -> List[Dict]:
        """将 ORM 对象列表转换为 Dict 列表"""
        return [self._model_to_dict(obj) for obj in objs]
    
    # ==================== 通用参数化查询方法 ====================
    
    def execute_query(self, sql: str, params: Optional[Dict] = None) -> List[Dict]:
        """
        执行参数化查询（安全）
        
        Args:
            sql: 参数化 SQL 语句，使用 :name 格式
            params: 参数字典
        
        Returns:
            查询结果列表（Dict 格式）
        """
        with self._get_session() as session:
            result = session.execute(text(sql), params or {})
            return [dict(row._mapping) for row in result]
    
    def execute_query_one(self, sql: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """执行参数化查询，返回单条结果"""
        results = self.execute_query(sql, params)
        return results[0] if results else None
    
    # ==================== 查询方法（ORM 方式 - 简单查询） ====================
    
    def get_by_id(self, id: int) -> Optional[Dict]:
        """根据 ID 获取单条记录（ORM）"""
        with self._get_session() as session:
            obj = session.query(self.model_class).filter_by(id=id).first()
            return self._model_to_dict(obj) if obj else None
    
    def find_one(self, conditions: Dict[str, Any]) -> Optional[Dict]:
        """根据条件获取单条记录（ORM）"""
        results = self.find(conditions, limit=1)
        return results[0] if results else None
    
    def find(self, conditions: Optional[Dict] = None,
             order_by: Optional[str] = None,
             limit: Optional[int] = None,
             offset: Optional[int] = None) -> List[Dict]:
        """根据条件查询记录列表（ORM）"""
        with self._get_session() as session:
            query = session.query(self.model_class)
            query = self._apply_filters(query, conditions)
            query = self._apply_order_by(query, order_by)
            
            if limit:
                query = query.limit(limit)
            if offset:
                query = query.offset(offset)
            
            results = query.all()
            return self._models_to_dicts(results)
    
    def get_all(self, filters: Optional[Dict] = None,
                order_by: Optional[str] = None,
                limit: Optional[int] = None) -> List[Dict]:
        """获取所有记录（简化版）"""
        return self.find(filters, order_by, limit)
    
    def exists(self, **conditions) -> bool:
        """检查记录是否存在"""
        result = self.find_one(conditions)
        return result is not None
    
    def count(self, filters: Optional[Dict] = None) -> int:
        """统计记录数量（ORM）"""
        with self._get_session() as session:
            query = session.query(self.model_class)
            query = self._apply_filters(query, filters)
            return query.count()
    
    def paginate(self, page: int = 1, per_page: int = 20,
                 filters: Optional[Dict] = None,
                 order_by: str = "id DESC") -> Dict:
        """分页查询（ORM）"""
        offset = (page - 1) * per_page
        
        items = self.find(
            conditions=filters,
            order_by=order_by,
            limit=per_page,
            offset=offset
        )
        
        total = self.count(filters)
        
        return {
            'items': items,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page if total else 0,
            'has_next': page * per_page < total,
            'has_prev': page > 1
        }
    
    # ==================== 创建方法（ORM） ====================
    
    def create(self, **kwargs) -> T:
        """创建记录（从参数）"""
        with self._get_session() as session:
            instance = self.model_class(**kwargs)
            session.add(instance)
            session.flush()
            session.refresh(instance)
            return instance
    
    def create_from_model(self, model: T) -> T:
        """创建记录（从模型对象）"""
        with self._get_session() as session:
            session.add(model)
            session.flush()
            session.refresh(model)
            return model
    
    def batch_create(self, models: List[T]) -> List[T]:
        """批量创建"""
        with self._get_session() as session:
            session.add_all(models)
            session.flush()
            for model in models:
                session.refresh(model)
            return models
    
    # ==================== 更新方法（ORM） ====================
    
    def update(self, id: int, **kwargs) -> bool:
        """更新记录（从参数）"""
        with self._get_session() as session:
            instance = session.query(self.model_class).get(id)
            if not instance:
                return False
            
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            
            session.flush()
            return True
    
    def update_from_model(self, model: T) -> bool:
        """更新记录（从模型对象）"""
        with self._get_session() as session:
            session.merge(model)
            session.flush()
            return True
    
    def batch_update(self, updates: Dict[int, Dict[str, Any]]) -> int:
        """批量更新"""
        updated_count = 0
        with self._get_session() as session:
            for record_id, fields in updates.items():
                instance = session.query(self.model_class).get(record_id)
                if instance:
                    for key, value in fields.items():
                        if hasattr(instance, key):
                            setattr(instance, key, value)
                    updated_count += 1
            session.flush()
        return updated_count
    
    # ==================== 删除方法（ORM） ====================
    
    def delete(self, id: int, soft: bool = True) -> bool:
        """删除单条记录"""
        with self._get_session() as session:
            instance = session.query(self.model_class).get(id)
            if not instance:
                return False
            
            if soft:
                if hasattr(instance, self.soft_field):
                    setattr(instance, self.soft_field, False)
                else:
                    raise ValueError(f"模型 {self.model_class.__name__} 缺少 {self.soft_field} 字段")
            else:
                session.delete(instance)
            
            session.flush()
            return True
    
    def batch_delete(self, ids: List[int], soft: bool = True) -> int:
        """批量删除"""
        deleted_count = 0
        for id in ids:
            if self.delete(id, soft):
                deleted_count += 1
        return deleted_count
    
    # ==================== 辅助方法 ====================
    
    def get_orm_instance(self, id: int) -> Optional[T]:
        """获取 ORM 实例"""
        with self._get_session() as session:
            return session.query(self.model_class).get(id)
    
    def get_allowed_columns(self) -> List[str]:
        """获取允许查询的列名列表"""
        return sorted(self._allowed_columns)