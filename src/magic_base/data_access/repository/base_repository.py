# magicm_base/data_access/repository/base_repository.py

from abc import ABC
from typing import Dict, List, Optional, TypeVar, Generic, Type, Any, get_origin, get_args
from sqlalchemy.orm import Session
from sqlalchemy import inspect, text

from .base_repository_cud_mixin import CUDRepositoryMixin
from .base_repository_query_mixin import QueryRepositoryMixin


T = TypeVar('T')


class BaseRepository(CUDRepositoryMixin[T], QueryRepositoryMixin[T]):
    """
    混合 Repository 基类（抽象基类，只能通过继承使用）
    
    组合 CUD 和 Query 两个 Mixin，提供完整的 CRUD 操作。
    
    - CUD (创建/更新/删除): 使用 ORM
    - R (查询): 使用原生 SQL
    
    设计理念:
        采用混合策略，发挥各自优势：
        - 写操作使用 ORM：获得对象关系映射的便利性、自动事务管理、关联关系处理
        - 读操作使用原生 SQL：获得更好的性能、更灵活的查询、复杂 JOIN 支持
    
    继承关系:
        BaseRepository
        ├── CUDRepositoryMixin (ORM 写操作)
        │   └── RepositoryCoreMixin (核心基础设施)
        └── QueryRepositoryMixin (SQL 读操作)
            └── RepositoryCoreMixin (核心基础设施)
    
    使用方式：
        class UserRepository(BaseRepository[User]):
            '''用户数据仓库'''
            pass
        
        # 实例化
        repo = UserRepository(session)  # 使用现有会话
        repo = UserRepository()          # 自动获取会话
        
        # 执行操作
        user = repo.create(name="Alice", email="alice@example.com")
        user_dict = repo.get_by_id(user.id)
        users = repo.find(conditions={'is_active': True})
    
    设计优势:
        - 职责分离：核心、CUD、查询各司其职，代码清晰易维护
        - 灵活组合：可以根据需要只继承部分 Mixin（如只读 Repository）
        - 易于测试：每个 Mixin 可以独立测试，降低测试复杂度
        - 代码复用：不同的 Repository 可以灵活组合不同的能力
        - 类型安全：完整的泛型支持，IDE 可提供准确的代码补全
    
    注意事项:
        1. 此类为抽象基类，不能直接实例化，必须通过子类继承
        2. 子类必须指定泛型类型 T（具体的 ORM 模型类）
        3. 泛型类型会在实例化时自动提取，无需手动设置
    
    示例:
        # 定义模型
        class User(Base):
            __tablename__ = 'users'
            id = Column(Integer, primary_key=True)
            name = Column(String)
            email = Column(String)
        
        # 定义 Repository
        class UserRepository(BaseRepository[User]):
            '''用户数据仓库'''
            
            def find_by_email(self, email: str) -> Optional[Dict]:
                '''自定义查询方法'''
                return self.find_one({'email': email})
            
            def activate_user(self, user_id: int) -> bool:
                '''自定义业务方法'''
                return self.update(user_id, is_active=True)
        
        # 使用 Repository
        repo = UserRepository()
        
        # 继承的基础方法
        user = repo.create(name="Bob", email="bob@example.com")
        user_dict = repo.get_by_id(user.id)
        
        # 自定义方法
        user = repo.find_by_email("bob@example.com")
        repo.activate_user(user['id'])
    """
    
    def __new__(cls, *args, **kwargs):
        """在子类实例化时自动提取泛型类型
        
        拦截实例创建过程，确保抽象基类不能被直接实例化，
        同时允许子类正常实例化。
        
        执行流程:
            1. 检查当前类是否为 BaseRepository 本身
            2. 如果是，抛出 TypeError 禁止实例化
            3. 如果不是（说明是子类），正常创建实例
        
        参数:
            *args: 位置参数
            **kwargs: 关键字参数
        
        返回:
            子类实例
        
        异常:
            TypeError: 当尝试直接实例化 BaseRepository 时抛出
        
        示例:
            # 错误用法 - 会抛出 TypeError
            repo = BaseRepository()
            
            # 正确用法
            repo = UserRepository()
        
        注意:
            此方法只检查直接实例化 BaseRepository 的情况，
            子类实例化时会正常通过检查。
        """
        if cls is BaseRepository:
            raise TypeError(f"抽象基类 {cls.__name__} 不能直接实例化，请使用子类继承")
        
        instance = super().__new__(cls)
        return instance
    
    def __init__(self, session: Optional[Session] = None):
        """初始化 Repository
        
        调用父类（CUDRepositoryMixin 和 QueryRepositoryMixin）的初始化方法，
        设置数据库会话、模型类、表名等核心属性。
        
        参数:
            session: 数据库会话（可选，如果不提供则自动从 db_connection 获取）
        
        示例:
            # 使用自动会话管理
            repo = UserRepository()
            
            # 使用自定义会话
            from sqlalchemy.orm import Session
            session = Session(engine)
            repo = UserRepository(session)
        
        注意:
            session 采用延迟初始化策略，只有在首次使用时才会获取，
            这样可以避免在 Repository 创建时就依赖数据库连接。
        """
        super().__init__(session)


class MagicBaseRepository(ABC, BaseRepository[T]):
    """
    Magic 系列基础 Repository 适配类
    
    继承自 ABC（抽象基类）和 BaseRepository，为 Magic 系列项目提供统一的 Repository 基类。
    
    设计目的:
        为 Magic 生态系统中的各个项目提供一致的 Repository 接口，
        便于代码复用和统一管理。
    
    多重继承说明:
        - ABC: 来自 abc 模块的抽象基类，确保此类不能被直接实例化
        - BaseRepository: 提供完整的 CRUD 操作能力
    
    使用方式:
        from magic_base.data_access.repository import MagicBaseRepository
        
        # 基础用法
        class UserRepository(MagicBaseRepository[User]):
            '''用户数据仓库'''
            pass
        
        # 可以添加自定义方法
        class ProductRepository(MagicBaseRepository[Product]):
            '''产品数据仓库'''
            
            def find_by_category(self, category_id: int) -> List[Dict]:
                '''根据分类查找产品'''
                return self.find(conditions={'category_id': category_id})
            
            def find_active_products(self) -> List[Dict]:
                '''查找激活的产品'''
                return self.find(conditions={'is_active': True})
        
        # 只读 Repository（不需要 CUD 操作）
        class ReadOnlyRepository(QueryRepositoryMixin[ReadOnlyModel]):
            '''只读 Repository，没有 CUD 操作'''
            def find_by_name(self, name: str) -> Optional[Dict]:
                return self.find_one({'name': name})
    
    与 BaseRepository 的区别:
        - MagicBaseRepository 添加了 ABC 抽象标记
        - MagicBaseRepository 是 Magic 生态的统一接口
        - BaseRepository 是更通用的实现
    
    注意:
        此类为抽象基类，通过 ABC 确保不能被直接实例化。
        必须通过子类继承并实例化子类。
    
    示例:
        # 定义模型
        from magic_base.data_access.model import MagicBaseModel
        
        class User(MagicBaseModel):
            __tablename__ = 'magic_users'
            username = Column(String(50), unique=True)
            email = Column(String(100), unique=True)
        
        # 定义 Repository
        class UserRepository(MagicBaseRepository[User]):
            '''Magic 用户仓库'''
            
            def find_by_username(self, username: str) -> Optional[Dict]:
                '''根据用户名查找用户'''
                return self.find_one({'username': username})
            
            def exists_by_email(self, email: str) -> bool:
                '''检查邮箱是否存在'''
                return self.exists(email=email)
        
        # 使用
        repo = UserRepository()
        
        # 创建用户
        user = repo.create(
            username='alice',
            email='alice@magic.com',
            is_active=True
        )
        
        # 查询用户
        user_dict = repo.find_by_username('alice')
        print(f"找到用户: {user_dict['email']}")
        
        # 检查存在性
        if repo.exists_by_email('new@magic.com'):
            print("邮箱已被注册")
    
    扩展建议:
        可以根据项目需求，在 MagicBaseRepository 基础上添加更多通用方法，
        如批量导入、导出、缓存等。
    """
    pass