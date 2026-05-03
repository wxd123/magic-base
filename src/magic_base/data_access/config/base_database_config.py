"""
数据库配置基类
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path
from enum import Enum


class DatabaseType(Enum):
    """数据库类型枚举
    
    定义了支持的数据库类型，用于统一配置不同数据库的连接参数。
    
    成员:
        SQLITE: SQLite 轻量级文件数据库
        POSTGRESQL: PostgreSQL 关系型数据库
        MYSQL: MySQL 关系型数据库
    """
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"


class DatabaseConfigBase(ABC):
    """数据库配置抽象基类
    
    定义了数据库配置的标准接口，所有具体数据库配置类都应继承此类。
    提供获取连接字符串和引擎选项的核心方法。
    """
    
    @abstractmethod
    def get_connection_string(self) -> str:
        """获取数据库连接字符串
        
        根据配置的数据库类型和参数，生成符合 SQLAlchemy 格式的连接字符串。
        
        返回:
            str: 数据库连接字符串，格式如 "sqlite:///path/to/db.db" 或
                "postgresql://user:pass@localhost:5432/dbname"
        """
        pass
    
    @abstractmethod
    def get_engine_options(self) -> Dict[str, Any]:
        """获取引擎选项
        
        返回 SQLAlchemy 引擎初始化时所需的参数字典，包括连接池配置、日志设置等。
        
        返回:
            Dict[str, Any]: 引擎选项字典，可直接传递给 SQLAlchemy create_engine 函数
        """
        pass


class MagicDatabaseConfig(DatabaseConfigBase):
    """
    Magic 系列统一数据库配置
    
    为 Magic 系列项目提供统一的数据库配置管理，支持 SQLite、PostgreSQL 和 MySQL。
    自动处理数据库文件的目录创建、路径解析等细节。
    
    设计原则:
        只做一件事：提供统一的数据库配置，不涉及业务逻辑。
    
    类属性:
        MAGIC_DATA_DIR: Magic 默认数据存储目录，位于用户家目录下的 magic/data
    """
    
    MAGIC_DATA_DIR = Path.home() / "magic" / "data"
    """Magic 默认数据目录，路径为 ~/magic/data"""
    
    def __init__(
        self, 
        db_type: DatabaseType = DatabaseType.SQLITE,
        **kwargs
    ):
        """
        初始化数据库配置
        
        参数:
            db_type: 数据库类型，默认为 SQLite。可选值见 DatabaseType 枚举
            **kwargs: 连接参数，根据数据库类型不同而不同
            
        不同数据库类型支持的 kwargs 参数:
            SQLite:
                - path: 数据库文件路径（可选），默认为 "magic.db"
                      可以是相对路径或绝对路径
                - echo: 是否打印 SQL 日志（可选），默认为 False
                - pool_size: 连接池大小（可选），默认为 10
                - max_overflow: 连接池溢出限制（可选），默认为 20
                - pool_pre_ping: 连接前检查（可选），默认为 True
                - pool_recycle: 连接回收时间（秒，可选），默认为 3600
                
            PostgreSQL:
                - host: 数据库主机地址（可选），默认为 "localhost"
                - port: 数据库端口（可选），默认为 5432
                - user: 数据库用户名（可选），默认为空字符串
                - password: 数据库密码（可选），默认为空字符串
                - database: 数据库名称（可选），默认为 "magic"
                - echo: 是否打印 SQL 日志（可选），默认为 False
                - pool_size: 连接池大小（可选），默认为 10
                - max_overflow: 连接池溢出限制（可选），默认为 20
                - pool_pre_ping: 连接前检查（可选），默认为 True
                - pool_recycle: 连接回收时间（秒，可选），默认为 3600
                
            MySQL:
                - host: 数据库主机地址（可选），默认为 "localhost"
                - port: 数据库端口（可选），默认为 3306
                - user: 数据库用户名（可选），默认为空字符串
                - password: 数据库密码（可选），默认为空字符串
                - database: 数据库名称（可选），默认为 "magic"
                - echo: 是否打印 SQL 日志（可选），默认为 False
                - pool_size: 连接池大小（可选），默认为 10
                - max_overflow: 连接池溢出限制（可选），默认为 20
                - pool_pre_ping: 连接前检查（可选），默认为 True
                - pool_recycle: 连接回收时间（秒，可选），默认为 3600
        
        示例:
            # 默认 SQLite 配置
            config = MagicDatabaseConfig()
            
            # 自定义 SQLite 路径
            config = MagicDatabaseConfig(
                DatabaseType.SQLITE,
                path="./myapp/custom.db",
                echo=True
            )
            
            # PostgreSQL 配置
            config = MagicDatabaseConfig(
                DatabaseType.POSTGRESQL,
                host="localhost",
                port=5432,
                user="magic_user",
                password="secure_pass",
                database="magic_db"
            )
        """
        self.db_type = db_type
        """数据库类型"""
        
        self.kwargs = kwargs
        """连接参数字典"""
        
        self._engine_options_cache = None
        """引擎选项缓存，避免重复计算"""
        
        if db_type == DatabaseType.SQLITE:        
            # 本地数据库路径，服务于 sqlite
            self.db_path = self._get_sqlite_path()
            """SQLite 数据库文件路径（仅 SQLite 类型有效）"""
        else:
            self.db_path = None
    
    def get_connection_string(self) -> str:
        """统一构建连接字符串
        
        根据数据库类型调用对应的构建方法，返回符合 SQLAlchemy 格式的连接字符串。
        
        返回:
            str: 数据库连接字符串
            
        异常:
            ValueError: 当数据库类型不支持时抛出
        """
        if self.db_type == DatabaseType.SQLITE:
            return self._build_sqlite()
        elif self.db_type == DatabaseType.POSTGRESQL:
            return self._build_postgresql()
        elif self.db_type == DatabaseType.MYSQL:
            return self._build_mysql()
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")
    
    def _get_sqlite_path(self) -> str:
        """获取 SQLite 数据库路径
        
        处理 SQLite 数据库文件路径的逻辑：
        1. 如果用户未指定 path 参数，使用默认文件名并放在 MAGIC_DATA_DIR 下
        2. 如果用户指定了 path 参数：
           - 绝对路径：直接使用
           - 相对路径：相对于当前工作目录
        3. 自动创建目标目录（如果不存在）
        
        返回:
            str: SQLite 数据库文件的完整路径字符串
        """
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
        """构建 SQLite 连接字符串
        
        返回:
            str: SQLite 连接字符串，格式如 "sqlite:///path/to/database.db"
        """
        return f"sqlite:///{self.db_path}"
    
    def _build_postgresql(self) -> str:
        """构建 PostgreSQL 连接字符串
        
        返回:
            str: PostgreSQL 连接字符串，格式如 "postgresql://user:pass@host:port/database"
        """
        host = self.kwargs.get("host", "localhost")
        port = self.kwargs.get("port", 5432)
        user = self.kwargs.get("user", "")
        password = self.kwargs.get("password", "")
        database = self.kwargs.get("database", "magic")
        
        auth = f"{user}:{password}@" if user and password else f"{user}@" if user else ""
        return f"postgresql://{auth}{host}:{port}/{database}"
    
    def _build_mysql(self) -> str:
        """构建 MySQL 连接字符串
        
        使用 PyMySQL 驱动，返回格式为 "mysql+pymysql://..."
        
        返回:
            str: MySQL 连接字符串，格式如 "mysql+pymysql://user:pass@host:port/database"
        """
        host = self.kwargs.get("host", "localhost")
        port = self.kwargs.get("port", 3306)
        user = self.kwargs.get("user", "")
        password = self.kwargs.get("password", "")
        database = self.kwargs.get("database", "magic")
        
        auth = f"{user}:{password}@" if user and password else f"{user}@" if user else ""
        return f"mysql+pymysql://{auth}{host}:{port}/{database}"
    
    def get_engine_options(self) -> Dict[str, Any]:
        """获取引擎选项
        
        返回 SQLAlchemy 引擎初始化参数，包括连接池配置和日志设置。
        结果会被缓存以提高性能。
        
        SQLite 特殊处理:
            自动添加 connect_args = {"check_same_thread": False} 以支持多线程访问
        
        返回:
            Dict[str, Any]: 引擎选项字典，包含以下配置：
                - echo: 是否打印 SQL 日志
                - pool_size: 连接池大小
                - max_overflow: 连接池溢出限制
                - pool_pre_ping: 连接前是否检查可用性
                - pool_recycle: 连接回收时间（秒）
                - connect_args: 连接参数（仅 SQLite）
        """
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
        """获取数据目录
        
        仅 SQLite 数据库支持此方法，返回默认数据存储目录。
        
        返回:
            Path: Magic 默认数据目录路径对象
            
        异常:
            RuntimeError: 当数据库类型不是 SQLite 时抛出
        """
        if self.db_type != DatabaseType.SQLITE:
            raise RuntimeError("Data directory only available for SQLite")
        return self.MAGIC_DATA_DIR
    
    def get_db_path(self) -> str:
        """获取数据库文件路径
        
        返回:
            str: 数据库文件的完整路径字符串（仅 SQLite 类型有效）
        """
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