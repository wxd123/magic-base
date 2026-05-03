# magic_base/core/context.py

import threading
from typing import Optional, Generic, TypeVar

from magic_base.data_access.config.base_database_config import DatabaseConfigBase
from magic_base.data_access.manager.base_database_manager import DatabaseManagerBase





# 定义泛型变量
ContextType = TypeVar('ContextType')

class ApplicationContext(Generic[ContextType]):
    """全局应用上下文 - 泛型基类
    
    每个项目继承此类并指定自己的上下文类型
    """
    
    _lock = threading.Lock()
    
    # 共享属性（所有项目都需要）
    db_config: Optional[DatabaseConfigBase] = None
    db_manager: Optional[DatabaseManagerBase] = None
    
    # 项目特定上下文（泛型）
    context: Optional[ContextType] = None
    
    @classmethod
    def initialize(cls, 
                   db_config: Optional[DatabaseConfigBase] = None,
                   db_manager: Optional[DatabaseManagerBase] = None,
                   context: Optional[ContextType] = None):
        """初始化全局上下文"""
        with cls._lock:
            if db_config is not None:
                cls.db_config = db_config
            if db_manager is not None:
                cls.db_manager = db_manager
            if context is not None:
                cls.context = context
    
    @classmethod
    def get_db_manager(cls) -> DatabaseManagerBase:
        if cls.db_manager is None:
            raise RuntimeError("Database manager not initialized")
        return cls.db_manager
    
    @classmethod
    def get_context(cls) -> ContextType:
        """获取项目特定的上下文"""
        if cls.context is None:
            raise RuntimeError("Context not initialized")
        return cls.context
    
    @classmethod
    def reset(cls):
        with cls._lock:
            cls.db_config = None
            cls.db_manager = None
            cls.context = None



__all__ = ['ApplicationContext']