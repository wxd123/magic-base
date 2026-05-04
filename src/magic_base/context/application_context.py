# magic_base/core/context.py

import threading
from typing import Optional, Generic, TypeVar

from magic_base.data_access.config.base_database_config import DatabaseConfigBase
from magic_base.data_access.manager.base_database_manager import DatabaseManagerBase


# 定义泛型变量
ContextType = TypeVar('ContextType')

class ApplicationContext(Generic[ContextType]):
    """全局应用上下文 - 泛型基类
    
    提供全局单例级别的上下文管理，支持数据库配置、数据库管理器以及项目特定的上下文信息。
    使用线程锁保证多线程环境下的线程安全。
    
    每个项目可以继承此类并指定自己的上下文类型，从而获得类型安全的上下文访问。
    
    泛型参数:
        ContextType: 项目特定上下文的类型，可以是任何自定义类或数据结构
    
    类属性:
        _lock: 线程锁，用于保证初始化与重置操作的原子性
        db_config: 数据库配置对象，用于存储数据库连接参数
        db_manager: 数据库管理器对象，用于执行数据库操作
        context: 项目特定的上下文对象，类型由泛型参数ContextType决定
    
    使用示例:
        # 定义项目特定上下文类
        class MyContext:
            user_id: str
            tenant_id: str
        
        # 初始化全局上下文
        ApplicationContext[MyContext].initialize(
            db_config=my_db_config,
            db_manager=my_db_manager,
            context=MyContext(user_id="123", tenant_id="tenant1")
        )
        
        # 获取上下文
        ctx = ApplicationContext[MyContext].get_context()
        db_mgr = ApplicationContext[MyContext].get_db_manager()
    """
    
    _lock = threading.Lock()
    
    # 共享属性（所有项目都需要）
    db_config: Optional[DatabaseConfigBase] = None
    """数据库配置对象，可选，未设置时为None"""
    
    db_manager: Optional[DatabaseManagerBase] = None
    """数据库管理器对象，可选，未设置时为None"""
    
    # 项目特定上下文（泛型）
    context: Optional[ContextType] = None
    """项目特定上下文对象，类型由泛型参数ContextType决定，未设置时为None"""
    
    @classmethod
    def initialize(cls, 
                   db_config: Optional[DatabaseConfigBase] = None,
                   db_manager: Optional[DatabaseManagerBase] = None,
                   context: Optional[ContextType] = None):
        """初始化全局上下文
        
        使用线程锁保证初始化操作的线程安全性。允许部分初始化，即可以只设置部分属性，
        未传入的参数对应的属性将保持原值不变（如果之前已设置）或保持为None。
        
        参数:
            db_config: 数据库配置对象，可选，如果提供则替换现有的db_config
            db_manager: 数据库管理器对象，可选，如果提供则替换现有的db_manager
            context: 项目特定的上下文对象，可选，如果提供则替换现有的context
        
        注意:
            此方法不是全量替换，而是增量更新。若希望完全重置所有属性，请先调用reset()方法。
        
        示例:
            # 仅初始化数据库管理器
            ApplicationContext.initialize(db_manager=my_manager)
            
            # 初始化所有属性
            ApplicationContext.initialize(
                db_config=config,
                db_manager=manager,
                context=my_context
            )
        """
        with cls._lock:
            if db_config is not None:
                cls.db_config = db_config
            if db_manager is not None:
                cls.db_manager = db_manager
            if context is not None:
                cls.context = context

        #   cls._create_tables_if_not_exists()

    @classmethod
    def _create_tables_if_not_exists(cls):
        """自动创建所有定义的表"""
        try:
            from magic_base import Base
            engine = cls.db_manager.engine
            Base.metadata.create_all(engine)  # 幂等操作，表已存在时不会重复创建
            print("✅ 数据库表结构已就绪")
        except Exception as e:
            print(f"⚠️ 建表失败（不影响核心功能）: {e}")

    @classmethod
    def get_db_manager(cls) -> DatabaseManagerBase:
        """获取数据库管理器实例
        
        返回:
            DatabaseManagerBase: 已初始化的数据库管理器对象
        
        异常:
            RuntimeError: 当db_manager尚未初始化（为None）时抛出
        
        示例:
            db_manager = ApplicationContext.get_db_manager()
            result = db_manager.query("SELECT * FROM users")
        """
        if cls.db_manager is None:
            raise RuntimeError("Database manager not initialized")
        return cls.db_manager
    
    @classmethod
    def get_context(cls) -> ContextType:
        """获取项目特定的上下文
        
        返回:
            ContextType: 项目特定的上下文对象，类型由泛型参数决定
        
        异常:
            RuntimeError: 当context尚未初始化（为None）时抛出
        
        示例:
            ctx = ApplicationContext[MyContext].get_context()
            print(ctx.user_id)  # 类型安全，IDE可提供代码补全
        """
        if cls.context is None:
            raise RuntimeError("Context not initialized")
        return cls.context
    
    @classmethod
    def reset(cls):
        """重置全局上下文
        
        将所有的类属性（db_config, db_manager, context）重置为None。
        使用线程锁保证重置操作的线程安全性。
        
        通常在以下场景使用:
            - 单元测试的清理阶段，避免测试用例之间的状态污染
            - 应用重新初始化前，需要清空旧的状态
            - 切换不同的运行时环境
        
        示例:
            # 测试用例清理
            def tearDown(self):
                ApplicationContext.reset()
        """
        with cls._lock:
            cls.db_config = None
            cls.db_manager = None
            cls.context = None


__all__ = ['ApplicationContext']
