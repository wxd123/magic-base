"""
数据库配置基类
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path
from enum import Enum


class DatabaseType(Enum):
    """数据库类型"""
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"


class DatabaseConfigBase(ABC):
    """数据库配置抽象基类"""
    
    @abstractmethod
    def get_connection_string(self) -> str:
        """获取数据库连接字符串"""
        pass
    
    @abstractmethod
    def get_engine_options(self) -> Dict[str, Any]:
        """获取引擎选项"""
        pass


class MagicDatabaseConfig(DatabaseConfigBase):
    """
    Magic 系列统一数据库配置
    
    只做一件事：提供统一的数据库配置
    """
    
    MAGIC_DATA_DIR = Path.home() / "magic" / "data"
    
    def __init__(
        self, 
        db_type: DatabaseType = DatabaseType.SQLITE,
        **kwargs
    ):
        """
        Args:
            db_type: 数据库类型
            **kwargs: 连接参数
                SQLite: path="custom.db"
                PostgreSQL: host, port, user, password, database
                MySQL: host, port, user, password, database
        """
        self.db_type = db_type
        self.kwargs = kwargs
        self._engine_options_cache = None        
        
       
        if db_type == DatabaseType.SQLITE:        
            # 本地数据库路径，服务于sqllite
            self.db_path = self._get_sqlite_path()
        else:
            self.db_path = None
    
    def get_connection_string(self) -> str:
        """统一构建连接字符串"""
        if self.db_type == DatabaseType.SQLITE:
            return self._build_sqlite()
        elif self.db_type == DatabaseType.POSTGRESQL:
            return self._build_postgresql()
        elif self.db_type == DatabaseType.MYSQL:
            return self._build_mysql()
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")
    
    def _get_sqlite_path(self) -> str:
        """获取 SQLite 数据库路径"""
        path = self.kwargs.get("path", "magic.db")
        
        # 判断是否使用默认目录
        if "path" not in self.kwargs:
            # 用户没有指定 path，使用默认目录
            path = self.MAGIC_DATA_DIR / path
            self.MAGIC_DATA_DIR.mkdir(parents=True, exist_ok=True)
        else:
            # 用户指定了 path，处理相对路径
            path_obj = Path(path)
            if not path_obj.is_absolute():
                # 相对路径：相对于当前工作目录
                path = Path.cwd() / path_obj
            else:
                path = path_obj
            
            # 确保目录存在
            path.parent.mkdir(parents=True, exist_ok=True)
        
        return str(path)
        
    def _build_sqlite(self) -> str:
        """SQLite 连接字符串"""
        
        return f"sqlite:///{self.db_path}"
    
    def _build_postgresql(self) -> str:
        """PostgreSQL 连接字符串"""
        host = self.kwargs.get("host", "localhost")
        port = self.kwargs.get("port", 5432)
        user = self.kwargs.get("user", "")
        password = self.kwargs.get("password", "")
        database = self.kwargs.get("database", "magic")
        
        auth = f"{user}:{password}@" if user and password else f"{user}@" if user else ""
        return f"postgresql://{auth}{host}:{port}/{database}"
    
    def _build_mysql(self) -> str:
        """MySQL 连接字符串"""
        host = self.kwargs.get("host", "localhost")
        port = self.kwargs.get("port", 3306)
        user = self.kwargs.get("user", "")
        password = self.kwargs.get("password", "")
        database = self.kwargs.get("database", "magic")
        
        auth = f"{user}:{password}@" if user and password else f"{user}@" if user else ""
        return f"mysql+pymysql://{auth}{host}:{port}/{database}"
    
    def get_engine_options(self) -> Dict[str, Any]:
        """获取引擎选项"""
        if self._engine_options_cache:
            return self._engine_options_cache
        
        # 默认选项
        default_options = {
            "echo": self.kwargs.get("echo", False),
            "pool_size": self.kwargs.get("pool_size", 10),
            "max_overflow": self.kwargs.get("max_overflow", 20),
            "pool_pre_ping": self.kwargs.get("pool_pre_ping", True),
            "pool_recycle": self.kwargs.get("pool_recycle", 3600),
        }
        
        # SQLite 特殊配置
        if self.db_type == DatabaseType.SQLITE:
            default_options["connect_args"] = {"check_same_thread": False}
        
        self._engine_options_cache = default_options
        return self._engine_options_cache
    
    def get_data_dir(self) -> Path:
        """获取数据目录（仅 SQLite）"""
        if self.db_type != DatabaseType.SQLITE:
            raise RuntimeError("Data directory only available for SQLite")
        return self.MAGIC_DATA_DIR
    
    def get_db_path(self)-> str:
        return self.db_path



# 使用示例
if __name__ == "__main__":
    # 1. 默认 SQLite（最常用）
    config = MagicDatabaseConfig()
    print(config.get_connection_string())
    # 输出: sqlite:///Users/xxx/magic/data/magic.db
    
    # 2. 自定义 SQLite
    config = MagicDatabaseConfig(
        DatabaseType.SQLITE,
        path="./myapp.db",
        echo=True
    )
    
    # 3. PostgreSQL
    config = MagicDatabaseConfig(
        DatabaseType.POSTGRESQL,
        host="localhost",
        user="magic",
        password="secret",
        database="magic_db"
    )
    
    # 4. MySQL
    config = MagicDatabaseConfig(
        DatabaseType.MYSQL,
        host="192.168.1.100",
        user="root",
        password="pass123",
        database="magic_prod"
    )