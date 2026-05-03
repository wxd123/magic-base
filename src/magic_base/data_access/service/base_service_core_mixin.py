# magic_base/data_access/service/base_service.py
"""
Service 基类 - 定义业务层接口
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Dict, Any
from magic_base.data_access.repository.base_repository_cud_mixin import CUDRepositoryMixin
from magic_base.data_access.repository.base_repository_query_mixin import QueryRepositoryMixin


T = TypeVar('T')  # 业务对象类型


class ServiceCoreMixin(Generic[T]):
    """
    Service 核心 Mixin
    
    提供 Service 的基础设施：验证接口、依赖注入等。
    所有 Service 类都应该继承此 Mixin。
    
    设计理念:
        与 RepositoryCoreMixin 对应，提供 Service 层的核心功能。
        负责定义基础的业务验证接口和公共属性。
    
    泛型参数:
        T: 业务对象类型，可以是 Dict、Model 或自定义 DTO
    """
    
    @abstractmethod
    def validate(self, data: Dict[str, Any], is_update: bool = False) -> bool:
        """
        验证业务数据
        
        子类应实现具体的验证逻辑，确保数据符合业务规则。
        
        常见的验证项:
        - 必填字段检查：确保关键字段已提供
        - 格式验证：如邮箱、手机号、日期等格式
        - 长度验证：字符串长度限制
        - 取值范围验证：数字、枚举值的合法范围
        - 唯一性检查：与数据库中的现有数据对比
        - 业务规则验证：符合业务逻辑的规则
        - 关联数据验证：关联对象的存在性
        
        参数:
            data: 要验证的业务数据字典
            is_update: 是否为更新操作
                       True: 更新操作，某些字段可能未提供
                       False: 创建操作，通常需要完整验证
        
        返回:
            bool: True 表示验证通过
        
        异常:
            ValueError: 验证失败时抛出，建议包含详细的错误信息
        
        示例:
            def validate(self, data: Dict[str, Any], is_update: bool = False) -> bool:
                # 邮箱验证
                email = data.get('email')
                if not email and not is_update:
                    raise ValueError("邮箱是必填字段")
                if email and '@' not in email:
                    raise ValueError("邮箱格式不正确")
                
                # 年龄验证
                age = data.get('age')
                if age is not None:
                    if not isinstance(age, int) or age < 0 or age > 150:
                        raise ValueError("年龄必须在0-150之间")
                
                return True
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