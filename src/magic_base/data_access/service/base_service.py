# magic_base/data_access/service/base_service.py
"""
Service 基类 - 定义业务层接口
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Dict, Any
from .base_service_cud_mixin import CUDServiceMixin
from .base_service_query_mixin import QueryServiceMixin


T = TypeVar('T')  # 业务对象类型


class BaseService(CUDServiceMixin[T], QueryServiceMixin[T]):
    """
    Service 基类（抽象基类）
    
    组合 CUD 和 Query 两个 Mixin，提供完整的业务服务能力。
    
    设计理念:
        - 采用 Mixin 风格，与 Repository 层保持一致
        - CUD 操作：对应 CUDRepositoryMixin，处理写操作业务逻辑
        - Query 操作：对应 QueryRepositoryMixin，处理读操作业务逻辑
        - 职责分离，各司其职
    
    继承关系:
        BaseService
        ├── CUDServiceMixin (创建、更新、删除业务逻辑)
        │   └── ServiceCoreMixin (核心验证)
        └── QueryServiceMixin (查询业务逻辑)
            └── ServiceCoreMixin (核心验证)
    
    与 Repository 的对应关系:
        - CUDServiceMixin 内部通常注入 CUDRepositoryMixin
        - QueryServiceMixin 内部通常注入 QueryRepositoryMixin
        - BaseService 组合两者，提供完整功能
    
    使用方式:
        class UserService(BaseService[User]):
            def __init__(self):
                # 注入 Repository
                self.user_repo = UserRepository()
            
            # 实现 CUD 方法
            def create(self, data: Dict[str, Any]) -> Dict:
                self.validate(data)
                if self.user_repo.exists(email=data['email']):
                    raise ValueError("邮箱已被注册")
                user = self.user_repo.create(**data)
                return user.to_dict()
            
            def update(self, id: int, data: Dict[str, Any]) -> Dict:
                self.validate(data, is_update=True)
                if not self.user_repo.update(id, **data):
                    raise ValueError("用户不存在")
                return self.user_repo.get_by_id(id)
            
            def delete(self, id: int, soft: bool = True) -> bool:
                return self.user_repo.delete(id, soft=soft)
            
            # 实现 Query 方法
            def get_by_id(self, id: int) -> Optional[Dict]:
                # 权限检查
                if not self.has_permission(id):
                    return None
                return self.user_repo.get_by_id(id)
            
            def get_list(self, filters: Optional[Dict] = None,
                        order_by: Optional[str] = None,
                        limit: Optional[int] = None) -> List[Dict]:
                return self.user_repo.get_all(filters=filters, order_by=order_by, limit=limit)
            
            # 实现验证方法
            def validate(self, data: Dict[str, Any], is_update: bool = False) -> bool:
                if not data.get('email'):
                    raise ValueError("邮箱不能为空")
                return True
        
        # 使用 Service
        user_service = UserService()
        
        # 创建用户
        new_user = user_service.create({'name': 'Alice', 'email': 'alice@example.com'})
        
        # 查询用户
        user = user_service.get_by_id(new_user['id'])
        
        # 分页查询
        result = user_service.paginate(page=1, per_page=10)
    
    设计优势:
        - 职责分离：CUD 和 Query 各司其职
        - 灵活组合：可以根据需要只继承部分 Mixin（如只读 Service）
        - 易于测试：每个 Mixin 可以独立测试
        - 代码复用：不同的 Service 可以灵活组合不同的能力
        - 类型安全：完整的泛型支持
        - 与 Repository 层保持架构一致
    
    注意事项:
        1. 此类为抽象基类，不能直接实例化
        2. 子类必须实现所有抽象方法
        3. 建议在子类中注入对应的 Repository
        4. 业务逻辑应在 Service 层实现，Repository 层只负责数据访问
    """
    
    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Dict:
        """创建业务对象"""
        pass
    
    @abstractmethod
    def create_from_model(self, model: T) -> Dict:
        """从模型对象创建业务对象"""
        pass
    
    @abstractmethod
    def update(self, id: int, data: Dict[str, Any]) -> Dict:
        """更新业务对象"""
        pass
    
    @abstractmethod
    def update_from_model(self, model: T) -> Dict:
        """从模型对象更新业务对象"""
        pass
    
    @abstractmethod
    def delete(self, id: int, soft: bool = True) -> bool:
        """删除业务对象"""
        pass
    
    @abstractmethod
    def get_orm_instance(self, id: int) -> Optional[T]:
        """获取 ORM 实例"""
        pass
    
    @abstractmethod
    def batch_create(self, items: List[Dict[str, Any]]) -> List[Dict]:
        """批量创建业务对象"""
        pass
    
    @abstractmethod
    def batch_update(self, updates: Dict[int, Dict[str, Any]]) -> int:
        """批量更新业务对象"""
        pass
    
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Dict]:
        """根据 ID 获取业务对象"""
        pass
    
    @abstractmethod
    def get_list(self, filters: Optional[Dict] = None,
                 order_by: Optional[str] = None,
                 limit: Optional[int] = None) -> List[Dict]:
        """获取业务对象列表"""
        pass
    
    @abstractmethod
    def find(self, conditions: Optional[Dict[str, Any]] = None,
             order_by: Optional[str] = None,
             limit: Optional[int] = None,
             offset: Optional[int] = None) -> List[Dict]:
        """动态查询业务对象"""
        pass
    
    @abstractmethod
    def find_one(self, conditions: Dict[str, Any]) -> Optional[Dict]:
        """查询单个业务对象"""
        pass
    
    @abstractmethod
    def exists(self, **conditions) -> bool:
        """检查业务对象是否存在"""
        pass
    
    @abstractmethod
    def count(self, filters: Optional[Dict] = None) -> int:
        """统计业务对象数量"""
        pass
    
    @abstractmethod
    def paginate(self, page: int = 1, per_page: int = 20,
                 conditions: Optional[Dict[str, Any]] = None,
                 order_by: str = "id DESC") -> Dict[str, Any]:
        """分页查询业务对象"""
        pass
    
    @abstractmethod
    def validate(self, data: Dict[str, Any], is_update: bool = False) -> bool:
        """验证业务数据"""
        pass


class MagicBaseService(ABC, BaseService[T]):
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