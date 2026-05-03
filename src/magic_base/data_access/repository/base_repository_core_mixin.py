# magicm_base/data_access/repository/base_repository.py

from typing import Dict, List, Optional, TypeVar, Generic, Type, Any, get_origin, get_args
from sqlalchemy.orm import Session
from magic_base.data_access.manager.base_database_manager import DatabaseManagerBase


T = TypeVar('T')


class RepositoryCoreMixin(Generic[T]):
    """
    Repository 核心 Mixin
    
    提供 Repository 的基础设施：模型类提取、会话管理、表名推断等。
    所有 Repository 类都应该继承此 Mixin。
    
    设计理念:
        将 Repository 的核心功能提取到独立的 Mixin 中，便于其他 Mixin 类复用。
        负责处理泛型模型类的自动提取、数据库会话的延迟初始化、表名的智能推断。
    
    泛型参数:
        T: ORM 模型类的类型
    
    类属性:
        _model_class: 存储提取出的模型类
        _session: 数据库会话实例（延迟初始化）
        _table_name: 推断出的数据库表名
    
    使用方式:
        class MyRepository(RepositoryCoreMixin[User]):
            pass
    """
    
    def __new__(cls, *args, **kwargs):
        """在子类实例化时自动提取泛型类型
        
        拦截实例创建过程，在实例化前自动提取子类指定的泛型模型类。
        确保每个子类都能正确地知道它要操作的模型类型。
        
        参数:
            *args: 位置参数
            **kwargs: 关键字参数
        
        返回:
            子类实例
        
        注意:
            对于抽象基类（BaseRepository 和 RepositoryCoreMixin 本身），不进行提取，
            允许它们被正常实例化（虽然通常不会直接实例化）。
        """
        instance = super().__new__(cls)
        try:
            instance._model_class = cls._extract_model_class()
        except TypeError:
            # 如果是抽象基类本身，不设置 _model_class
            pass
        return instance
        
       
    def __init__(self, session: Optional[Session] = None):
        """
        初始化 Repository 核心
        
        负责设置数据库会话、提取表名等核心基础设施。
        
        参数:
            session: 数据库会话（可选，如果不提供则自动从 db_connection 获取）
        
        异常:
            RuntimeError: 当模型类未正确初始化时抛出
        """
        # 如果是 Mixin 类本身，跳过初始化
        if type(self).__name__ in ['RepositoryCoreMixin', 'BaseRepository']:
            return
            
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
        """从泛型参数提取模型类
        
        通过检查类的原始基类（__orig_bases__）和泛型参数（__args__），
        自动提取子类在继承时指定的模型类型。
        
        工作原理:
            1. 优先检查 __orig_bases__（Python 3.8+ 特性）
            2. 降级检查 __bases__（兼容旧版本）
            3. 查找继承自 BaseRepository 或 RepositoryCoreMixin 的基类
            4. 从该基类的泛型参数中提取第一个参数作为模型类
        
        返回:
            Type[T]: 泛型参数中指定的模型类
        
        异常:
            TypeError: 当无法提取到泛型类型时抛出
        
        示例:
            class UserRepository(BaseRepository[User]):
                pass
            # UserRepository._extract_model_class() 返回 User 类
        """
        # 方法1：检查当前类的直接基类
        if hasattr(cls, '__orig_bases__'):
            for base in cls.__orig_bases__:
                args = get_args(base)
                if args and not isinstance(args[0], TypeVar):
                    # 找到具体类型（不是 TypeVar），直接返回
                    return args[0]
        
        # 方法2：如果当前类还有父类，递归查找
        for base in cls.__bases__:
            if base is not object and hasattr(base, '_extract_model_class'):
                try:
                    # 尝试从父类提取
                    return base._extract_model_class()
                except TypeError:
                    continue  # 父类也没找到，继续找下一个父类
        
        # 实在找不到，抛出异常
        raise TypeError(
            f"{cls.__name__} 必须指定泛型类型。\n"
            f"正确用法：class {cls.__name__}(BaseRepository[UserModel]): pass"
        )
    
    def _get_session(self) -> Session:
        """获取数据库会话（延迟初始化）
        
        如果实例化时提供了 session 则直接使用，否则从全局 DatabaseManagerBase 获取。
        采用延迟初始化策略，避免在不需要数据库操作时建立不必要的连接。
        
        返回:
            Session: 数据库会话对象
        """
        if self._session is None:
            self._session = DatabaseManagerBase.session()
        return self._session
    
    @property
    def session(self) -> Session:
        """获取数据库会话
        
        通过属性方式提供会话访问，内部调用 _get_session 实现延迟初始化。
        
        返回:
            Session: 数据库会话对象
        
        示例:
            repo = UserRepository()
            session = repo.session  # 第一次访问时自动初始化
        """
        return self._get_session()
    
    @property
    def model_class(self) -> Type[T]:
        """获取模型类
        
        返回子类指定的 ORM 模型类，用于创建实例和类型提示。
        
        返回:
            Type[T]: ORM 模型类
        
        示例:
            repo = UserRepository()
            new_user = repo.model_class(name="Alice")
        """
        return self._model_class
    
    @property
    def table_name(self) -> str:
        """获取表名
        
        返回与模型类对应的数据库表名，由 _get_table_name_from_model 推断得出。
        
        返回:
            str: 数据库表名
        
        示例:
            repo = UserRepository()
            print(repo.table_name)  # "users"
        """
        return self._table_name
    
    def _get_table_name_from_model(self, model_class: Type[T]) -> str:
        """从模型类自动获取表名
        
        使用多种策略智能推断表名：
            1. 优先使用模型类的 __tablename__ 属性（显式定义）
            2. 其次使用 SQLAlchemy 的 __table__.name 属性
            3. 最后降级方案：将驼峰命名转换为蛇形命名，并添加复数 's'
        
        参数:
            model_class: ORM 模型类
        
        返回:
            str: 推断出的数据库表名
        
        示例:
            class User(Base):
                __tablename__ = "sys_users"
            # 返回 "sys_users"
            
            class Product(Base):
                pass
            # 返回 "products"（驼峰转蛇形+复数）
        """
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