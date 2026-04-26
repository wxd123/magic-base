# magic_base/data_access/base_database_config.py
"""
数据访问基类 - 提供数据库连接和会话管理
"""

from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Generator, Optional, Dict, Any
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session


class DatabaseConfigBase(ABC):
    """数据库配置基类"""
    
    @abstractmethod
    def get_connection_string(self) -> str:
        """获取数据库连接字符串"""
        pass
    
    @abstractmethod
    def get_engine_options(self) -> Dict[str, Any]:
        """
        获取引擎选项
        
        常用选项：
        - pool_size: 连接池大小（默认5）
        - max_overflow: 连接池最大溢出数（默认10）
        - pool_timeout: 获取连接超时时间（默认30秒）
        - pool_recycle: 连接回收时间（默认3600秒）
        - echo: 是否打印SQL语句（默认False）
        
        Returns:
            Dict[str, Any]: 引擎选项字典
        """
        pass


class DatabaseManagerBase(ABC):
    """
    数据库管理器基类
    
    提供统一的会话管理，具体模块继承此类实现自己的数据库管理。
    
    Example:
        >>> class MyDBManager(DatabaseManagerBase):
        ...     def init_database(self, drop_first=False):
        ...         Base.metadata.create_all(self.engine)
        ...     
        ...     def close(self):
        ...         super().close()
        ...         # 额外的清理逻辑
    """
    
    def __init__(self, config: DatabaseConfigBase):
        self._config = config
        self._engine: Optional[Engine] = None
        self._SessionLocal: Optional[sessionmaker] = None
    
    @property
    def engine(self) -> Engine:
        """获取数据库引擎（延迟初始化）"""
        if self._engine is None:
            self._engine = create_engine(
                self._config.get_connection_string(),
                **self._config.get_engine_options()
            )
        return self._engine
    
    @property
    def SessionLocal(self) -> sessionmaker:
        """获取会话工厂"""
        if self._SessionLocal is None:
            self._SessionLocal = sessionmaker(bind=self.engine)
        return self._SessionLocal
    
    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        """获取数据库会话（上下文管理器）"""
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
        """获取数据库会话（手动管理）"""
        return self.SessionLocal()
    
    def close(self) -> None:
        """关闭数据库引擎，释放连接"""
        if self._engine:
            self._engine.dispose()
            self._engine = None
            self._SessionLocal = None
    
    def __enter__(self):
        """支持 with 语句"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出 with 语句时关闭连接"""
        self.close()
    
    @abstractmethod
    def init_database(self, drop_first: bool = False):
        """
        初始化数据库
        
        具体模块需要实现此方法，创建自己的表。
        
        Args:
            drop_first: 是否先删除现有表（慎用）
        """
        pass