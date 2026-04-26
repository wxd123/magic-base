
# magic_base/config/base_database_manager.py
from abc import ABC, abstractmethod, contextmanager

class DatabaseManagerBase(ABC):
    @abstractmethod
    def init_database(self, drop_first: bool = False):
        """每个业务模块必须实现自己的初始化逻辑"""
        pass
    
    # 非抽象方法：提供通用的会话管理
    @contextmanager
    def session(self):
        """所有子类自动获得这个能力"""
        pass