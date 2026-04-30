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
    
    提供统一的会话管理，具体模块继承此类实现自己的数据库管理。
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
        """关闭数据库引擎"""
        if self._engine:
            self._engine.dispose()
            self._engine = None
            self._SessionLocal = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    @abstractmethod
    def init_database(self, drop_first: bool = False):
        """
        初始化数据库（子类必须实现）
        
        Args:
            drop_first: 是否先删除现有表（慎用）
        """
        pass


class MagicDatabaseManager(DatabaseManagerBase):
    """
    共享数据库管理器
    
    提供便捷的表初始化方法，子类只需提供 SQLAlchemy Base
    """
    
    def __init__(self, config: MagicDatabaseConfig, base=None):
        """
        Args:
            config: 数据库配置
            base: SQLAlchemy 声明式基类
        """
        super().__init__(config)
        self._base = base
    
    def set_base(self, base):
        """设置 SQLAlchemy Base（延迟设置）"""
        self._base = base
    
    def init_database(self, drop_first: bool = False):
        """初始化数据库表"""
        if self._base is None:
            raise ValueError("SQLAlchemy Base not set. Call set_base() first.")
        
        if drop_first:
            self._base.metadata.drop_all(bind=self.engine)
        self._base.metadata.create_all(bind=self.engine)
    