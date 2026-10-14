# magic_base/data_access/service/base_service.py
"""
Service 基类 - 定义业务层接口
"""

from typing import Dict, List, Optional, Generic, TypeVar
from abc import ABC

from magic_base.data_access.repository.base_repository import BaseRepository


T = TypeVar('T')


class BaseService(ABC, Generic[T]):
    """
    Service 抽象基类

    提供对 Repository 的基础 CRUD 操作透传。
    子类只需指定对应的 Repository 类型。

    使用方式:
        class ProjectService(BaseService[Project]):
            def __init__(self):
                super().__init__(ProjectRepository())

    设计理念:
        - 基础 CRUD 方法由基类统一实现，避免重复代码
        - 子类可以添加业务方法
        - 保持与 Repository 方法命名一致
        - 提供 *_by_key 系列，支持按业务 key 操作（内部转主键）
    """

    def __init__(self, repository: BaseRepository[T]):
        """
        初始化 Service

        参数:
            repository: 对应的 Repository 实例
        """
        self._repo = repository

    # ==================== Create 操作 ====================

    def create(self, **kwargs) -> Dict:
        """创建记录"""
        return self._repo.create(**kwargs)

    def create_from_model(self, model: T) -> T:
        """从 ORM 实例创建记录"""
        return self._repo.create_from_model(model)

    # ==================== Read 操作 ====================

    def get_by_id(self, record_id: int) -> Optional[Dict]:
        """根据 ID 获取记录"""
        return self._repo.get_by_id(record_id)

    def find(self, conditions: Optional[Dict] = None,
             order_by: Optional[str] = None,
             limit: Optional[int] = None,
             offset: int = 0) -> List[Dict]:
        """条件查询"""
        return self._repo.find(conditions or {}, order_by, limit, offset)

    def find_one(self, conditions: Dict) -> Optional[Dict]:
        """条件查询单条"""
        return self._repo.find_one(conditions)

    def find_all(self, limit: Optional[int] = None, offset: int = 0) -> List[Dict]:
        """查询所有（支持 offset）"""
        return self._repo.find({}, limit=limit, offset=offset)

    def count(self, conditions: Optional[Dict] = None) -> int:
        """统计数量"""
        return self._repo.count(conditions or {})

    def exists(self, **kwargs) -> bool:
        """检查是否存在"""
        return self._repo.exists(**kwargs)

    def paginate(self, page: int = 1, per_page: int = 20,
                 conditions: Optional[Dict] = None,
                 order_by: str = "id DESC") -> Dict:
        """分页查询"""
        return self._repo.paginate(page, per_page, conditions or {}, order_by)

    # ==================== Read 操作（按业务 key） ====================

    def get_by_key(self, key_field: str, key_value) -> Optional[Dict]:
        """按业务 key 查询"""
        return self._repo.find_one({key_field: key_value})

    def exists_by_key(self, key_field: str, key_value) -> bool:
        """按业务 key 检查存在"""
        return self._repo.find_one({key_field: key_value}) is not None

    # ==================== Update 操作 ====================

    def update(self, record_id: int, **kwargs) -> bool:
        """更新记录"""
        return self._repo.update(record_id, **kwargs)

    def update_by_key(self, key_field: str, key_value, **kwargs) -> bool:
        """按业务 key 更新"""
        record = self._repo.find_one({key_field: key_value})
        if not record:
            return False
        return self._repo.update(record['id'], **kwargs)

    def batch_create(self, models: List[Dict[str, str]]) -> int:
        """批量创建"""
        return self._repo.batch_create_from_dict(models)

    def batch_update(self, updates: Dict[int, Dict]) -> int:
        """批量更新"""
        return self._repo.batch_update(updates)

    # ==================== Delete 操作 ====================

    def delete(self, record_id: int, soft: bool = True) -> bool:
        """删除记录"""
        return self._repo.delete(record_id, soft=soft)

    def delete_by_key(self, key_field: str, key_value, soft: bool = True) -> bool:
        """按业务 key 删除"""
        record = self._repo.find_one({key_field: key_value})
        if not record:
            return False
        return self._repo.delete(record['id'], soft=soft)

    # ==================== ORM 操作 ====================

    def get_orm_instance(self, record_id: int) -> Optional[T]:
        """获取 ORM 实例"""
        return self._repo.get_orm_instance(record_id)


class MagicBaseService(BaseService[T]):
    """
    Magic 系列基础 Service 适配类

    继承自 BaseService，为 Magic 系列项目提供统一的 Service 基类。

    设计目的:
        为 Magic 生态系统中的各个项目提供一致的 Service 接口，
        便于业务逻辑的复用和统一管理。

    使用方式:
        from magic_base.data_access.service import MagicBaseService

        class UserService(MagicBaseService[User]):
            def __init__(self):
                super().__init__(UserRepository())

            def validate(self, data):
                ...

            def create(self, data):
                self.validate(data)
                return super().create(**data)

    注意:
        本类通过子类继承使用。子类需指定泛型类型 T 并注入 Repository。
        本类不含抽象方法，可直接实例化（但通常不这么做）。
    """
    pass