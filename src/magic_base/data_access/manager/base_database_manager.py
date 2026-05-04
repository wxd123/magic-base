"""
数据库管理器基类
"""
from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Generator, Optional
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from magic_base.data_access.config.base_database_config import DatabaseConfigBase, MagicDatabaseConfig


class DatabaseManagerBase(ABC):
    """
    数据库管理器基类
    
    提供统一的数据库会话管理和引擎生命周期控制，具体模块继承此类实现自己的数据库管理。
    
    功能特性:
        - 延迟初始化数据库引擎，避免不必要的资源消耗
        - 提供上下文管理器风格的会话管理，自动处理提交和回滚
        - 支持手动管理会话模式
        - 提供优雅的引擎关闭机制
    
    设计原则:
        子类必须实现 init_database 方法，用于具体的数据库表结构初始化。
    
    使用示例:
        # 创建配置
        config = MagicDatabaseConfig(DatabaseType.SQLITE)
        
        # 创建管理器
        db_manager = MyDatabaseManager(config)
        
        # 使用上下文管理器自动管理会话
        with db_manager.session() as session:
            result = session.query(User).filter_by(id=1).first()
        
        # 手动管理会话
        session = db_manager.get_session()
        try:
            session.add(new_user)
            session.commit()
        finally:
            session.close()
    """
    
    def __init__(self, config: DatabaseConfigBase):
        """
        初始化数据库管理器
        
        参数:
            config: 数据库配置对象，必须继承自 DatabaseConfigBase
        """
        self._config = config
        """数据库配置对象"""
        
        self._engine: Optional[Engine] = None
        """SQLAlchemy 数据库引擎实例，延迟初始化"""
        
        self._SessionLocal: Optional[sessionmaker] = None
        """会话工厂，延迟初始化"""
    
    @property
    def engine(self) -> Engine:
        """获取数据库引擎（延迟初始化）
        
        当第一次访问此属性时，会根据配置创建数据库引擎。
        引擎创建后会被缓存，后续访问直接返回缓存的实例。
        
        返回:
            Engine: SQLAlchemy 数据库引擎对象
        """
        if self._engine is None:
            print(f"\n🔧 创建数据库引擎...")
            print(f"   - 连接字符串: {self._config.get_connection_string()}")
            print(f"   - 引擎选项: {self._config.get_engine_options()}")
            self._engine = create_engine(
                self._config.get_connection_string(),
                **self._config.get_engine_options()
            )
        return self._engine
    
    @property
    def SessionLocal(self) -> sessionmaker:
        """获取会话工厂
        
        当第一次访问此属性时，会基于数据库引擎创建会话工厂。
        会话工厂创建后会被缓存，后续访问直接返回缓存的实例。
        
        返回:
            sessionmaker: SQLAlchemy 会话工厂，用于创建新的会话对象
        """
        if self._SessionLocal is None:
            self._SessionLocal = sessionmaker(bind=self.engine)
        return self._SessionLocal
    
    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        """获取数据库会话（上下文管理器）
        
        使用上下文管理器自动管理会话的生命周期：
            - 成功执行时自动提交事务
            - 发生异常时自动回滚事务
            - 无论成功与否都会关闭会话
        
        这是推荐的会话使用方式，可以避免手动管理事务和资源泄露。
        
        产生:
            Session: 数据库会话对象
            
        示例:
            with db_manager.session() as session:
                # 数据库操作
                user = session.query(User).get(1)
                # 退出上下文时自动提交
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_session(self) -> Session:
        """获取数据库会话（手动管理）
        
        返回一个新的会话对象，调用者负责管理会话的生命周期：
            - 必须手动调用 commit() 提交事务
            - 必须手动调用 close() 关闭会话
            - 发生异常时需要手动调用 rollback()
        
        返回:
            Session: 数据库会话对象
            
        示例:
            session = db_manager.get_session()
            try:
                session.add(new_user)
                session.commit()
            except Exception as e:
                session.rollback()
                raise
            finally:
                session.close()
        """
        return self.SessionLocal()
    
    def close(self) -> None:
        """关闭数据库引擎
        
        释放数据库引擎占用的所有资源，包括连接池中的所有连接。
        关闭后，可以重新调用 engine 属性重新创建引擎。
        
        使用场景:
            - 应用关闭时的清理工作
            - 单元测试的清理阶段
            - 需要重新配置数据库连接时
        """
        if self._engine:
            self._engine.dispose()
            self._engine = None
            self._SessionLocal = None
    
    def __enter__(self):
        """上下文管理器入口
        
        支持 with 语句，返回自身实例。
        
        返回:
            DatabaseManagerBase: 管理器实例
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口
        
        自动调用 close() 方法释放数据库资源。
        
        参数:
            exc_type: 异常类型
            exc_val: 异常值
            exc_tb: 异常追踪信息
        """
        self.close()
    
    @abstractmethod
    def init_database(self, drop_first: bool = False):
        """
        初始化数据库（子类必须实现）
        
        创建或更新数据库表结构。子类应根据自己的 ORM 模型实现此方法。
        
        参数:
            drop_first: 是否先删除现有表，设置为 True 会清空所有现有数据，请谨慎使用
            
        异常:
            NotImplementedError: 子类未实现此方法时抛出
            
        示例:
            def init_database(self, drop_first: bool = False):
                if drop_first:
                    Base.metadata.drop_all(bind=self.engine)
                Base.metadata.create_all(bind=self.engine)
        """
        pass


class MagicDatabaseManager(DatabaseManagerBase):
    """
    共享数据库管理器
    
    为 Magic 系列项目提供的通用数据库管理器实现。
    提供便捷的表初始化方法，子类只需提供 SQLAlchemy Base 即可快速初始化数据库。
    
    使用场景:
        - 标准的 CRUD 应用
        - 简单的数据库访问层
        - 快速原型开发
    
    使用示例:
        # 创建配置
        config = MagicDatabaseConfig()
        
        # 创建管理器并设置 Base
        db_manager = MagicDatabaseManager(config)
        db_manager.set_base(Base)  # Base 是 SQLAlchemy 声明式基类
        
        # 初始化数据库
        db_manager.init_database()
        
        # 使用会话
        with db_manager.session() as session:
            users = session.query(User).all()
    """
    
    def __init__(self, config: MagicDatabaseConfig, base=None):
        """
        初始化 Magic 数据库管理器
        
        参数:
            config: Magic 数据库配置对象
            base: SQLAlchemy 声明式基类，可选，可以在初始化后通过 set_base() 设置
        """
        super().__init__(config)
        """调用父类初始化方法"""
        
        self._base = base
        """SQLAlchemy 声明式基类，包含所有模型定义的表元数据"""
    
    def set_base(self, base):
        """设置 SQLAlchemy Base（延迟设置）
        
        允许在创建管理器实例后单独设置 Base 对象，便于某些需要延迟绑定的场景。
        
        参数:
            base: SQLAlchemy 声明式基类，必须包含 metadata 属性
            
        使用场景:
            # 循环导入问题的解决方案
            db_manager = MagicDatabaseManager(config)
            # 延迟导入 Base 避免循环依赖
            from myapp.models import Base
            db_manager.set_base(Base)
        """
        self._base = base
    
    def init_database(self, drop_first: bool = False):
        """初始化数据库表
        
        根据 SQLAlchemy Base 中定义的模型，创建所有数据库表。
        
        参数:
            drop_first: 是否先删除现有表，默认为 False
                      设置为 True 会删除所有现有表和数据，请仅在开发和测试环境中使用
            
        异常:
            ValueError: 当 Base 尚未设置时抛出
            
        警告:
            drop_first=True 会删除所有现有数据，生产环境请勿使用！
            
        示例:
            # 正常初始化（保持现有数据）
            db_manager.init_database()
            
            # 重新初始化（清空所有数据）
            db_manager.init_database(drop_first=True)
        """
        if self._base is None:
            raise ValueError("SQLAlchemy Base not set. Call set_base() first.")
        
        if drop_first:
            self._base.metadata.drop_all(bind=self.engine)
        self._base.metadata.create_all(bind=self.engine)