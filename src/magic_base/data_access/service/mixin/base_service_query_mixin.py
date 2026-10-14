# magic_base/data_access/service/base_service.py
"""
Service 基类 - 定义业务层接口
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Dict, Any
from .base_service_core_mixin import ServiceCoreMixin


T = TypeVar('T')  # 业务对象类型


class QueryServiceMixin(ServiceCoreMixin[T]):
    """
    查询业务操作 Mixin (Query)
    
    提供业务层的查询操作接口。
    继承自 ServiceCoreMixin，获得核心验证功能。
    
    设计理念:
        与 QueryRepositoryMixin 对应，定义业务层的读操作接口。
        Service 层负责业务逻辑处理，通常内部会调用 QueryRepositoryMixin 的方法。
    
    包含的功能:
        - 根据 ID 查询
        - 列表查询（分页）
        - 动态条件查询
        - 存在性检查
        - 计数统计
        - 分页查询
    
    使用方式:
        class UserService(QueryServiceMixin[User]):
            def __init__(self, user_repo: UserRepository):
                self.user_repo = user_repo
            
            def get_by_id(self, id: int) -> Optional[Dict]:
                # 业务逻辑：权限检查
                if not self.has_permission(id):
                    return None
                return self.user_repo.get_by_id(id)
    """
    
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Dict]:
        """
        根据 ID 获取业务对象
        
        业务逻辑可包含:
        - 权限检查：验证当前用户是否有权限查看该对象
        - 数据转换：将数据库对象转换为前端需要的格式
        - 关联数据加载：加载相关联的其他数据
        - 缓存处理：从缓存读取或更新缓存
        
        参数:
            id: 业务对象的主键 ID
        
        返回:
            Optional[Dict]: 业务对象字典，未找到时返回 None
        
        示例:
            user = user_service.get_by_id(1)
            if user:
                print(f"用户: {user['name']}, 角色: {user['role']}")
        """
        pass
    
    @abstractmethod
    def get_list(self, filters: Optional[Dict] = None,
                 order_by: Optional[str] = None,
                 limit: Optional[int] = None) -> List[Dict]:
        """
        获取业务对象列表
        
        支持过滤条件、排序和限制返回数量。
        
        业务逻辑可包含:
        - 权限过滤：根据用户权限过滤可见数据
        - 数据脱敏：隐藏敏感字段
        - 格式化输出：转换日期、枚举等字段格式
        
        参数:
            filters: 过滤条件字典，格式为 {field_name: value}
            order_by: 排序字段，如 "created_at DESC"
            limit: 返回记录数量限制
        
        返回:
            List[Dict]: 业务对象字典列表
        
        示例:
            users = user_service.get_list(
                filters={'is_active': True},
                order_by='created_at DESC',
                limit=10
            )
        """
        pass
    
    @abstractmethod
    def find(self, conditions: Optional[Dict[str, Any]] = None,
             order_by: Optional[str] = None,
             limit: Optional[int] = None,
             offset: Optional[int] = None) -> List[Dict]:
        """
        动态查询业务对象
        
        灵活的查询方法，支持等值条件、排序、分页。
        
        业务逻辑可包含:
        - 动态条件构建
        - 数据权限过滤
        - 字段映射转换
        
        参数:
            conditions: 查询条件字典，格式为 {field_name: value}
            order_by: 排序字段，如 "created_at DESC"
            limit: 返回记录数量限制
            offset: 偏移量，用于分页
        
        返回:
            List[Dict]: 业务对象字典列表
        
        示例:
            users = user_service.find(
                conditions={'is_active': True, 'age': 25},
                order_by='id DESC',
                limit=20,
                offset=0
            )
        """
        pass
    
    @abstractmethod
    def find_one(self, conditions: Dict[str, Any]) -> Optional[Dict]:
        """
        查询单个业务对象
        
        根据条件查询第一条匹配的记录。
        
        参数:
            conditions: 查询条件字典，格式为 {field_name: value}
        
        返回:
            Optional[Dict]: 业务对象字典，未找到时返回 None
        
        示例:
            user = user_service.find_one({'email': 'alice@example.com'})
        """
        pass
    
    @abstractmethod
    def exists(self, **conditions) -> bool:
        """
        检查业务对象是否存在
        
        快速检查是否存在满足条件的业务对象，常用于唯一性验证。
        
        参数:
            **conditions: 条件字段和值的键值对
        
        返回:
            bool: True 表示存在，False 表示不存在
        
        示例:
            if user_service.exists(email='alice@example.com'):
                raise ValueError("邮箱已被注册")
        """
        pass
    
    @abstractmethod
    def count(self, filters: Optional[Dict] = None) -> int:
        """
        统计业务对象数量
        
        统计满足条件的业务对象总数，常用于数据概览和分页计算。
        
        参数:
            filters: 过滤条件字典，格式为 {field_name: value}
        
        返回:
            int: 符合条件的业务对象数量
        
        示例:
            active_count = user_service.count({'is_active': True})
        """
        pass
    
    @abstractmethod
    def paginate(self, page: int = 1, per_page: int = 20,
                 conditions: Optional[Dict[str, Any]] = None,
                 order_by: str = "id DESC") -> Dict[str, Any]:
        """
        分页查询业务对象
        
        实现标准的分页查询，返回包含数据和分页信息的字典。
        
        业务逻辑可包含:
        - 分页参数验证
        - 数据权限过滤
        - 结果集转换
        
        参数:
            page: 当前页码，从 1 开始
            per_page: 每页记录数
            conditions: 查询条件字典
            order_by: 排序字段，默认为 "id DESC"
        
        返回:
            Dict[str, Any]: 分页结果字典，包含以下键：
                - items: 当前页的数据列表 (List[Dict])
                - total: 总记录数 (int)
                - page: 当前页码 (int)
                - per_page: 每页记录数 (int)
                - pages: 总页数 (int)
                - has_next: 是否有下一页 (bool)
                - has_prev: 是否有上一页 (bool)
        
        示例:
            result = user_service.paginate(
                page=2,
                per_page=10,
                conditions={'is_active': True},
                order_by='created_at DESC'
            )
            for user in result['items']:
                print(user['name'])
            print(f"第 {result['page']}/{result['pages']} 页")
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