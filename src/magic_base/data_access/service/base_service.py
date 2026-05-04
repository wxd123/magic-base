# magic_base/data_access/service/base_service.py
"""
Service 基类 - 定义业务层接口
"""


from typing import Dict, List, Optional, Generic, TypeVar, Type
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
    
    # ==================== Read 操作 ====================
    
    def get_by_id(self, record_id: int) -> Optional[Dict]:
        """根据ID获取记录"""
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
        """查询所有"""
        return self._repo.find_all(limit, offset)
    
    def count(self, conditions: Optional[Dict] = None) -> int:
        """统计数量"""
        return self._repo.count(conditions or {})
    
    def exists(self, **kwargs) -> bool:
        """检查是否存在"""
        return self._repo.exists(**kwargs)
    
    def paginate(self, page: int = 1, per_page: int = 20,
                 conditions: Optional[Dict] = None) -> Dict:
        """分页查询"""
        return self._repo.paginate(page, per_page, conditions or {})
    
    # ==================== Update 操作 ====================
    
    def update(self, record_id: int, **kwargs) -> bool:
        """更新记录"""
        return self._repo.update(record_id, **kwargs)
    
    def batch_update(self, updates: Dict[int, Dict]) -> int:
        """批量更新"""
        return self._repo.batch_update(updates)
    
    # ==================== Delete 操作 ====================
    
    def delete(self, record_id: int, soft: bool = True) -> bool:
        """删除记录"""
        return self._repo.delete(record_id, soft=soft)
    
    # ==================== ORM 操作 ====================
    
    def get_orm_instance(self, record_id: int) -> Optional[T]:
        """获取 ORM 实例"""
        return self._repo.get_orm_instance(record_id)

class MagicBaseService(BaseService[T]):
    """
    Magic 系列基础 Service 适配类
    
    继承自 ABC（抽象基类）和 BaseService，为 Magic 系列项目提供统一的 Service 基类。
    
    设计目的:
        为 Magic 生态系统中的各个项目提供一致的 Service 接口，
        便于业务逻辑的复用和统一管理。
    
    使用方式:
        from magic_base.data_access.service import MagicBaseService
        
        class UserService(MagicBaseService[User]):
            def __init__(self):
                self.user_repo = UserRepository()
            
            def get_by_id(self, id: int) -> Optional[Dict]:
                return self.user_repo.get_by_id(id)
            
            def create(self, data: Dict[str, Any]) -> Dict:
                self.validate(data)
                user = self.user_repo.create(**data)
                return user.to_dict()
            
            # ... 实现其他抽象方法
    
    注意:
        此类为抽象基类，通过 ABC 确保不能被直接实例化。
        必须通过子类继承并实现所有抽象方法。
    """
    pass