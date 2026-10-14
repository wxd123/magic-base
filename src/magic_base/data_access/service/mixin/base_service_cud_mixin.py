# magic_base/data_access/service/base_service.py
"""
Service 基类 - 定义业务层接口
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Dict, Any
from .base_service_core_mixin import ServiceCoreMixin


T = TypeVar('T')  # 业务对象类型


class CUDServiceMixin(ServiceCoreMixin[T]):
    """
    CUD 业务操作 Mixin (Create, Update, Delete)
    
    提供使用 ORM 方式的创建、更新、删除业务操作。
    继承自 ServiceCoreMixin，获得核心验证功能。
    
    设计理念:
        与 CUDRepositoryMixin 对应，定义业务层的写操作接口。
        Service 层负责业务流程编排，通常内部会调用 CUDRepositoryMixin 的方法。
    
    包含的功能:
        - 创建业务对象
        - 从模型对象创建
        - 更新业务对象
        - 从模型对象更新
        - 删除业务对象（支持软删除）
        - 获取 ORM 实例
        - 批量创建
        - 批量更新
    
    使用方式:
        class UserService(CUDServiceMixin[User]):
            def __init__(self, user_repo: UserRepository):
                self.user_repo = user_repo
            
            def create(self, data: Dict[str, Any]) -> Dict:
                # 业务逻辑
                self.validate(data)
                
                # 业务规则检查
                if self.user_repo.exists(email=data['email']):
                    raise ValueError("邮箱已被注册")
                
                # 调用 Repository
                user = self.user_repo.create(**data)
                return user.to_dict()
    """
    
    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Dict:
        """
        创建业务对象
        
        处理创建业务对象的完整流程，包括验证、转换和持久化。
        
        业务逻辑可包含:
        - 数据验证：调用 validate 方法验证输入数据
        - 业务规则检查：如唯一性约束、关联数据存在性等
        - 默认值设置：为未提供的字段设置默认值
        - 关联数据处理：创建主对象时同时创建关联对象
        - 日志记录：记录创建操作日志
        - 事件触发：触发创建后的事件（如发送通知）
        
        参数:
            data: 要创建的业务对象数据字典
        
        返回:
            Dict: 创建后的完整业务对象（通常包含自动生成的 ID）
        
        异常:
            ValueError: 数据验证失败或业务规则违反时抛出
        
        示例:
            user_data = {
                'name': 'Alice',
                'email': 'alice@example.com',
                'role': 'user'
            }
            new_user = user_service.create(user_data)
            print(f"创建成功，用户 ID: {new_user['id']}")
        """
        pass
    
    @abstractmethod
    def create_from_model(self, model: T) -> Dict:
        """
        从模型对象创建业务对象
        
        使用已有的模型实例创建记录，适用于模型已经部分填充的情况。
        
        业务逻辑可包含:
        - 模型验证
        - 业务规则检查
        - 数据转换
        
        参数:
            model: 模型实例对象
        
        返回:
            Dict: 创建后的业务对象字典
        
        示例:
            user = User(name="Bob", email="bob@example.com")
            user_dict = user_service.create_from_model(user)
        """
        pass
    
    @abstractmethod
    def update(self, id: int, data: Dict[str, Any]) -> Dict:
        """
        更新业务对象
        
        处理更新业务对象的完整流程，支持部分字段更新。
        
        业务逻辑可包含:
        - 存在性检查：验证要更新的对象是否存在
        - 数据验证：调用 validate 方法验证更新数据
        - 业务规则检查：如状态转换合法性
        - 乐观锁处理：防止并发更新冲突
        - 更新时间戳：自动更新 updated_at 字段
        
        参数:
            id: 要更新的业务对象 ID
            data: 要更新的字段字典（支持部分字段更新）
        
        返回:
            Dict: 更新后的完整业务对象
        
        异常:
            ValueError: 对象不存在、数据验证失败或业务规则违反时抛出
        
        示例:
            update_data = {'name': 'Alice Updated', 'email': 'alice_new@example.com'}
            updated_user = user_service.update(1, update_data)
        """
        pass
    
    @abstractmethod
    def update_from_model(self, model: T) -> Dict:
        """
        从模型对象更新业务对象
        
        使用 merge 操作将模型实例的状态同步到数据库。
        
        参数:
            model: 包含更新数据的模型实例
        
        返回:
            Dict: 更新后的业务对象字典
        
        示例:
            user = user_service.get_orm_instance(1)
            user.name = "New Name"
            updated_user = user_service.update_from_model(user)
        """
        pass
    
    @abstractmethod
    def delete(self, id: int, soft: bool = True) -> bool:
        """
        删除业务对象
        
        支持软删除和硬删除两种模式，可根据业务需求选择。
        
        业务逻辑可包含:
        - 权限检查：验证用户是否有删除权限
        - 关联数据检查：检查是否有依赖数据阻止删除
        - 业务规则验证：如某些状态的对象不可删除
        
        参数:
            id: 要删除的业务对象 ID
            soft: 是否软删除
                - True: 软删除，设置 is_active=False 或 deleted_at
                - False: 硬删除，从数据库中物理删除
        
        返回:
            bool: True 表示删除成功，False 表示对象不存在
        
        示例:
            # 软删除（推荐）
            if user_service.delete(1, soft=True):
                print("用户已禁用")
        """
        pass
    
    @abstractmethod
    def get_orm_instance(self, id: int) -> Optional[T]:
        """
        获取 ORM 实例
        
        返回完整的 ORM 模型实例，可用于进一步的 ORM 操作。
        
        参数:
            id: 记录的主键 ID
        
        返回:
            Optional[T]: 模型实例，不存在时返回 None
        
        示例:
            user = user_service.get_orm_instance(1)
            if user:
                user.last_login = datetime.now()
                user_service.update_from_model(user)
        """
        pass
    
    @abstractmethod
    def batch_create(self, items: List[Dict[str, Any]]) -> List[Dict]:
        """
        批量创建业务对象
        
        一次性创建多个业务对象，提高批量处理效率。
        
        业务逻辑可包含:
        - 批量验证：验证所有数据项
        - 事务处理：确保全部成功或全部失败
        - 性能优化：使用批量插入减少数据库往返
        
        参数:
            items: 业务对象数据字典列表
        
        返回:
            List[Dict]: 创建后的业务对象列表（包含生成的 ID）
        
        异常:
            ValueError: 任一数据验证失败时抛出
        
        示例:
            users_data = [
                {'name': 'User1', 'email': 'user1@example.com'},
                {'name': 'User2', 'email': 'user2@example.com'}
            ]
            created_users = user_service.batch_create(users_data)
        """
        pass
    
    @abstractmethod
    def batch_update(self, updates: Dict[int, Dict[str, Any]]) -> int:
        """
        批量更新业务对象
        
        一次性更新多个业务对象，每个对象可以更新不同的字段。
        
        参数:
            updates: 更新字典，格式为 {record_id: {field_name: new_value, ...}}
        
        返回:
            int: 实际更新的记录数量
        
        示例:
            updates = {
                1: {'name': 'User1 Updated', 'status': 'active'},
                2: {'email': 'user2_new@example.com'}
            }
            updated_count = user_service.batch_update(updates)
        """
        pass



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