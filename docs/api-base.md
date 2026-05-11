# `magic_base`

## Table of Contents

- 🅼 [magic\_base](#magic_base)
- 🅼 [magic\_base\.config](#magic_base-config)
- 🅼 [magic\_base\.config\.base\_config](#magic_base-config-base_config)
- 🅼 [magic\_base\.crypto](#magic_base-crypto)
- 🅼 [magic\_base\.crypto\.base\_cert](#magic_base-crypto-base_cert)
- 🅼 [magic\_base\.crypto\.base\_crypto](#magic_base-crypto-base_crypto)
- 🅼 [magic\_base\.data\_access](#magic_base-data_access)
- 🅼 [magic\_base\.data\_access\.config](#magic_base-data_access-config)
- 🅼 [magic\_base\.data\_access\.config\.base\_database\_config](#magic_base-data_access-config-base_database_config)
- 🅼 [magic\_base\.data\_access\.manager](#magic_base-data_access-manager)
- 🅼 [magic\_base\.data\_access\.manager\.base\_database\_manager](#magic_base-data_access-manager-base_database_manager)
- 🅼 [magic\_base\.data\_access\.model](#magic_base-data_access-model)
- 🅼 [magic\_base\.data\_access\.model\.base\_entity](#magic_base-data_access-model-base_entity)
- 🅼 [magic\_base\.data\_access\.repository](#magic_base-data_access-repository)
- 🅼 [magic\_base\.data\_access\.repository\.base\_repository](#magic_base-data_access-repository-base_repository)
- 🅼 [magic\_base\.data\_access\.repository\.base\_repository\_core\_mixin](#magic_base-data_access-repository-base_repository_core_mixin)
- 🅼 [magic\_base\.data\_access\.repository\.base\_repository\_cud\_mixin](#magic_base-data_access-repository-base_repository_cud_mixin)
- 🅼 [magic\_base\.data\_access\.repository\.base\_repository\_query\_mixin](#magic_base-data_access-repository-base_repository_query_mixin)
- 🅼 [magic\_base\.data\_access\.repository\.base\_sqlalchemy\_repository](#magic_base-data_access-repository-base_sqlalchemy_repository)
- 🅼 [magic\_base\.data\_access\.service](#magic_base-data_access-service)
- 🅼 [magic\_base\.data\_access\.service\.base\_service](#magic_base-data_access-service-base_service)
- 🅼 [magic\_base\.data\_access\.service\.base\_service\_core\_mixin](#magic_base-data_access-service-base_service_core_mixin)
- 🅼 [magic\_base\.data\_access\.service\.base\_service\_cud\_mixin](#magic_base-data_access-service-base_service_cud_mixin)
- 🅼 [magic\_base\.data\_access\.service\.base\_service\_query\_mixin](#magic_base-data_access-service-base_service_query_mixin)
- 🅼 [magic\_base\.data\_access\.util](#magic_base-data_access-util)
- 🅼 [magic\_base\.data\_access\.util\.base\_data\_command](#magic_base-data_access-util-base_data_command)
- 🅼 [magic\_base\.data\_access\.util\.base\_db\_command](#magic_base-data_access-util-base_db_command)
- 🅼 [magic\_base\.data\_access\.util\.base\_db\_table\_util](#magic_base-data_access-util-base_db_table_util)
- 🅼 [magic\_base\.data\_access\.util\.base\_db\_util](#magic_base-data_access-util-base_db_util)
- 🅼 [magic\_base\.data\_access\.util\.base\_type\_converter](#magic_base-data_access-util-base_type_converter)
- 🅼 [magic\_base\.detector](#magic_base-detector)
- 🅼 [magic\_base\.detector\.base\_detector](#magic_base-detector-base_detector)
- 🅼 [magic\_base\.detector\.base\_hardware\_define](#magic_base-detector-base_hardware_define)
- 🅼 [magic\_base\.detector\.base\_hardware\_result](#magic_base-detector-base_hardware_result)
- 🅼 [magic\_base\.exceptions](#magic_base-exceptions)
- 🅼 [magic\_base\.exceptions\.base\_exceptions](#magic_base-exceptions-base_exceptions)
- 🅼 [magic\_base\.platform](#magic_base-platform)
- 🅼 [magic\_base\.platform\.base\_platform\_adapter](#magic_base-platform-base_platform_adapter)
- 🅼 [magic\_base\.types](#magic_base-types)
- 🅼 [magic\_base\.types\.base\_types](#magic_base-types-base_types)
- 🅼 [magic\_base\.utils](#magic_base-utils)
- 🅼 [magic\_base\.utils\.base\_csv\_validator](#magic_base-utils-base_csv_validator)

<a name="magic_base"></a>
## 🅼 magic\_base

- **[Exports](#magic_base-exports)**

<a name="magic_base-exports"></a>
### Exports

- 🅼 [`ApplicationContext`](#magic_base-ApplicationContext)
- 🅼 [`BaseConfig`](#magic_base-BaseConfig)
- 🅼 [`BaseDatabaseConfig`](#magic_base-BaseDatabaseConfig)
- 🅼 [`MagicDatabaseConfig`](#magic_base-MagicDatabaseConfig)
- 🅼 [`BaseDatabaseManager`](#magic_base-BaseDatabaseManager)
- 🅼 [`MagicDatabaseManager`](#magic_base-MagicDatabaseManager)
- 🅼 [`Base`](#magic_base-Base)
- 🅼 [`BaseEntity`](#magic_base-BaseEntity)
- 🅼 [`MagicBaseEntity`](#magic_base-MagicBaseEntity)
- 🅼 [`BaseRepository`](#magic_base-BaseRepository)
- 🅼 [`MagicBaseRepository`](#magic_base-MagicBaseRepository)
- 🅼 [`BaseService`](#magic_base-BaseService)
- 🅼 [`MagicBaseService`](#magic_base-MagicBaseService)
- 🅼 [`CSVValidator`](#magic_base-CSVValidator)
<a name="magic_base-config"></a>
## 🅼 magic\_base\.config
<a name="magic_base-config-base_config"></a>
## 🅼 magic\_base\.config\.base\_config

配置管理基类

- **Classes:**
  - 🅲 [BaseConfig](#magic_base-config-base_config-BaseConfig)

### Classes

<a name="magic_base-config-base_config-BaseConfig"></a>
### 🅲 magic\_base\.config\.base\_config\.BaseConfig

```python
class BaseConfig(ABC):
```

配置管理基类

**Functions:**

<a name="magic_base-config-base_config-BaseConfig-get"></a>
#### 🅵 magic\_base\.config\.base\_config\.BaseConfig\.get

```python
def get(self, key: str, default: Any = None) -> Any:
```

获取配置值
<a name="magic_base-config-base_config-BaseConfig-set"></a>
#### 🅵 magic\_base\.config\.base\_config\.BaseConfig\.set

```python
def set(self, key: str, value: Any) -> None:
```

设置配置值
<a name="magic_base-config-base_config-BaseConfig-load"></a>
#### 🅵 magic\_base\.config\.base\_config\.BaseConfig\.load

```python
def load(self) -> Dict[str, Any]:
```

加载配置
<a name="magic_base-config-base_config-BaseConfig-save"></a>
#### 🅵 magic\_base\.config\.base\_config\.BaseConfig\.save

```python
def save(self) -> bool:
```

保存配置
<a name="magic_base-config-base_config-BaseConfig-reload"></a>
#### 🅵 magic\_base\.config\.base\_config\.BaseConfig\.reload

```python
def reload(self) -> None:
```

重新加载配置
<a name="magic_base-crypto"></a>
## 🅼 magic\_base\.crypto
<a name="magic_base-crypto-base_cert"></a>
## 🅼 magic\_base\.crypto\.base\_cert

证书验证基类

- **Classes:**
  - 🅲 [CertValidatorBase](#magic_base-crypto-base_cert-CertValidatorBase)

### Classes

<a name="magic_base-crypto-base_cert-CertValidatorBase"></a>
### 🅲 magic\_base\.crypto\.base\_cert\.CertValidatorBase

```python
class CertValidatorBase(ABC):
```

证书验证器基类

**Functions:**

<a name="magic_base-crypto-base_cert-CertValidatorBase-verify_signature"></a>
#### 🅵 magic\_base\.crypto\.base\_cert\.CertValidatorBase\.verify\_signature

```python
def verify_signature(self, data: bytes, signature: bytes, cert_path: str) -> bool:
```

验证签名
<a name="magic_base-crypto-base_cert-CertValidatorBase-get_cert_info"></a>
#### 🅵 magic\_base\.crypto\.base\_cert\.CertValidatorBase\.get\_cert\_info

```python
def get_cert_info(self, cert_path: str) -> Dict[str, Any]:
```

获取证书信息
<a name="magic_base-crypto-base_cert-CertValidatorBase-verify_chain"></a>
#### 🅵 magic\_base\.crypto\.base\_cert\.CertValidatorBase\.verify\_chain

```python
def verify_chain(self, cert_path: str, ca_bundle_path: str) -> bool:
```

验证证书链
<a name="magic_base-crypto-base_crypto"></a>
## 🅼 magic\_base\.crypto\.base\_crypto

加密基类

- **Classes:**
  - 🅲 [CryptoBase](#magic_base-crypto-base_crypto-CryptoBase)

### Classes

<a name="magic_base-crypto-base_crypto-CryptoBase"></a>
### 🅲 magic\_base\.crypto\.base\_crypto\.CryptoBase

```python
class CryptoBase(ABC):
```

加密工具基类

**Functions:**

<a name="magic_base-crypto-base_crypto-CryptoBase-encrypt"></a>
#### 🅵 magic\_base\.crypto\.base\_crypto\.CryptoBase\.encrypt

```python
def encrypt(self, data: bytes, key: bytes) -> bytes:
```

加密数据
<a name="magic_base-crypto-base_crypto-CryptoBase-decrypt"></a>
#### 🅵 magic\_base\.crypto\.base\_crypto\.CryptoBase\.decrypt

```python
def decrypt(self, data: bytes, key: bytes) -> bytes:
```

解密数据
<a name="magic_base-crypto-base_crypto-CryptoBase-hash"></a>
#### 🅵 magic\_base\.crypto\.base\_crypto\.CryptoBase\.hash

```python
def hash(self, data: bytes) -> str:
```

计算哈希值
<a name="magic_base-crypto-base_crypto-CryptoBase-generate_key"></a>
#### 🅵 magic\_base\.crypto\.base\_crypto\.CryptoBase\.generate\_key

```python
def generate_key(self) -> bytes:
```

生成密钥
<a name="magic_base-data_access"></a>
## 🅼 magic\_base\.data\_access
<a name="magic_base-data_access-config"></a>
## 🅼 magic\_base\.data\_access\.config
<a name="magic_base-data_access-config-base_database_config"></a>
## 🅼 magic\_base\.data\_access\.config\.base\_database\_config

数据库配置基类

- **Classes:**
  - 🅲 [DatabaseType](#magic_base-data_access-config-base_database_config-DatabaseType)
  - 🅲 [BaseDatabaseConfig](#magic_base-data_access-config-base_database_config-BaseDatabaseConfig)
  - 🅲 [MagicDatabaseConfig](#magic_base-data_access-config-base_database_config-MagicDatabaseConfig)

### Classes

<a name="magic_base-data_access-config-base_database_config-DatabaseType"></a>
### 🅲 magic\_base\.data\_access\.config\.base\_database\_config\.DatabaseType

```python
class DatabaseType(Enum):
```

数据库类型枚举

定义了支持的数据库类型，用于统一配置不同数据库的连接参数。

成员:
    SQLITE: SQLite 轻量级文件数据库
    POSTGRESQL: PostgreSQL 关系型数据库
    MYSQL: MySQL 关系型数据库
<a name="magic_base-data_access-config-base_database_config-BaseDatabaseConfig"></a>
### 🅲 magic\_base\.data\_access\.config\.base\_database\_config\.BaseDatabaseConfig

```python
class BaseDatabaseConfig(ABC):
```

数据库配置抽象基类

定义了数据库配置的标准接口，所有具体数据库配置类都应继承此类。
提供获取连接字符串和引擎选项的核心方法。

**Functions:**

<a name="magic_base-data_access-config-base_database_config-BaseDatabaseConfig-get_connection_string"></a>
#### 🅵 magic\_base\.data\_access\.config\.base\_database\_config\.BaseDatabaseConfig\.get\_connection\_string

```python
def get_connection_string(self) -> str:
```

获取数据库连接字符串

根据配置的数据库类型和参数，生成符合 SQLAlchemy 格式的连接字符串。

返回:
    str: 数据库连接字符串，格式如 "sqlite:///path/to/db\.db" 或
        "postgresql://user:pass@localhost:5432/dbname"
<a name="magic_base-data_access-config-base_database_config-BaseDatabaseConfig-get_engine_options"></a>
#### 🅵 magic\_base\.data\_access\.config\.base\_database\_config\.BaseDatabaseConfig\.get\_engine\_options

```python
def get_engine_options(self) -> Dict[str, Any]:
```

获取引擎选项

返回 SQLAlchemy 引擎初始化时所需的参数字典，包括连接池配置、日志设置等。

返回:
    Dict\[str, Any\]: 引擎选项字典，可直接传递给 SQLAlchemy create\_engine 函数
<a name="magic_base-data_access-config-base_database_config-BaseDatabaseConfig-get_db_path"></a>
#### 🅵 magic\_base\.data\_access\.config\.base\_database\_config\.BaseDatabaseConfig\.get\_db\_path

```python
def get_db_path(self) -> str:
```

获取数据库文件路径\(仅限于sqlite\)

返回 sqlite数据库文件路径。
<a name="magic_base-data_access-config-base_database_config-MagicDatabaseConfig"></a>
### 🅲 magic\_base\.data\_access\.config\.base\_database\_config\.MagicDatabaseConfig

```python
class MagicDatabaseConfig(BaseDatabaseConfig):
```

Magic 系列统一数据库配置

为 Magic 系列项目提供统一的数据库配置管理，支持 SQLite、PostgreSQL 和 MySQL。
自动处理数据库文件的目录创建、路径解析等细节。

设计原则:
    只做一件事：提供统一的数据库配置，不涉及业务逻辑。

类属性:
    MAGIC\_DATA\_DIR: Magic 默认数据存储目录，位于用户家目录下的 magic/data

**Functions:**

<a name="magic_base-data_access-config-base_database_config-MagicDatabaseConfig-__init__"></a>
#### 🅵 magic\_base\.data\_access\.config\.base\_database\_config\.MagicDatabaseConfig\.\_\_init\_\_

```python
def __init__(self, db_type: DatabaseType = DatabaseType.SQLITE, **kwargs):
```

初始化数据库配置

参数:
    db\_type: 数据库类型，默认为 SQLite。可选值见 DatabaseType 枚举
    \*\*kwargs: 连接参数，根据数据库类型不同而不同
    
不同数据库类型支持的 kwargs 参数:
    SQLite:
        - path: 数据库文件路径（可选），默认为 "magic\.db"
              可以是相对路径或绝对路径
        - echo: 是否打印 SQL 日志（可选），默认为 False
        - pool\_size: 连接池大小（可选），默认为 10
        - max\_overflow: 连接池溢出限制（可选），默认为 20
        - pool\_pre\_ping: 连接前检查（可选），默认为 True
        - pool\_recycle: 连接回收时间（秒，可选），默认为 3600
        
    PostgreSQL:
        - host: 数据库主机地址（可选），默认为 "localhost"
        - port: 数据库端口（可选），默认为 5432
        - user: 数据库用户名（可选），默认为空字符串
        - password: 数据库密码（可选），默认为空字符串
        - database: 数据库名称（可选），默认为 "magic"
        - echo: 是否打印 SQL 日志（可选），默认为 False
        - pool\_size: 连接池大小（可选），默认为 10
        - max\_overflow: 连接池溢出限制（可选），默认为 20
        - pool\_pre\_ping: 连接前检查（可选），默认为 True
        - pool\_recycle: 连接回收时间（秒，可选），默认为 3600
        
    MySQL:
        - host: 数据库主机地址（可选），默认为 "localhost"
        - port: 数据库端口（可选），默认为 3306
        - user: 数据库用户名（可选），默认为空字符串
        - password: 数据库密码（可选），默认为空字符串
        - database: 数据库名称（可选），默认为 "magic"
        - echo: 是否打印 SQL 日志（可选），默认为 False
        - pool\_size: 连接池大小（可选），默认为 10
        - max\_overflow: 连接池溢出限制（可选），默认为 20
        - pool\_pre\_ping: 连接前检查（可选），默认为 True
        - pool\_recycle: 连接回收时间（秒，可选），默认为 3600

示例:
    \# 默认 SQLite 配置
    config = MagicDatabaseConfig\(\)
    
    \# 自定义 SQLite 路径
    config = MagicDatabaseConfig\(
        DatabaseType\.SQLITE,
        path="\./myapp/custom\.db",
        echo=True
    \)
    
    \# PostgreSQL 配置
    config = MagicDatabaseConfig\(
        DatabaseType\.POSTGRESQL,
        host="localhost",
        port=5432,
        user="magic\_user",
        password="secure\_pass",
        database="magic\_db"
    \)
<a name="magic_base-data_access-config-base_database_config-MagicDatabaseConfig-get_connection_string"></a>
#### 🅵 magic\_base\.data\_access\.config\.base\_database\_config\.MagicDatabaseConfig\.get\_connection\_string

```python
def get_connection_string(self) -> str:
```

统一构建连接字符串

根据数据库类型调用对应的构建方法，返回符合 SQLAlchemy 格式的连接字符串。

返回:
    str: 数据库连接字符串
    
异常:
    ValueError: 当数据库类型不支持时抛出
<a name="magic_base-data_access-config-base_database_config-MagicDatabaseConfig-get_engine_options"></a>
#### 🅵 magic\_base\.data\_access\.config\.base\_database\_config\.MagicDatabaseConfig\.get\_engine\_options

```python
def get_engine_options(self) -> Dict[str, Any]:
```

获取引擎选项

返回 SQLAlchemy 引擎初始化参数，包括连接池配置和日志设置。
结果会被缓存以提高性能。

SQLite 特殊处理:
    自动添加 connect\_args = \{"check\_same\_thread": False\} 以支持多线程访问

返回:
    Dict\[str, Any\]: 引擎选项字典，包含以下配置：
        - echo: 是否打印 SQL 日志
        - pool\_size: 连接池大小
        - max\_overflow: 连接池溢出限制
        - pool\_pre\_ping: 连接前是否检查可用性
        - pool\_recycle: 连接回收时间（秒）
        - connect\_args: 连接参数（仅 SQLite）
<a name="magic_base-data_access-config-base_database_config-MagicDatabaseConfig-get_data_dir"></a>
#### 🅵 magic\_base\.data\_access\.config\.base\_database\_config\.MagicDatabaseConfig\.get\_data\_dir

```python
def get_data_dir(self) -> Path:
```

获取数据目录

仅 SQLite 数据库支持此方法，返回默认数据存储目录。

返回:
    Path: Magic 默认数据目录路径对象
    
异常:
    RuntimeError: 当数据库类型不是 SQLite 时抛出
<a name="magic_base-data_access-config-base_database_config-MagicDatabaseConfig-get_db_path"></a>
#### 🅵 magic\_base\.data\_access\.config\.base\_database\_config\.MagicDatabaseConfig\.get\_db\_path

```python
def get_db_path(self) -> str:
```

获取数据库文件路径

返回:
    str: 数据库文件的完整路径字符串（仅 SQLite 类型有效）
<a name="magic_base-data_access-manager"></a>
## 🅼 magic\_base\.data\_access\.manager
<a name="magic_base-data_access-manager-base_database_manager"></a>
## 🅼 magic\_base\.data\_access\.manager\.base\_database\_manager

数据库管理器基类

- **Classes:**
  - 🅲 [BaseDatabaseManager](#magic_base-data_access-manager-base_database_manager-BaseDatabaseManager)
  - 🅲 [MagicDatabaseManager](#magic_base-data_access-manager-base_database_manager-MagicDatabaseManager)

### Classes

<a name="magic_base-data_access-manager-base_database_manager-BaseDatabaseManager"></a>
### 🅲 magic\_base\.data\_access\.manager\.base\_database\_manager\.BaseDatabaseManager

```python
class BaseDatabaseManager(ABC):
```

数据库管理器基类

提供统一的数据库会话管理和引擎生命周期控制，具体模块继承此类实现自己的数据库管理。

功能特性:
    - 延迟初始化数据库引擎，避免不必要的资源消耗
    - 提供上下文管理器风格的会话管理，自动处理提交和回滚
    - 支持手动管理会话模式
    - 提供优雅的引擎关闭机制

设计原则:
    子类必须实现 init\_database 方法，用于具体的数据库表结构初始化。

使用示例:
    \# 创建配置
    config = MagicDatabaseConfig\(DatabaseType\.SQLITE\)
    
    \# 创建管理器
    db\_manager = MyDatabaseManager\(config\)
    
    \# 使用上下文管理器自动管理会话
    with db\_manager\.session\(\) as session:
        result = session\.query\(User\)\.filter\_by\(id=1\)\.first\(\)
    
    \# 手动管理会话
    session = db\_manager\.get\_session\(\)
    try:
        session\.add\(new\_user\)
        session\.commit\(\)
    finally:
        session\.close\(\)

**Functions:**

<a name="magic_base-data_access-manager-base_database_manager-BaseDatabaseManager-__init__"></a>
#### 🅵 magic\_base\.data\_access\.manager\.base\_database\_manager\.BaseDatabaseManager\.\_\_init\_\_

```python
def __init__(self, config: BaseDatabaseConfig):
```

初始化数据库管理器

参数:
    config: 数据库配置对象，必须继承自 BaseDatabaseConfig
<a name="magic_base-data_access-manager-base_database_manager-BaseDatabaseManager-engine"></a>
#### 🅵 magic\_base\.data\_access\.manager\.base\_database\_manager\.BaseDatabaseManager\.engine

```python
def engine(self) -> Engine:
```

获取数据库引擎（延迟初始化）

当第一次访问此属性时，会根据配置创建数据库引擎。
引擎创建后会被缓存，后续访问直接返回缓存的实例。

返回:
    Engine: SQLAlchemy 数据库引擎对象
<a name="magic_base-data_access-manager-base_database_manager-BaseDatabaseManager-SessionLocal"></a>
#### 🅵 magic\_base\.data\_access\.manager\.base\_database\_manager\.BaseDatabaseManager\.SessionLocal

```python
def SessionLocal(self) -> sessionmaker:
```

获取会话工厂

当第一次访问此属性时，会基于数据库引擎创建会话工厂。
会话工厂创建后会被缓存，后续访问直接返回缓存的实例。

返回:
    sessionmaker: SQLAlchemy 会话工厂，用于创建新的会话对象
<a name="magic_base-data_access-manager-base_database_manager-BaseDatabaseManager-session"></a>
#### 🅵 magic\_base\.data\_access\.manager\.base\_database\_manager\.BaseDatabaseManager\.session

```python
def session(self) -> Generator[Session, None, None]:
```

获取数据库会话（上下文管理器）

使用上下文管理器自动管理会话的生命周期：
    - 成功执行时自动提交事务
    - 发生异常时自动回滚事务
    - 无论成功与否都会关闭会话

这是推荐的会话使用方式，可以避免手动管理事务和资源泄露。

产生:
    Session: 数据库会话对象
    
示例:
    with db\_manager\.session\(\) as session:
        \# 数据库操作
        user = session\.query\(User\)\.get\(1\)
        \# 退出上下文时自动提交
<a name="magic_base-data_access-manager-base_database_manager-BaseDatabaseManager-get_session"></a>
#### 🅵 magic\_base\.data\_access\.manager\.base\_database\_manager\.BaseDatabaseManager\.get\_session

```python
def get_session(self) -> Session:
```

获取数据库会话（手动管理）

返回一个新的会话对象，调用者负责管理会话的生命周期：
    - 必须手动调用 commit\(\) 提交事务
    - 必须手动调用 close\(\) 关闭会话
    - 发生异常时需要手动调用 rollback\(\)

返回:
    Session: 数据库会话对象
    
示例:
    session = db\_manager\.get\_session\(\)
    try:
        session\.add\(new\_user\)
        session\.commit\(\)
    except Exception as e:
        session\.rollback\(\)
        raise
    finally:
        session\.close\(\)
<a name="magic_base-data_access-manager-base_database_manager-BaseDatabaseManager-close"></a>
#### 🅵 magic\_base\.data\_access\.manager\.base\_database\_manager\.BaseDatabaseManager\.close

```python
def close(self) -> None:
```

关闭数据库引擎

释放数据库引擎占用的所有资源，包括连接池中的所有连接。
关闭后，可以重新调用 engine 属性重新创建引擎。

使用场景:
    - 应用关闭时的清理工作
    - 单元测试的清理阶段
    - 需要重新配置数据库连接时
<a name="magic_base-data_access-manager-base_database_manager-BaseDatabaseManager-__enter__"></a>
#### 🅵 magic\_base\.data\_access\.manager\.base\_database\_manager\.BaseDatabaseManager\.\_\_enter\_\_

```python
def __enter__(self):
```

上下文管理器入口

支持 with 语句，返回自身实例。

返回:
    BaseDatabaseManager: 管理器实例
<a name="magic_base-data_access-manager-base_database_manager-BaseDatabaseManager-__exit__"></a>
#### 🅵 magic\_base\.data\_access\.manager\.base\_database\_manager\.BaseDatabaseManager\.\_\_exit\_\_

```python
def __exit__(self, exc_type, exc_val, exc_tb):
```

上下文管理器出口

自动调用 close\(\) 方法释放数据库资源。

参数:
    exc\_type: 异常类型
    exc\_val: 异常值
    exc\_tb: 异常追踪信息
<a name="magic_base-data_access-manager-base_database_manager-BaseDatabaseManager-init_database"></a>
#### 🅵 magic\_base\.data\_access\.manager\.base\_database\_manager\.BaseDatabaseManager\.init\_database

```python
def init_database(self, drop_first: bool = False):
```

初始化数据库（子类必须实现）

创建或更新数据库表结构。子类应根据自己的 ORM 模型实现此方法。

参数:
    drop\_first: 是否先删除现有表，设置为 True 会清空所有现有数据，请谨慎使用
    
异常:
    NotImplementedError: 子类未实现此方法时抛出
    
示例:
    def init\_database\(self, drop\_first: bool = False\):
        if drop\_first:
            Base\.metadata\.drop\_all\(bind=self\.engine\)
        Base\.metadata\.create\_all\(bind=self\.engine\)
<a name="magic_base-data_access-manager-base_database_manager-MagicDatabaseManager"></a>
### 🅲 magic\_base\.data\_access\.manager\.base\_database\_manager\.MagicDatabaseManager

```python
class MagicDatabaseManager(BaseDatabaseManager):
```

共享数据库管理器

为 Magic 系列项目提供的通用数据库管理器实现。
提供便捷的表初始化方法，子类只需提供 SQLAlchemy Base 即可快速初始化数据库。

使用场景:
    - 标准的 CRUD 应用
    - 简单的数据库访问层
    - 快速原型开发

使用示例:
    \# 创建配置
    config = MagicDatabaseConfig\(\)
    
    \# 创建管理器并设置 Base
    db\_manager = MagicDatabaseManager\(config\)
    db\_manager\.set\_base\(Base\)  \# Base 是 SQLAlchemy 声明式基类
    
    \# 初始化数据库
    db\_manager\.init\_database\(\)
    
    \# 使用会话
    with db\_manager\.session\(\) as session:
        users = session\.query\(User\)\.all\(\)

**Functions:**

<a name="magic_base-data_access-manager-base_database_manager-MagicDatabaseManager-__init__"></a>
#### 🅵 magic\_base\.data\_access\.manager\.base\_database\_manager\.MagicDatabaseManager\.\_\_init\_\_

```python
def __init__(self, config: MagicDatabaseConfig, base = None):
```

初始化 Magic 数据库管理器

参数:
    config: Magic 数据库配置对象
    base: SQLAlchemy 声明式基类，可选，可以在初始化后通过 set\_base\(\) 设置
<a name="magic_base-data_access-manager-base_database_manager-MagicDatabaseManager-set_base"></a>
#### 🅵 magic\_base\.data\_access\.manager\.base\_database\_manager\.MagicDatabaseManager\.set\_base

```python
def set_base(self, base):
```

设置 SQLAlchemy Base（延迟设置）

允许在创建管理器实例后单独设置 Base 对象，便于某些需要延迟绑定的场景。

参数:
    base: SQLAlchemy 声明式基类，必须包含 metadata 属性
    
使用场景:
    \# 循环导入问题的解决方案
    db\_manager = MagicDatabaseManager\(config\)
    \# 延迟导入 Base 避免循环依赖
    from myapp\.models import Base
    db\_manager\.set\_base\(Base\)
<a name="magic_base-data_access-manager-base_database_manager-MagicDatabaseManager-init_database"></a>
#### 🅵 magic\_base\.data\_access\.manager\.base\_database\_manager\.MagicDatabaseManager\.init\_database

```python
def init_database(self, drop_first: bool = False):
```

初始化数据库表

根据 SQLAlchemy Base 中定义的模型，创建所有数据库表。

参数:
    drop\_first: 是否先删除现有表，默认为 False
              设置为 True 会删除所有现有表和数据，请仅在开发和测试环境中使用
    
异常:
    ValueError: 当 Base 尚未设置时抛出
    
警告:
    drop\_first=True 会删除所有现有数据，生产环境请勿使用！
    
示例:
    \# 正常初始化（保持现有数据）
    db\_manager\.init\_database\(\)
    
    \# 重新初始化（清空所有数据）
    db\_manager\.init\_database\(drop\_first=True\)
<a name="magic_base-data_access-model"></a>
## 🅼 magic\_base\.data\_access\.model
<a name="magic_base-data_access-model-base_entity"></a>
## 🅼 magic\_base\.data\_access\.model\.base\_entity

ORM 基类 - 所有数据模型继承此基类

- **Constants:**
  - 🆅 [T](#magic_base-data_access-model-base_entity-T)
- **Classes:**
  - 🅲 [BaseEntity](#magic_base-data_access-model-base_entity-BaseEntity)
  - 🅲 [MagicBaseEntity](#magic_base-data_access-model-base_entity-MagicBaseEntity)

### Constants

<a name="magic_base-data_access-model-base_entity-T"></a>
### 🆅 magic\_base\.data\_access\.model\.base\_entity\.T

```python
T = TypeVar('T', bound='BaseEntity')
```

### Classes

<a name="magic_base-data_access-model-base_entity-BaseEntity"></a>
### 🅲 magic\_base\.data\_access\.model\.base\_entity\.BaseEntity

```python
class BaseEntity:
```

ORM 模型抽象基类

所有业务模型都应继承此类，提供基础的模型转换和验证功能。
具体的 ORM 实现（如 SQLAlchemy Base）由业务模块自己创建。

设计理念:
    - 与具体的 ORM 框架解耦，提供纯 Python 层面的基础功能
    - 子类需要自行创建 ORM Base 并继承此类
    - 提供字典序列化、反序列化和数据验证等通用方法

主要功能:
    - to\_dict\(\): 模型转字典
    - from\_dict\(\): 字典更新模型
    - validate\(\): 数据验证接口
    - get\_table\_name\(\): 获取表名
    - \_\_repr\_\_\(\): 友好的字符串表示

**Functions:**

<a name="magic_base-data_access-model-base_entity-BaseEntity-to_dict"></a>
#### 🅵 magic\_base\.data\_access\.model\.base\_entity\.BaseEntity\.to\_dict

```python
def to_dict(self) -> Dict[str, Any]:
```

将模型转换为字典

遍历模型实例的所有属性，过滤掉以下划线开头的私有属性，
返回一个包含所有公开属性的字典。

**Returns:**

- `Dict[str, Any]`: 字典格式的模型数据，键为属性名，值为属性值
<a name="magic_base-data_access-model-base_entity-BaseEntity-from_dict"></a>
#### 🅵 magic\_base\.data\_access\.model\.base\_entity\.BaseEntity\.from\_dict

```python
def from_dict(self: T, data: Dict[str, Any]) -> T:
```

从字典更新模型属性

遍历字典中的每一项，如果模型存在同名属性则更新其值。
不会添加模型中不存在的属性。

参数:
    data: 字典数据，键为属性名，值为要设置的值
    
返回:
    self: 返回当前实例，支持链式调用
<a name="magic_base-data_access-model-base_entity-BaseEntity-validate"></a>
#### 🅵 magic\_base\.data\_access\.model\.base\_entity\.BaseEntity\.validate

```python
def validate(self) -> bool:
```

验证模型数据

子类可以重写此方法实现自定义验证逻辑。
基类默认实现返回 True，表示总是通过验证。

使用场景:
    - 在保存前验证必填字段
    - 检查字段值格式（如邮箱、手机号）
    - 验证业务规则（如年龄范围、金额非负）
    
返回:
    bool: True 表示验证通过，False 表示验证失败
<a name="magic_base-data_access-model-base_entity-BaseEntity-get_table_name"></a>
#### 🅵 magic\_base\.data\_access\.model\.base\_entity\.BaseEntity\.get\_table\_name

```python
def get_table_name(cls) -> str:
```

获取表名

优先返回类属性 \_\_tablename\_\_ 定义的表名，
如果没有定义则返回类名的小写形式。

子类可以通过在类中定义 \_\_tablename\_\_ 属性来显式指定表名。

返回:
    str: 表名
<a name="magic_base-data_access-model-base_entity-BaseEntity-__repr__"></a>
#### 🅵 magic\_base\.data\_access\.model\.base\_entity\.BaseEntity\.\_\_repr\_\_

```python
def __repr__(self) -> str:
```

友好的字符串表示

格式为 "ClassName\(attr1=value1, attr2=value2, \.\.\.\)"
为了方便阅读，每个属性值只显示前50个字符，超长部分用 "\.\.\." 替代。

返回:
    str: 模型的字符串表示
<a name="magic_base-data_access-model-base_entity-MagicBaseEntity"></a>
### 🅲 magic\_base\.data\_access\.model\.base\_entity\.MagicBaseEntity

```python
class MagicBaseEntity(Base):
```

所有 ORM 模型的抽象基类

提供通用的字段、方法序列化功能。
继承自 SQLAlchemy 的声明式基类，并混合了 BaseModel 的功能。

类属性:
    \_\_abstract\_\_: 标记为抽象类，不会在数据库中创建对应的表
    
通用字段:
    id: 自增主键，所有表的标准标识字段
    is\_active: 是否激活状态，带索引便于查询
    created\_at: 创建时间，自动设置为插入时的时间戳
    updated\_at: 更新时间，更新时自动修改
    deleted\_at: 软删除时间戳，nullable=True 表示未删除

使用场景:
    作为所有 ORM 模型的基类，提供标准字段和通用方法。
<a name="magic_base-data_access-repository"></a>
## 🅼 magic\_base\.data\_access\.repository
<a name="magic_base-data_access-repository-base_repository"></a>
## 🅼 magic\_base\.data\_access\.repository\.base\_repository

- **Constants:**
  - 🆅 [T](#magic_base-data_access-repository-base_repository-T)
- **Classes:**
  - 🅲 [BaseRepository](#magic_base-data_access-repository-base_repository-BaseRepository)
  - 🅲 [MagicBaseRepository](#magic_base-data_access-repository-base_repository-MagicBaseRepository)

### Constants

<a name="magic_base-data_access-repository-base_repository-T"></a>
### 🆅 magic\_base\.data\_access\.repository\.base\_repository\.T

```python
T = TypeVar('T')
```

### Classes

<a name="magic_base-data_access-repository-base_repository-BaseRepository"></a>
### 🅲 magic\_base\.data\_access\.repository\.base\_repository\.BaseRepository

```python
class BaseRepository(CUDRepositoryMixin[T], QueryRepositoryMixin[T]):
```

混合 Repository 基类（抽象基类，只能通过继承使用）

组合 CUD 和 Query 两个 Mixin，提供完整的 CRUD 操作。

- CUD \(创建/更新/删除\): 使用 ORM
- R \(查询\): 使用原生 SQL

设计理念:
    采用混合策略，发挥各自优势：
    - 写操作使用 ORM：获得对象关系映射的便利性、自动事务管理、关联关系处理
    - 读操作使用原生 SQL：获得更好的性能、更灵活的查询、复杂 JOIN 支持

继承关系:
    BaseRepository
    ├── CUDRepositoryMixin \(ORM 写操作\)
    │   └── RepositoryCoreMixin \(核心基础设施\)
    └── QueryRepositoryMixin \(SQL 读操作\)
        └── RepositoryCoreMixin \(核心基础设施\)

使用方式：
    class UserRepository\(BaseRepository\[User\]\):
        '''用户数据仓库'''
        pass
    
    \# 实例化
    repo = UserRepository\(session\)  \# 使用现有会话
    repo = UserRepository\(\)          \# 自动获取会话
    
    \# 执行操作
    user = repo\.create\(name="Alice", email="alice@example\.com"\)
    user\_dict = repo\.get\_by\_id\(user\.id\)
    users = repo\.find\(conditions=\{'is\_active': True\}\)

设计优势:
    - 职责分离：核心、CUD、查询各司其职，代码清晰易维护
    - 灵活组合：可以根据需要只继承部分 Mixin（如只读 Repository）
    - 易于测试：每个 Mixin 可以独立测试，降低测试复杂度
    - 代码复用：不同的 Repository 可以灵活组合不同的能力
    - 类型安全：完整的泛型支持，IDE 可提供准确的代码补全

注意事项:
    1\. 此类为抽象基类，不能直接实例化，必须通过子类继承
    2\. 子类必须指定泛型类型 T（具体的 ORM 模型类）
    3\. 泛型类型会在实例化时自动提取，无需手动设置

示例:
    \# 定义模型
    class User\(Base\):
        \_\_tablename\_\_ = 'users'
        id = Column\(Integer, primary\_key=True\)
        name = Column\(String\)
        email = Column\(String\)
    
    \# 定义 Repository
    class UserRepository\(BaseRepository\[User\]\):
        '''用户数据仓库'''
        
        def find\_by\_email\(self, email: str\) -\> Optional\[Dict\]:
            '''自定义查询方法'''
            return self\.find\_one\(\{'email': email\}\)
        
        def activate\_user\(self, user\_id: int\) -\> bool:
            '''自定义业务方法'''
            return self\.update\(user\_id, is\_active=True\)
    
    \# 使用 Repository
    repo = UserRepository\(\)
    
    \# 继承的基础方法
    user = repo\.create\(name="Bob", email="bob@example\.com"\)
    user\_dict = repo\.get\_by\_id\(user\.id\)
    
    \# 自定义方法
    user = repo\.find\_by\_email\("bob@example\.com"\)
    repo\.activate\_user\(user\['id'\]\)

**Functions:**

<a name="magic_base-data_access-repository-base_repository-BaseRepository-__new__"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\.BaseRepository\.\_\_new\_\_

```python
def __new__(cls, *args, **kwargs):
```

在子类实例化时自动提取泛型类型

拦截实例创建过程，确保抽象基类不能被直接实例化，
同时允许子类正常实例化。

执行流程:
    1\. 检查当前类是否为 BaseRepository 本身
    2\. 如果是，抛出 TypeError 禁止实例化
    3\. 如果不是（说明是子类），正常创建实例

参数:
    \*args: 位置参数
    \*\*kwargs: 关键字参数

返回:
    子类实例

异常:
    TypeError: 当尝试直接实例化 BaseRepository 时抛出

示例:
    \# 错误用法 - 会抛出 TypeError
    repo = BaseRepository\(\)
    
    \# 正确用法
    repo = UserRepository\(\)

注意:
    此方法只检查直接实例化 BaseRepository 的情况，
    子类实例化时会正常通过检查。
<a name="magic_base-data_access-repository-base_repository-BaseRepository-__init__"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\.BaseRepository\.\_\_init\_\_

```python
def __init__(self, session: Optional[Session] = None):
```

初始化 Repository

调用父类（CUDRepositoryMixin 和 QueryRepositoryMixin）的初始化方法，
设置数据库会话、模型类、表名等核心属性。

参数:
    session: 数据库会话（可选，如果不提供则自动从 db\_connection 获取）

示例:
    \# 使用自动会话管理
    repo = UserRepository\(\)
    
    \# 使用自定义会话
    from sqlalchemy\.orm import Session
    session = Session\(engine\)
    repo = UserRepository\(session\)

注意:
    session 采用延迟初始化策略，只有在首次使用时才会获取，
    这样可以避免在 Repository 创建时就依赖数据库连接。
<a name="magic_base-data_access-repository-base_repository-MagicBaseRepository"></a>
### 🅲 magic\_base\.data\_access\.repository\.base\_repository\.MagicBaseRepository

```python
class MagicBaseRepository(ABC, BaseRepository[T]):
```

Magic 系列基础 Repository 适配类

继承自 ABC（抽象基类）和 BaseRepository，为 Magic 系列项目提供统一的 Repository 基类。

设计目的:
    为 Magic 生态系统中的各个项目提供一致的 Repository 接口，
    便于代码复用和统一管理。

多重继承说明:
    - ABC: 来自 abc 模块的抽象基类，确保此类不能被直接实例化
    - BaseRepository: 提供完整的 CRUD 操作能力

使用方式:
    from magic\_base\.data\_access\.repository import MagicBaseRepository
    
    \# 基础用法
    class UserRepository\(MagicBaseRepository\[User\]\):
        '''用户数据仓库'''
        pass
    
    \# 可以添加自定义方法
    class ProductRepository\(MagicBaseRepository\[Product\]\):
        '''产品数据仓库'''
        
        def find\_by\_category\(self, category\_id: int\) -\> List\[Dict\]:
            '''根据分类查找产品'''
            return self\.find\(conditions=\{'category\_id': category\_id\}\)
        
        def find\_active\_products\(self\) -\> List\[Dict\]:
            '''查找激活的产品'''
            return self\.find\(conditions=\{'is\_active': True\}\)
    
    \# 只读 Repository（不需要 CUD 操作）
    class ReadOnlyRepository\(QueryRepositoryMixin\[ReadOnlyModel\]\):
        '''只读 Repository，没有 CUD 操作'''
        def find\_by\_name\(self, name: str\) -\> Optional\[Dict\]:
            return self\.find\_one\(\{'name': name\}\)

与 BaseRepository 的区别:
    - MagicBaseRepository 添加了 ABC 抽象标记
    - MagicBaseRepository 是 Magic 生态的统一接口
    - BaseRepository 是更通用的实现

注意:
    此类为抽象基类，通过 ABC 确保不能被直接实例化。
    必须通过子类继承并实例化子类。

示例:
    \# 定义模型
    from magic\_base\.data\_access\.model import MagicBaseModel
    
    class User\(MagicBaseModel\):
        \_\_tablename\_\_ = 'magic\_users'
        username = Column\(String\(50\), unique=True\)
        email = Column\(String\(100\), unique=True\)
    
    \# 定义 Repository
    class UserRepository\(MagicBaseRepository\[User\]\):
        '''Magic 用户仓库'''
        
        def find\_by\_username\(self, username: str\) -\> Optional\[Dict\]:
            '''根据用户名查找用户'''
            return self\.find\_one\(\{'username': username\}\)
        
        def exists\_by\_email\(self, email: str\) -\> bool:
            '''检查邮箱是否存在'''
            return self\.exists\(email=email\)
    
    \# 使用
    repo = UserRepository\(\)
    
    \# 创建用户
    user = repo\.create\(
        username='alice',
        email='alice@magic\.com',
        is\_active=True
    \)
    
    \# 查询用户
    user\_dict = repo\.find\_by\_username\('alice'\)
    print\(f"找到用户: \{user\_dict\['email'\]\}"\)
    
    \# 检查存在性
    if repo\.exists\_by\_email\('new@magic\.com'\):
        print\("邮箱已被注册"\)

扩展建议:
    可以根据项目需求，在 MagicBaseRepository 基础上添加更多通用方法，
    如批量导入、导出、缓存等。
<a name="magic_base-data_access-repository-base_repository_core_mixin"></a>
## 🅼 magic\_base\.data\_access\.repository\.base\_repository\_core\_mixin

- **Constants:**
  - 🆅 [T](#magic_base-data_access-repository-base_repository_core_mixin-T)
- **Classes:**
  - 🅲 [RepositoryCoreMixin](#magic_base-data_access-repository-base_repository_core_mixin-RepositoryCoreMixin)

### Constants

<a name="magic_base-data_access-repository-base_repository_core_mixin-T"></a>
### 🆅 magic\_base\.data\_access\.repository\.base\_repository\_core\_mixin\.T

```python
T = TypeVar('T')
```

### Classes

<a name="magic_base-data_access-repository-base_repository_core_mixin-RepositoryCoreMixin"></a>
### 🅲 magic\_base\.data\_access\.repository\.base\_repository\_core\_mixin\.RepositoryCoreMixin

```python
class RepositoryCoreMixin(Generic[T]):
```

Repository 核心 Mixin

提供 Repository 的基础设施：模型类提取、会话管理、表名推断等。
所有 Repository 类都应该继承此 Mixin。

设计理念:
    将 Repository 的核心功能提取到独立的 Mixin 中，便于其他 Mixin 类复用。
    负责处理泛型模型类的自动提取、数据库会话的延迟初始化、表名的智能推断。

泛型参数:
    T: ORM 模型类的类型

类属性:
    \_model\_class: 存储提取出的模型类
    \_session: 数据库会话实例（延迟初始化）
    \_table\_name: 推断出的数据库表名

使用方式:
    class MyRepository\(RepositoryCoreMixin\[User\]\):
        pass

**Functions:**

<a name="magic_base-data_access-repository-base_repository_core_mixin-RepositoryCoreMixin-__new__"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\_core\_mixin\.RepositoryCoreMixin\.\_\_new\_\_

```python
def __new__(cls, *args, **kwargs):
```

在子类实例化时自动提取泛型类型

拦截实例创建过程，在实例化前自动提取子类指定的泛型模型类。
确保每个子类都能正确地知道它要操作的模型类型。

参数:
    \*args: 位置参数
    \*\*kwargs: 关键字参数

返回:
    子类实例

注意:
    对于抽象基类（BaseRepository 和 RepositoryCoreMixin 本身），不进行提取，
    允许它们被正常实例化（虽然通常不会直接实例化）。
<a name="magic_base-data_access-repository-base_repository_core_mixin-RepositoryCoreMixin-__init__"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\_core\_mixin\.RepositoryCoreMixin\.\_\_init\_\_

```python
def __init__(self, session: Optional[Session] = None):
```

初始化 Repository 核心

负责设置数据库会话、提取表名等核心基础设施。

参数:
    session: 数据库会话（可选，如果不提供则自动从 db\_connection 获取）

异常:
    RuntimeError: 当模型类未正确初始化时抛出
<a name="magic_base-data_access-repository-base_repository_core_mixin-RepositoryCoreMixin-session"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\_core\_mixin\.RepositoryCoreMixin\.session

```python
def session(self) -> Session:
```

获取数据库会话

通过属性方式提供会话访问，内部调用 \_get\_session 实现延迟初始化。

返回:
    Session: 数据库会话对象

示例:
    repo = UserRepository\(\)
    session = repo\.session  \# 第一次访问时自动初始化
<a name="magic_base-data_access-repository-base_repository_core_mixin-RepositoryCoreMixin-model_class"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\_core\_mixin\.RepositoryCoreMixin\.model\_class

```python
def model_class(self) -> Type[T]:
```

获取模型类

返回子类指定的 ORM 模型类，用于创建实例和类型提示。

返回:
    Type\[T\]: ORM 模型类

示例:
    repo = UserRepository\(\)
    new\_user = repo\.model\_class\(name="Alice"\)
<a name="magic_base-data_access-repository-base_repository_core_mixin-RepositoryCoreMixin-table_name"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\_core\_mixin\.RepositoryCoreMixin\.table\_name

```python
def table_name(self) -> str:
```

获取表名

返回与模型类对应的数据库表名，由 \_get\_table\_name\_from\_model 推断得出。

返回:
    str: 数据库表名

示例:
    repo = UserRepository\(\)
    print\(repo\.table\_name\)  \# "users"
<a name="magic_base-data_access-repository-base_repository_cud_mixin"></a>
## 🅼 magic\_base\.data\_access\.repository\.base\_repository\_cud\_mixin

- **Constants:**
  - 🆅 [T](#magic_base-data_access-repository-base_repository_cud_mixin-T)
- **Classes:**
  - 🅲 [CUDRepositoryMixin](#magic_base-data_access-repository-base_repository_cud_mixin-CUDRepositoryMixin)

### Constants

<a name="magic_base-data_access-repository-base_repository_cud_mixin-T"></a>
### 🆅 magic\_base\.data\_access\.repository\.base\_repository\_cud\_mixin\.T

```python
T = TypeVar('T')
```

### Classes

<a name="magic_base-data_access-repository-base_repository_cud_mixin-CUDRepositoryMixin"></a>
### 🅲 magic\_base\.data\_access\.repository\.base\_repository\_cud\_mixin\.CUDRepositoryMixin

```python
class CUDRepositoryMixin(RepositoryCoreMixin[T]):
```

CUD 操作 Mixin（Create, Update, Delete）

提供使用 ORM 方式的创建、更新、删除操作。
继承自 RepositoryCoreMixin，获得核心基础设施。

设计理念:
    CUD 操作（创建、更新、删除）适合使用 ORM 方式，因为：
    - 需要对象关系映射的便利性
    - 需要自动处理关联关系
    - 需要触发 ORM 事件和钩子
    
包含的功能:
    - 单条记录的创建、更新、删除
    - 批量创建和更新
    - 软删除支持
    - ORM 实例获取

注意:
    本 Mixin 不包含查询操作，查询操作请使用 QueryRepositoryMixin

使用方式:
    class UserRepository\(RepositoryCoreMixin\[User\], CUDRepositoryMixin\[User\]\):
        pass
    
    repo = UserRepository\(\)
    user = repo\.create\(name="Alice", email="alice@example\.com"\)
    repo\.update\(user\.id, name="Alice Updated"\)
    repo\.delete\(user\.id, soft=True\)

**Functions:**

<a name="magic_base-data_access-repository-base_repository_cud_mixin-CUDRepositoryMixin-create"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\_cud\_mixin\.CUDRepositoryMixin\.create

```python
def create(self, **kwargs) -> T:
```

创建记录（ORM）

使用 ORM 方式创建并保存新记录，自动刷新并获取自增 ID。

执行流程:
    1\. 根据关键字参数实例化模型对象
    2\. 将实例添加到会话
    3\. 刷新会话（发送 SQL 到数据库）
    4\. 刷新实例（获取数据库生成的值，如自增 ID）

参数:
    \*\*kwargs: 模型字段名和值的键值对，字段名需与模型定义一致

返回:
    T: 创建后的模型实例（包含自增 ID 等数据库生成的值）

示例:
    \# 创建用户
    user = repo\.create\(
        name="Alice", 
        email="alice@example\.com",
        age=25
    \)
    print\(user\.id\)  \# 自动生成的 ID
    print\(user\.created\_at\)  \# 自动设置的时间戳

注意:
    如果模型定义了默认值或自动字段（如 created\_at），
    会在 refresh 后获得这些值。
<a name="magic_base-data_access-repository-base_repository_cud_mixin-CUDRepositoryMixin-create_from_model"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\_cud\_mixin\.CUDRepositoryMixin\.create\_from\_model

```python
def create_from_model(self, model: T) -> T:
```

从模型对象创建（ORM）

使用已有的模型实例创建记录，适用于模型已经部分填充的情况。

使用场景:
    - 模型已经通过其他方式构建完成
    - 需要批量创建相同的模型实例
    - 模型包含复杂的嵌套关系

参数:
    model: 模型实例对象（可以是新建的或从其他地方获取的）

返回:
    T: 创建后的模型实例（包含自增 ID）

示例:
    \# 预先构建模型
    user = User\(name="Bob", email="bob@example\.com"\)
    user\.age = 30
    
    \# 保存到数据库
    repo\.create\_from\_model\(user\)
    print\(user\.id\)  \# 现在有了 ID
<a name="magic_base-data_access-repository-base_repository_cud_mixin-CUDRepositoryMixin-update"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\_cud\_mixin\.CUDRepositoryMixin\.update

```python
def update(self, record_id: int, **kwargs) -> bool:
```

更新记录（ORM）

根据 ID 查找记录并更新指定字段。

执行流程:
    1\. 根据主键 ID 查询记录
    2\. 如果记录存在，更新指定字段的值
    3\. 刷新会话使更改生效

参数:
    record\_id: 记录的主键 ID
    \*\*kwargs: 要更新的字段名和值，只更新提供的字段

返回:
    bool: True 表示更新成功（记录存在），False 表示记录不存在

示例:
    \# 更新单个字段
    repo\.update\(1, name="New Name"\)
    
    \# 同时更新多个字段
    repo\.update\(1, name="New Name", age=26, email="new@example\.com"\)

注意:
    不会更新未在 kwargs 中指定的字段，保持原有值不变。
<a name="magic_base-data_access-repository-base_repository_cud_mixin-CUDRepositoryMixin-update_from_model"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\_cud\_mixin\.CUDRepositoryMixin\.update\_from\_model

```python
def update_from_model(self, model: T) -> bool:
```

从模型对象更新（ORM）

使用 merge 操作将模型实例的状态同步到数据库。

merge 操作的特点:
    - 如果数据库中存在相同 ID 的记录，则更新
    - 如果不存在，则插入新记录
    - 会返回一个附加到当前会话的实例

参数:
    model: 包含更新数据的模型实例（通常包含 ID 字段）

返回:
    bool: 总是返回 True

示例:
    \# 获取 ORM 实例
    user = repo\.get\_orm\_instance\(1\)
    
    \# 修改属性
    user\.name = "New Name"
    user\.email = "updated@example\.com"
    
    \# 保存更改
    repo\.update\_from\_model\(user\)

适用场景:
    - 在会话外修改了模型实例
    - 需要将脱管（detached）实例重新附加到会话
<a name="magic_base-data_access-repository-base_repository_cud_mixin-CUDRepositoryMixin-delete"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\_cud\_mixin\.CUDRepositoryMixin\.delete

```python
def delete(self, record_id: int, soft: bool = True, active_field: str = 'is_active') -> bool:
```

删除记录（ORM）

支持软删除和硬删除两种模式。

软删除（soft=True）:
    - 不实际删除数据，只设置激活状态字段为 False
    - 数据仍然保留在数据库中，可通过修改状态恢复
    - 适合需要数据审计或恢复的场景
    
硬删除（soft=False）:
    - 从数据库中物理删除记录
    - 数据永久丢失，无法恢复
    - 适合不需要保留历史数据的场景

参数:
    record\_id: 记录的主键 ID
    soft: 是否软删除，True 表示软删除（设置 is\_active=False），
          False 表示物理删除（从表中删除）
    active\_field: 激活状态字段名，默认为 'is\_active'
                   仅软删除模式使用

返回:
    bool: True 表示删除成功（记录存在），False 表示记录不存在

异常:
    ValueError: 当使用软删除但模型缺少指定的 active\_field 字段时抛出

示例:
    \# 软删除（推荐）
    repo\.delete\(1, soft=True\)
    
    \# 硬删除（谨慎使用）
    repo\.delete\(1, soft=False\)
    
    \# 自定义激活字段名
    repo\.delete\(1, soft=True, active\_field='enabled'\)
<a name="magic_base-data_access-repository-base_repository_cud_mixin-CUDRepositoryMixin-batch_create"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\_cud\_mixin\.CUDRepositoryMixin\.batch\_create

```python
def batch_create(self, models: List[T]) -> List[T]:
```

批量创建（ORM）

使用 bulk\_save\_objects 批量插入多个模型实例，性能优于逐个插入。

性能优势:
    - 减少数据库往返次数
    - 使用更高效的批量插入语句
    - 对于大量数据插入，性能提升显著

参数:
    models: 模型实例列表

返回:
    List\[T\]: 创建后的模型实例列表（与输入相同）

注意:
    批量操作不会触发 ORM 的事件（如 before\_insert）和钩子函数。
    如果需要触发事件，请使用循环逐个 create\(\)。

示例:
    users = \[
        User\(name="User1", email="user1@example\.com"\),
        User\(name="User2", email="user2@example\.com"\),
        User\(name="User3", email="user3@example\.com"\)
    \]
    repo\.batch\_create\(users\)

适用场景:
    - 数据迁移
    - 批量导入
    - 测试数据准备
<a name="magic_base-data_access-repository-base_repository_cud_mixin-CUDRepositoryMixin-batch_create_from_dict"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\_cud\_mixin\.CUDRepositoryMixin\.batch\_create\_from\_dict

```python
def batch_create_from_dict(self, models_data: List[Dict[str, str]]) -> int:
```

从字典格式批量创建
<a name="magic_base-data_access-repository-base_repository_cud_mixin-CUDRepositoryMixin-batch_update"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\_cud\_mixin\.CUDRepositoryMixin\.batch\_update

```python
def batch_update(self, updates: Dict[int, Dict[str, Any]]) -> int:
```

批量更新（ORM）

根据 ID 字典批量更新多条记录的不同字段。

参数:
    updates: 更新字典，格式为 \{record\_id: \{field\_name: new\_value, \.\.\.\}\}
            每个记录可以更新不同的字段集

返回:
    int: 实际更新的记录数量（不包括不存在的记录）

示例:
    updates = \{
        1: \{'name': 'Alice Updated', 'age': 31\},
        2: \{'name': 'Bob Updated'\},
        3: \{'email': 'charlie@new\.com', 'is\_active': False\}
    \}
    count = repo\.batch\_update\(updates\)
    print\(f"成功更新 \{count\} 条记录"\)

性能考虑:
    每条记录单独更新，对于大量记录建议使用原生 SQL 批量更新。

注意:
    不存在的记录会被跳过，不会抛出异常。
<a name="magic_base-data_access-repository-base_repository_cud_mixin-CUDRepositoryMixin-get_orm_instance"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\_cud\_mixin\.CUDRepositoryMixin\.get\_orm\_instance

```python
def get_orm_instance(self, record_id: int) -> Optional[T]:
```

获取 ORM 实例

返回完整的 ORM 模型实例，可用于进一步的 ORM 操作。

与查询方法返回字典不同，此方法返回 ORM 对象，可以：
    - 访问关联关系（relationships）
    - 调用模型的方法
    - 修改后直接 update\_from\_model

参数:
    record\_id: 记录的主键 ID

返回:
    Optional\[T\]: 模型实例，不存在时返回 None

示例:
    \# 获取实例并修改
    user = repo\.get\_orm\_instance\(1\)
    if user:
        user\.last\_login = datetime\.now\(\)
        repo\.update\_from\_model\(user\)
    
    \# 访问关联关系（假设定义了 relationship）
    user = repo\.get\_orm\_instance\(1\)
    if user and user\.profile:
        print\(user\.profile\.bio\)

适用场景:
    - 需要操作关联数据
    - 需要调用模型业务方法
    - 需要 ORM 的懒加载特性
<a name="magic_base-data_access-repository-base_repository_query_mixin"></a>
## 🅼 magic\_base\.data\_access\.repository\.base\_repository\_query\_mixin

- **Constants:**
  - 🆅 [T](#magic_base-data_access-repository-base_repository_query_mixin-T)
- **Classes:**
  - 🅲 [QueryRepositoryMixin](#magic_base-data_access-repository-base_repository_query_mixin-QueryRepositoryMixin)

### Constants

<a name="magic_base-data_access-repository-base_repository_query_mixin-T"></a>
### 🆅 magic\_base\.data\_access\.repository\.base\_repository\_query\_mixin\.T

```python
T = TypeVar('T')
```

### Classes

<a name="magic_base-data_access-repository-base_repository_query_mixin-QueryRepositoryMixin"></a>
### 🅲 magic\_base\.data\_access\.repository\.base\_repository\_query\_mixin\.QueryRepositoryMixin

```python
class QueryRepositoryMixin(RepositoryCoreMixin[T]):
```

查询操作 Mixin（Query）

提供使用原生 SQL 方式的查询操作，包括基础查询、动态查询、分页等。
继承自 RepositoryCoreMixin，获得核心基础设施。

设计理念:
    查询操作（Read）适合使用原生 SQL 方式，因为：
    - 可以精确控制查询语句，优化性能
    - 支持复杂的 JOIN、子查询、聚合函数
    - 避免 ORM 的性能开销
    - 返回字典格式，便于序列化和数据传输

包含的功能:
    - 原生 SQL 执行（fetch\_one/fetch\_all）
    - 基础查询（get\_by\_id/get\_all）
    - 动态条件查询（find/find\_one）
    - 存在性检查（exists）
    - 计数统计（count）
    - 分页查询（paginate）

注意:
    本 Mixin 不包含 CUD 操作（创建、更新、删除），
    CUD 操作请使用 CUDRepositoryMixin

使用方式:
    class UserRepository\(RepositoryCoreMixin\[User\], QueryRepositoryMixin\[User\]\):
        pass
    
    repo = UserRepository\(\)
    
    \# 基础查询
    user = repo\.get\_by\_id\(1\)
    users = repo\.get\_all\(filters=\{'is\_active': True\}, limit=10\)
    
    \# 动态查询
    admins = repo\.find\(conditions=\{'role': 'admin', 'is\_active': True\}\)
    
    \# 分页
    page = repo\.paginate\(page=2, per\_page=20, conditions=\{'is\_active': True\}\)

**Functions:**

<a name="magic_base-data_access-repository-base_repository_query_mixin-QueryRepositoryMixin-fetch_one"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\_query\_mixin\.QueryRepositoryMixin\.fetch\_one

```python
def fetch_one(self, sql: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict]:
```

查询单条记录（原生 SQL）

执行 SQL 查询并返回第一条记录，以字典形式呈现。

执行流程:
    1\. 执行原始 SQL 语句
    2\. 获取第一条结果行
    3\. 将行数据转换为字典（列名 -\> 值）
    4\. 如果没有结果返回 None

参数:
    sql: SQL 查询语句，支持命名占位符 :param\_name
    params: 参数字典，用于 SQL 占位符 :param\_name

返回:
    Optional\[Dict\]: 记录字典，键为列名，值为对应的值；未找到时返回 None

示例:
    \# 简单查询
    user = repo\.fetch\_one\("SELECT \* FROM users WHERE id = 1"\)
    
    \# 参数化查询（防止 SQL 注入）
    user = repo\.fetch\_one\(
        "SELECT \* FROM users WHERE id = :id AND is\_active = :active",
        \{'id': 1, 'active': True\}
    \)

注意:
    即使 SQL 返回多行，也只返回第一行。如需多行，使用 fetch\_all。
    建议始终使用参数化查询，避免 SQL 注入风险。
<a name="magic_base-data_access-repository-base_repository_query_mixin-QueryRepositoryMixin-fetch_all"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\_query\_mixin\.QueryRepositoryMixin\.fetch\_all

```python
def fetch_all(self, sql: str, params: Optional[Dict[str, Any]] = None) -> List[Dict]:
```

查询多条记录（原生 SQL）

执行 SQL 查询并返回所有记录，每条记录以字典形式呈现。

执行流程:
    1\. 执行原始 SQL 语句
    2\. 获取所有结果行
    3\. 将每行数据转换为字典（列名 -\> 值）
    4\. 返回字典列表

参数:
    sql: SQL 查询语句，支持命名占位符 :param\_name
    params: 参数字典，用于 SQL 占位符 :param\_name

返回:
    List\[Dict\]: 记录字典列表，未找到时返回空列表 \[\]

示例:
    \# 查询所有激活用户
    users = repo\.fetch\_all\(
        "SELECT \* FROM users WHERE is\_active = :active",
        \{'active': True\}
    \)
    
    \# 复杂 JOIN 查询
    results = repo\.fetch\_all\("
        SELECT u\.\*, p\.bio 
        FROM users u
        LEFT JOIN profiles p ON u\.id = p\.user\_id
        WHERE u\.created\_at \> :since
    ", \{'since': '2024-01-01'\}\)

性能考虑:
    对于可能返回大量数据的查询，建议添加 LIMIT 限制，
    或者使用分页查询减少单次返回的数据量。
<a name="magic_base-data_access-repository-base_repository_query_mixin-QueryRepositoryMixin-get_by_id"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\_query\_mixin\.QueryRepositoryMixin\.get\_by\_id

```python
def get_by_id(self, record_id: int) -> Optional[Dict]:
```

根据 ID 查询（SQL）

使用原生 SQL 根据主键 ID 查询单条记录。
这是最常用的查询方法之一。

参数:
    record\_id: 记录的主键 ID（通常为自增整数 ID）

返回:
    Optional\[Dict\]: 记录字典，键为列名，值为对应的值；未找到时返回 None

示例:
    \# 查询 ID 为 1 的用户
    user = repo\.get\_by\_id\(1\)
    if user:
        print\(f"用户名: \{user\['name'\]\}"\)
    else:
        print\("用户不存在"\)

注意:
    此方法假设主键字段名为 "id"。
    如果表使用其他主键名，请使用 fetch\_one 自定义查询。
<a name="magic_base-data_access-repository-base_repository_query_mixin-QueryRepositoryMixin-get_all"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\_query\_mixin\.QueryRepositoryMixin\.get\_all

```python
def get_all(self, filters: Optional[Dict[str, Any]] = None, order_by: Optional[str] = None, limit: Optional[int] = None) -> List[Dict]:
```

查询所有记录（SQL）

支持过滤条件、排序和限制返回数量，是基础的列表查询方法。

参数:
    filters: 过滤条件字典，格式为 \{field\_name: value\}
            所有条件使用 AND 连接，且为等值匹配
    order\_by: 排序字段，格式如 "id DESC" 或 "created\_at ASC"
    limit: 返回记录数量限制

返回:
    List\[Dict\]: 记录字典列表

示例:
    \# 查询所有用户
    all\_users = repo\.get\_all\(\)
    
    \# 带过滤条件
    active\_users = repo\.get\_all\(
        filters=\{'is\_active': True, 'role': 'user'\}
    \)
    
    \# 带排序和限制
    recent\_users = repo\.get\_all\(
        filters=\{'is\_active': True\},
        order\_by='created\_at DESC',
        limit=10
    \)

注意:
    过滤条件仅支持等值（=）匹配。如需范围查询（\>、\<、LIKE 等），
    请使用 find 方法或自定义 fetch\_all。
<a name="magic_base-data_access-repository-base_repository_query_mixin-QueryRepositoryMixin-find"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\_query\_mixin\.QueryRepositoryMixin\.find

```python
def find(self, conditions: Optional[Dict[str, Any]] = None, order_by: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None) -> List[Dict]:
```

动态查询（SQL）

灵活的查询方法，支持等值条件、排序、分页，比 get\_all 更灵活。

参数:
    conditions: 查询条件字典，格式为 \{field\_name: value\}
               所有条件使用 AND 连接，且为等值匹配
    order\_by: 排序字段，如 "created\_at DESC" 或 "name ASC"
    limit: 返回记录数量限制
    offset: 偏移量，用于分页（配合 limit 使用）

返回:
    List\[Dict\]: 记录字典列表

示例:
    \# 基础查询
    users = repo\.find\(conditions=\{'is\_active': True\}\)
    
    \# 分页查询
    page\_users = repo\.find\(
        conditions=\{'is\_active': True\},
        order\_by='id DESC',
        limit=20,
        offset=40
    \)
    
    \# 无条件的查询（相当于 get\_all）
    all\_users = repo\.find\(\)

适用场景:
    - 需要分页的列表查询
    - 简单的多条件等值查询
    - 需要排序和限制的查询

注意:
    仅支持等值匹配，复杂查询请使用 fetch\_all 方法。
<a name="magic_base-data_access-repository-base_repository_query_mixin-QueryRepositoryMixin-find_one"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\_query\_mixin\.QueryRepositoryMixin\.find\_one

```python
def find_one(self, conditions: Dict[str, Any]) -> Optional[Dict]:
```

查询单条记录（SQL）

根据条件查询第一条匹配的记录，常用于唯一性检查或获取单个结果。

参数:
    conditions: 查询条件字典，格式为 \{field\_name: value\}
               所有条件使用 AND 连接

返回:
    Optional\[Dict\]: 记录字典，未找到时返回 None

示例:
    \# 根据邮箱查找用户
    user = repo\.find\_one\(\{'email': 'alice@example\.com'\}\)
    
    \# 根据用户名和状态查找
    user = repo\.find\_one\(\{
        'username': 'alice',
        'is\_active': True
    \}\)
    
    \# 检查记录是否存在
    if repo\.find\_one\(\{'email': email\}\):
        raise ValueError\("邮箱已被注册"\)

注意:
    如果多个记录匹配条件，只返回第一个。
    建议在条件中包含唯一索引字段，确保结果唯一。
<a name="magic_base-data_access-repository-base_repository_query_mixin-QueryRepositoryMixin-exists"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\_query\_mixin\.QueryRepositoryMixin\.exists

```python
def exists(self, **conditions) -> bool:
```

检查是否存在（SQL）

检查是否存在满足条件的记录，常用于唯一性验证和存在性检查。

参数:
    \*\*conditions: 条件字段和值的键值对，支持多个条件

返回:
    bool: True 表示至少存在一条满足条件的记录，False 表示不存在

示例:
    \# 检查邮箱是否已存在
    if repo\.exists\(email='alice@example\.com'\):
        print\("用户已存在"\)
    
    \# 检查用户是否激活
    if repo\.exists\(id=1, is\_active=True\):
        print\("用户已激活"\)
    
    \# 验证唯一性
    def register\_user\(email, username\):
        if repo\.exists\(email=email\):
            raise ValueError\("邮箱已被注册"\)
        if repo\.exists\(username=username\):
            raise ValueError\("用户名已被占用"\)
        \# 注册逻辑\.\.\.

性能考虑:
    此方法在查到第一条匹配记录后就会停止，比 count\(\) \> 0 更高效。
<a name="magic_base-data_access-repository-base_repository_query_mixin-QueryRepositoryMixin-count"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\_query\_mixin\.QueryRepositoryMixin\.count

```python
def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
```

统计数量（SQL）

统计满足条件的记录总数，常用于数据概览和分页计算。

参数:
    filters: 过滤条件字典，格式为 \{field\_name: value\}
            所有条件使用 AND 连接

返回:
    int: 记录总数，如果无匹配记录返回 0

示例:
    \# 统计所有用户
    total\_users = repo\.count\(\)
    
    \# 统计激活用户数
    active\_count = repo\.count\(\{'is\_active': True\}\)
    
    \# 统计 admin 角色数量
    admin\_count = repo\.count\(\{'role': 'admin', 'is\_active': True\}\)
    
    \# 用于分页计算
    total = repo\.count\(conditions\)
    pages = \(total \+ per\_page - 1\) // per\_page

注意:
    如果 filters 为 None 或空字典，统计所有记录。
    对于大表，COUNT\(\*\) 操作可能较慢，请谨慎使用。
<a name="magic_base-data_access-repository-base_repository_query_mixin-QueryRepositoryMixin-paginate"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\_query\_mixin\.QueryRepositoryMixin\.paginate

```python
def paginate(self, page: int = 1, per_page: int = 20, conditions: Optional[Dict[str, Any]] = None, order_by: str = 'id DESC') -> Dict[str, Any]:
```

分页查询（SQL）

实现标准的分页查询，返回包含数据和分页信息的字典。
这是 Web 应用中最常用的查询方法之一。

参数:
    page: 当前页码，从 1 开始（第 1 页为首页）
    per\_page: 每页记录数，默认 20 条
    conditions: 查询条件字典，格式为 \{field\_name: value\}
    order\_by: 排序字段，默认为 "id DESC"（最新的在前）

返回:
    Dict\[str, Any\]: 分页结果字典，包含以下键：
        - items: 当前页的记录列表（List\[Dict\]）
        - total: 总记录数（int）
        - page: 当前页码（int）
        - per\_page: 每页记录数（int）
        - pages: 总页数（int）
        - has\_next: 是否有下一页（bool）
        - has\_prev: 是否有上一页（bool）

示例:
    \# 基础分页
    result = repo\.paginate\(page=2, per\_page=10\)
    for user in result\['items'\]:
        print\(user\['name'\]\)
    
    \# 带条件的分页
    result = repo\.paginate\(
        page=1,
        per\_page=20,
        conditions=\{'is\_active': True\},
        order\_by='created\_at DESC'
    \)
    
    \# 渲染分页导航
    print\(f"第 \{result\['page'\]\} 页，共 \{result\['pages'\]\} 页"\)
    if result\['has\_prev'\]:
        print\("上一页"\)
    if result\['has\_next'\]:
        print\("下一页"\)

分页计算:
    offset = \(page - 1\) \* per\_page
    LIMIT per\_page OFFSET offset

注意:
    page 参数小于 1 时会被视为 1。
    per\_page 建议根据实际需求设置，避免单次返回过多数据。
<a name="magic_base-data_access-repository-base_sqlalchemy_repository"></a>
## 🅼 magic\_base\.data\_access\.repository\.base\_sqlalchemy\_repository

SQLAlchemy 仓储实现（可选）

提供基于 SQLAlchemy 的通用 CRUD 实现，业务模块可直接继承使用。

设计原则：
- 简单 CRUD：使用 ORM，安全便捷
- 复杂查询：使用参数化原生 SQL \+ 白名单验证

- **Constants:**
  - 🆅 [T](#magic_base-data_access-repository-base_sqlalchemy_repository-T)
- **Classes:**
  - 🅲 [SQLAlchemyRepository](#magic_base-data_access-repository-base_sqlalchemy_repository-SQLAlchemyRepository)

### Constants

<a name="magic_base-data_access-repository-base_sqlalchemy_repository-T"></a>
### 🆅 magic\_base\.data\_access\.repository\.base\_sqlalchemy\_repository\.T

```python
T = TypeVar('T')
```

### Classes

<a name="magic_base-data_access-repository-base_sqlalchemy_repository-SQLAlchemyRepository"></a>
### 🅲 magic\_base\.data\_access\.repository\.base\_sqlalchemy\_repository\.SQLAlchemyRepository

```python
class SQLAlchemyRepository(BaseRepository[T], Generic[T]):
```

SQLAlchemy 仓储实现

提供 ORM 和参数化 SQL 两种查询方式。

**Functions:**

<a name="magic_base-data_access-repository-base_sqlalchemy_repository-SQLAlchemyRepository-__init__"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_sqlalchemy\_repository\.SQLAlchemyRepository\.\_\_init\_\_

```python
def __init__(self, model_class: Type[T], session_factory: Callable[[], Session], soft_field: str = 'is_active', allowed_columns: Optional[List[str]] = None):
```

初始化仓储

**Parameters:**

- **model_class**: SQLAlchemy 模型类
- **session_factory**: 返回数据库 session 的可调用对象
- **soft_field**: 软删除字段名（默认 is\_active）
- **allowed_columns**: 允许查询的列名白名单（None 表示从模型自动获取）
<a name="magic_base-data_access-repository-base_sqlalchemy_repository-SQLAlchemyRepository-execute_query"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_sqlalchemy\_repository\.SQLAlchemyRepository\.execute\_query

```python
def execute_query(self, sql: str, params: Optional[Dict] = None) -> List[Dict]:
```

执行参数化查询（安全）

**Parameters:**

- **sql**: 参数化 SQL 语句，使用 :name 格式
- **params**: 参数字典

**Returns:**

- 查询结果列表（Dict 格式）
<a name="magic_base-data_access-repository-base_sqlalchemy_repository-SQLAlchemyRepository-execute_query_one"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_sqlalchemy\_repository\.SQLAlchemyRepository\.execute\_query\_one

```python
def execute_query_one(self, sql: str, params: Optional[Dict] = None) -> Optional[Dict]:
```

执行参数化查询，返回单条结果
<a name="magic_base-data_access-repository-base_sqlalchemy_repository-SQLAlchemyRepository-get_by_id"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_sqlalchemy\_repository\.SQLAlchemyRepository\.get\_by\_id

```python
def get_by_id(self, id: int) -> Optional[Dict]:
```

根据 ID 获取单条记录（ORM）
<a name="magic_base-data_access-repository-base_sqlalchemy_repository-SQLAlchemyRepository-find_one"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_sqlalchemy\_repository\.SQLAlchemyRepository\.find\_one

```python
def find_one(self, conditions: Dict[str, Any]) -> Optional[Dict]:
```

根据条件获取单条记录（ORM）
<a name="magic_base-data_access-repository-base_sqlalchemy_repository-SQLAlchemyRepository-find"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_sqlalchemy\_repository\.SQLAlchemyRepository\.find

```python
def find(self, conditions: Optional[Dict] = None, order_by: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None) -> List[Dict]:
```

根据条件查询记录列表（ORM）
<a name="magic_base-data_access-repository-base_sqlalchemy_repository-SQLAlchemyRepository-get_all"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_sqlalchemy\_repository\.SQLAlchemyRepository\.get\_all

```python
def get_all(self, filters: Optional[Dict] = None, order_by: Optional[str] = None, limit: Optional[int] = None) -> List[Dict]:
```

获取所有记录（简化版）
<a name="magic_base-data_access-repository-base_sqlalchemy_repository-SQLAlchemyRepository-exists"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_sqlalchemy\_repository\.SQLAlchemyRepository\.exists

```python
def exists(self, **conditions) -> bool:
```

检查记录是否存在
<a name="magic_base-data_access-repository-base_sqlalchemy_repository-SQLAlchemyRepository-count"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_sqlalchemy\_repository\.SQLAlchemyRepository\.count

```python
def count(self, filters: Optional[Dict] = None) -> int:
```

统计记录数量（ORM）
<a name="magic_base-data_access-repository-base_sqlalchemy_repository-SQLAlchemyRepository-paginate"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_sqlalchemy\_repository\.SQLAlchemyRepository\.paginate

```python
def paginate(self, page: int = 1, per_page: int = 20, filters: Optional[Dict] = None, order_by: str = 'id DESC') -> Dict:
```

分页查询（ORM）
<a name="magic_base-data_access-repository-base_sqlalchemy_repository-SQLAlchemyRepository-create"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_sqlalchemy\_repository\.SQLAlchemyRepository\.create

```python
def create(self, **kwargs) -> T:
```

创建记录（从参数）
<a name="magic_base-data_access-repository-base_sqlalchemy_repository-SQLAlchemyRepository-create_from_model"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_sqlalchemy\_repository\.SQLAlchemyRepository\.create\_from\_model

```python
def create_from_model(self, model: T) -> T:
```

创建记录（从模型对象）
<a name="magic_base-data_access-repository-base_sqlalchemy_repository-SQLAlchemyRepository-batch_create"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_sqlalchemy\_repository\.SQLAlchemyRepository\.batch\_create

```python
def batch_create(self, models: List[T]) -> List[T]:
```

批量创建
<a name="magic_base-data_access-repository-base_sqlalchemy_repository-SQLAlchemyRepository-update"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_sqlalchemy\_repository\.SQLAlchemyRepository\.update

```python
def update(self, id: int, **kwargs) -> bool:
```

更新记录（从参数）
<a name="magic_base-data_access-repository-base_sqlalchemy_repository-SQLAlchemyRepository-update_from_model"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_sqlalchemy\_repository\.SQLAlchemyRepository\.update\_from\_model

```python
def update_from_model(self, model: T) -> bool:
```

更新记录（从模型对象）
<a name="magic_base-data_access-repository-base_sqlalchemy_repository-SQLAlchemyRepository-batch_update"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_sqlalchemy\_repository\.SQLAlchemyRepository\.batch\_update

```python
def batch_update(self, updates: Dict[int, Dict[str, Any]]) -> int:
```

批量更新
<a name="magic_base-data_access-repository-base_sqlalchemy_repository-SQLAlchemyRepository-delete"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_sqlalchemy\_repository\.SQLAlchemyRepository\.delete

```python
def delete(self, id: int, soft: bool = True) -> bool:
```

删除单条记录
<a name="magic_base-data_access-repository-base_sqlalchemy_repository-SQLAlchemyRepository-batch_delete"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_sqlalchemy\_repository\.SQLAlchemyRepository\.batch\_delete

```python
def batch_delete(self, ids: List[int], soft: bool = True) -> int:
```

批量删除
<a name="magic_base-data_access-repository-base_sqlalchemy_repository-SQLAlchemyRepository-get_orm_instance"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_sqlalchemy\_repository\.SQLAlchemyRepository\.get\_orm\_instance

```python
def get_orm_instance(self, id: int) -> Optional[T]:
```

获取 ORM 实例
<a name="magic_base-data_access-repository-base_sqlalchemy_repository-SQLAlchemyRepository-get_allowed_columns"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_sqlalchemy\_repository\.SQLAlchemyRepository\.get\_allowed\_columns

```python
def get_allowed_columns(self) -> List[str]:
```

获取允许查询的列名列表
<a name="magic_base-data_access-service"></a>
## 🅼 magic\_base\.data\_access\.service
<a name="magic_base-data_access-service-base_service"></a>
## 🅼 magic\_base\.data\_access\.service\.base\_service

Service 基类 - 定义业务层接口

- **Constants:**
  - 🆅 [T](#magic_base-data_access-service-base_service-T)
- **Classes:**
  - 🅲 [BaseService](#magic_base-data_access-service-base_service-BaseService)
  - 🅲 [MagicBaseService](#magic_base-data_access-service-base_service-MagicBaseService)

### Constants

<a name="magic_base-data_access-service-base_service-T"></a>
### 🆅 magic\_base\.data\_access\.service\.base\_service\.T

```python
T = TypeVar('T')
```

### Classes

<a name="magic_base-data_access-service-base_service-BaseService"></a>
### 🅲 magic\_base\.data\_access\.service\.base\_service\.BaseService

```python
class BaseService(ABC, Generic[T]):
```

Service 抽象基类

提供对 Repository 的基础 CRUD 操作透传。
子类只需指定对应的 Repository 类型。

使用方式:
    class ProjectService\(BaseService\[Project\]\):
        def \_\_init\_\_\(self\):
            super\(\)\.\_\_init\_\_\(ProjectRepository\(\)\)

设计理念:
    - 基础 CRUD 方法由基类统一实现，避免重复代码
    - 子类可以添加业务方法
    - 保持与 Repository 方法命名一致

**Functions:**

<a name="magic_base-data_access-service-base_service-BaseService-__init__"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\.BaseService\.\_\_init\_\_

```python
def __init__(self, repository: BaseRepository[T]):
```

初始化 Service

参数:
    repository: 对应的 Repository 实例
<a name="magic_base-data_access-service-base_service-BaseService-create"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\.BaseService\.create

```python
def create(self, **kwargs) -> Dict:
```

创建记录
<a name="magic_base-data_access-service-base_service-BaseService-get_by_id"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\.BaseService\.get\_by\_id

```python
def get_by_id(self, record_id: int) -> Optional[Dict]:
```

根据ID获取记录
<a name="magic_base-data_access-service-base_service-BaseService-find"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\.BaseService\.find

```python
def find(self, conditions: Optional[Dict] = None, order_by: Optional[str] = None, limit: Optional[int] = None, offset: int = 0) -> List[Dict]:
```

条件查询
<a name="magic_base-data_access-service-base_service-BaseService-find_one"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\.BaseService\.find\_one

```python
def find_one(self, conditions: Dict) -> Optional[Dict]:
```

条件查询单条
<a name="magic_base-data_access-service-base_service-BaseService-find_all"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\.BaseService\.find\_all

```python
def find_all(self, limit: Optional[int] = None, offset: int = 0) -> List[Dict]:
```

查询所有
<a name="magic_base-data_access-service-base_service-BaseService-count"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\.BaseService\.count

```python
def count(self, conditions: Optional[Dict] = None) -> int:
```

统计数量
<a name="magic_base-data_access-service-base_service-BaseService-exists"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\.BaseService\.exists

```python
def exists(self, **kwargs) -> bool:
```

检查是否存在
<a name="magic_base-data_access-service-base_service-BaseService-paginate"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\.BaseService\.paginate

```python
def paginate(self, page: int = 1, per_page: int = 20, conditions: Optional[Dict] = None) -> Dict:
```

分页查询
<a name="magic_base-data_access-service-base_service-BaseService-update"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\.BaseService\.update

```python
def update(self, record_id: int, **kwargs) -> bool:
```

更新记录
<a name="magic_base-data_access-service-base_service-BaseService-batch_create"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\.BaseService\.batch\_create

```python
def batch_create(self, models: List[Dict[str, str]]) -> int:
```

批量创建
<a name="magic_base-data_access-service-base_service-BaseService-batch_update"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\.BaseService\.batch\_update

```python
def batch_update(self, updates: Dict[int, Dict]) -> int:
```

批量更新
<a name="magic_base-data_access-service-base_service-BaseService-delete"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\.BaseService\.delete

```python
def delete(self, record_id: int, soft: bool = True) -> bool:
```

删除记录
<a name="magic_base-data_access-service-base_service-BaseService-get_orm_instance"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\.BaseService\.get\_orm\_instance

```python
def get_orm_instance(self, record_id: int) -> Optional[T]:
```

获取 ORM 实例
<a name="magic_base-data_access-service-base_service-MagicBaseService"></a>
### 🅲 magic\_base\.data\_access\.service\.base\_service\.MagicBaseService

```python
class MagicBaseService(BaseService[T]):
```

Magic 系列基础 Service 适配类

继承自 ABC（抽象基类）和 BaseService，为 Magic 系列项目提供统一的 Service 基类。

设计目的:
    为 Magic 生态系统中的各个项目提供一致的 Service 接口，
    便于业务逻辑的复用和统一管理。

使用方式:
    from magic\_base\.data\_access\.service import MagicBaseService
    
    class UserService\(MagicBaseService\[User\]\):
        def \_\_init\_\_\(self\):
            self\.user\_repo = UserRepository\(\)
        
        def get\_by\_id\(self, id: int\) -\> Optional\[Dict\]:
            return self\.user\_repo\.get\_by\_id\(id\)
        
        def create\(self, data: Dict\[str, Any\]\) -\> Dict:
            self\.validate\(data\)
            user = self\.user\_repo\.create\(\*\*data\)
            return user\.to\_dict\(\)
        
        \# \.\.\. 实现其他抽象方法

注意:
    此类为抽象基类，通过 ABC 确保不能被直接实例化。
    必须通过子类继承并实现所有抽象方法。
<a name="magic_base-data_access-service-base_service_core_mixin"></a>
## 🅼 magic\_base\.data\_access\.service\.base\_service\_core\_mixin

Service 基类 - 定义业务层接口

- **Constants:**
  - 🆅 [T](#magic_base-data_access-service-base_service_core_mixin-T)
- **Classes:**
  - 🅲 [ServiceCoreMixin](#magic_base-data_access-service-base_service_core_mixin-ServiceCoreMixin)

### Constants

<a name="magic_base-data_access-service-base_service_core_mixin-T"></a>
### 🆅 magic\_base\.data\_access\.service\.base\_service\_core\_mixin\.T

```python
T = TypeVar('T')
```

### Classes

<a name="magic_base-data_access-service-base_service_core_mixin-ServiceCoreMixin"></a>
### 🅲 magic\_base\.data\_access\.service\.base\_service\_core\_mixin\.ServiceCoreMixin

```python
class ServiceCoreMixin(Generic[T]):
```

Service 核心 Mixin

提供 Service 的基础设施：验证接口、依赖注入等。
所有 Service 类都应该继承此 Mixin。

设计理念:
    与 RepositoryCoreMixin 对应，提供 Service 层的核心功能。
    负责定义基础的业务验证接口和公共属性。

泛型参数:
    T: 业务对象类型，可以是 Dict、Model 或自定义 DTO

**Functions:**

<a name="magic_base-data_access-service-base_service_core_mixin-ServiceCoreMixin-validate"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\_core\_mixin\.ServiceCoreMixin\.validate

```python
def validate(self, data: Dict[str, Any], is_update: bool = False) -> bool:
```

验证业务数据

子类应实现具体的验证逻辑，确保数据符合业务规则。

常见的验证项:
- 必填字段检查：确保关键字段已提供
- 格式验证：如邮箱、手机号、日期等格式
- 长度验证：字符串长度限制
- 取值范围验证：数字、枚举值的合法范围
- 唯一性检查：与数据库中的现有数据对比
- 业务规则验证：符合业务逻辑的规则
- 关联数据验证：关联对象的存在性

参数:
    data: 要验证的业务数据字典
    is\_update: 是否为更新操作
               True: 更新操作，某些字段可能未提供
               False: 创建操作，通常需要完整验证

返回:
    bool: True 表示验证通过

异常:
    ValueError: 验证失败时抛出，建议包含详细的错误信息

示例:
    def validate\(self, data: Dict\[str, Any\], is\_update: bool = False\) -\> bool:
        \# 邮箱验证
        email = data\.get\('email'\)
        if not email and not is\_update:
            raise ValueError\("邮箱是必填字段"\)
        if email and '@' not in email:
            raise ValueError\("邮箱格式不正确"\)
        
        \# 年龄验证
        age = data\.get\('age'\)
        if age is not None:
            if not isinstance\(age, int\) or age \< 0 or age \> 150:
                raise ValueError\("年龄必须在0-150之间"\)
        
        return True
<a name="magic_base-data_access-service-base_service_cud_mixin"></a>
## 🅼 magic\_base\.data\_access\.service\.base\_service\_cud\_mixin

Service 基类 - 定义业务层接口

- **Constants:**
  - 🆅 [T](#magic_base-data_access-service-base_service_cud_mixin-T)
- **Classes:**
  - 🅲 [CUDServiceMixin](#magic_base-data_access-service-base_service_cud_mixin-CUDServiceMixin)

### Constants

<a name="magic_base-data_access-service-base_service_cud_mixin-T"></a>
### 🆅 magic\_base\.data\_access\.service\.base\_service\_cud\_mixin\.T

```python
T = TypeVar('T')
```

### Classes

<a name="magic_base-data_access-service-base_service_cud_mixin-CUDServiceMixin"></a>
### 🅲 magic\_base\.data\_access\.service\.base\_service\_cud\_mixin\.CUDServiceMixin

```python
class CUDServiceMixin(ServiceCoreMixin[T]):
```

CUD 业务操作 Mixin \(Create, Update, Delete\)

提供使用 ORM 方式的创建、更新、删除业务操作。
继承自 ServiceCoreMixin，获得核心验证功能。

设计理念:
    与 CUDRepositoryMixin 对应，定义业务层的写操作接口。
    Service 层负责业务流程编排，通常内部会调用 CUDRepositoryMixin 的方法。

包含的功能:
    - 创建业务对象
    - 从模型对象创建
    - 更新业务对象
    - 从模型对象更新
    - 删除业务对象（支持软删除）
    - 获取 ORM 实例
    - 批量创建
    - 批量更新

使用方式:
    class UserService\(CUDServiceMixin\[User\]\):
        def \_\_init\_\_\(self, user\_repo: UserRepository\):
            self\.user\_repo = user\_repo
        
        def create\(self, data: Dict\[str, Any\]\) -\> Dict:
            \# 业务逻辑
            self\.validate\(data\)
            
            \# 业务规则检查
            if self\.user\_repo\.exists\(email=data\['email'\]\):
                raise ValueError\("邮箱已被注册"\)
            
            \# 调用 Repository
            user = self\.user\_repo\.create\(\*\*data\)
            return user\.to\_dict\(\)

**Functions:**

<a name="magic_base-data_access-service-base_service_cud_mixin-CUDServiceMixin-create"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\_cud\_mixin\.CUDServiceMixin\.create

```python
def create(self, data: Dict[str, Any]) -> Dict:
```

创建业务对象

处理创建业务对象的完整流程，包括验证、转换和持久化。

业务逻辑可包含:
- 数据验证：调用 validate 方法验证输入数据
- 业务规则检查：如唯一性约束、关联数据存在性等
- 默认值设置：为未提供的字段设置默认值
- 关联数据处理：创建主对象时同时创建关联对象
- 日志记录：记录创建操作日志
- 事件触发：触发创建后的事件（如发送通知）

参数:
    data: 要创建的业务对象数据字典

返回:
    Dict: 创建后的完整业务对象（通常包含自动生成的 ID）

异常:
    ValueError: 数据验证失败或业务规则违反时抛出

示例:
    user\_data = \{
        'name': 'Alice',
        'email': 'alice@example\.com',
        'role': 'user'
    \}
    new\_user = user\_service\.create\(user\_data\)
    print\(f"创建成功，用户 ID: \{new\_user\['id'\]\}"\)
<a name="magic_base-data_access-service-base_service_cud_mixin-CUDServiceMixin-create_from_model"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\_cud\_mixin\.CUDServiceMixin\.create\_from\_model

```python
def create_from_model(self, model: T) -> Dict:
```

从模型对象创建业务对象

使用已有的模型实例创建记录，适用于模型已经部分填充的情况。

业务逻辑可包含:
- 模型验证
- 业务规则检查
- 数据转换

参数:
    model: 模型实例对象

返回:
    Dict: 创建后的业务对象字典

示例:
    user = User\(name="Bob", email="bob@example\.com"\)
    user\_dict = user\_service\.create\_from\_model\(user\)
<a name="magic_base-data_access-service-base_service_cud_mixin-CUDServiceMixin-update"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\_cud\_mixin\.CUDServiceMixin\.update

```python
def update(self, id: int, data: Dict[str, Any]) -> Dict:
```

更新业务对象

处理更新业务对象的完整流程，支持部分字段更新。

业务逻辑可包含:
- 存在性检查：验证要更新的对象是否存在
- 数据验证：调用 validate 方法验证更新数据
- 业务规则检查：如状态转换合法性
- 乐观锁处理：防止并发更新冲突
- 更新时间戳：自动更新 updated\_at 字段

参数:
    id: 要更新的业务对象 ID
    data: 要更新的字段字典（支持部分字段更新）

返回:
    Dict: 更新后的完整业务对象

异常:
    ValueError: 对象不存在、数据验证失败或业务规则违反时抛出

示例:
    update\_data = \{'name': 'Alice Updated', 'email': 'alice\_new@example\.com'\}
    updated\_user = user\_service\.update\(1, update\_data\)
<a name="magic_base-data_access-service-base_service_cud_mixin-CUDServiceMixin-update_from_model"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\_cud\_mixin\.CUDServiceMixin\.update\_from\_model

```python
def update_from_model(self, model: T) -> Dict:
```

从模型对象更新业务对象

使用 merge 操作将模型实例的状态同步到数据库。

参数:
    model: 包含更新数据的模型实例

返回:
    Dict: 更新后的业务对象字典

示例:
    user = user\_service\.get\_orm\_instance\(1\)
    user\.name = "New Name"
    updated\_user = user\_service\.update\_from\_model\(user\)
<a name="magic_base-data_access-service-base_service_cud_mixin-CUDServiceMixin-delete"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\_cud\_mixin\.CUDServiceMixin\.delete

```python
def delete(self, id: int, soft: bool = True) -> bool:
```

删除业务对象

支持软删除和硬删除两种模式，可根据业务需求选择。

业务逻辑可包含:
- 权限检查：验证用户是否有删除权限
- 关联数据检查：检查是否有依赖数据阻止删除
- 业务规则验证：如某些状态的对象不可删除

参数:
    id: 要删除的业务对象 ID
    soft: 是否软删除
        - True: 软删除，设置 is\_active=False 或 deleted\_at
        - False: 硬删除，从数据库中物理删除

返回:
    bool: True 表示删除成功，False 表示对象不存在

示例:
    \# 软删除（推荐）
    if user\_service\.delete\(1, soft=True\):
        print\("用户已禁用"\)
<a name="magic_base-data_access-service-base_service_cud_mixin-CUDServiceMixin-get_orm_instance"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\_cud\_mixin\.CUDServiceMixin\.get\_orm\_instance

```python
def get_orm_instance(self, id: int) -> Optional[T]:
```

获取 ORM 实例

返回完整的 ORM 模型实例，可用于进一步的 ORM 操作。

参数:
    id: 记录的主键 ID

返回:
    Optional\[T\]: 模型实例，不存在时返回 None

示例:
    user = user\_service\.get\_orm\_instance\(1\)
    if user:
        user\.last\_login = datetime\.now\(\)
        user\_service\.update\_from\_model\(user\)
<a name="magic_base-data_access-service-base_service_cud_mixin-CUDServiceMixin-batch_create"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\_cud\_mixin\.CUDServiceMixin\.batch\_create

```python
def batch_create(self, items: List[Dict[str, Any]]) -> List[Dict]:
```

批量创建业务对象

一次性创建多个业务对象，提高批量处理效率。

业务逻辑可包含:
- 批量验证：验证所有数据项
- 事务处理：确保全部成功或全部失败
- 性能优化：使用批量插入减少数据库往返

参数:
    items: 业务对象数据字典列表

返回:
    List\[Dict\]: 创建后的业务对象列表（包含生成的 ID）

异常:
    ValueError: 任一数据验证失败时抛出

示例:
    users\_data = \[
        \{'name': 'User1', 'email': 'user1@example\.com'\},
        \{'name': 'User2', 'email': 'user2@example\.com'\}
    \]
    created\_users = user\_service\.batch\_create\(users\_data\)
<a name="magic_base-data_access-service-base_service_cud_mixin-CUDServiceMixin-batch_update"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\_cud\_mixin\.CUDServiceMixin\.batch\_update

```python
def batch_update(self, updates: Dict[int, Dict[str, Any]]) -> int:
```

批量更新业务对象

一次性更新多个业务对象，每个对象可以更新不同的字段。

参数:
    updates: 更新字典，格式为 \{record\_id: \{field\_name: new\_value, \.\.\.\}\}

返回:
    int: 实际更新的记录数量

示例:
    updates = \{
        1: \{'name': 'User1 Updated', 'status': 'active'\},
        2: \{'email': 'user2\_new@example\.com'\}
    \}
    updated\_count = user\_service\.batch\_update\(updates\)
<a name="magic_base-data_access-service-base_service_query_mixin"></a>
## 🅼 magic\_base\.data\_access\.service\.base\_service\_query\_mixin

Service 基类 - 定义业务层接口

- **Constants:**
  - 🆅 [T](#magic_base-data_access-service-base_service_query_mixin-T)
- **Classes:**
  - 🅲 [QueryServiceMixin](#magic_base-data_access-service-base_service_query_mixin-QueryServiceMixin)

### Constants

<a name="magic_base-data_access-service-base_service_query_mixin-T"></a>
### 🆅 magic\_base\.data\_access\.service\.base\_service\_query\_mixin\.T

```python
T = TypeVar('T')
```

### Classes

<a name="magic_base-data_access-service-base_service_query_mixin-QueryServiceMixin"></a>
### 🅲 magic\_base\.data\_access\.service\.base\_service\_query\_mixin\.QueryServiceMixin

```python
class QueryServiceMixin(ServiceCoreMixin[T]):
```

查询业务操作 Mixin \(Query\)

提供业务层的查询操作接口。
继承自 ServiceCoreMixin，获得核心验证功能。

设计理念:
    与 QueryRepositoryMixin 对应，定义业务层的读操作接口。
    Service 层负责业务逻辑处理，通常内部会调用 QueryRepositoryMixin 的方法。

包含的功能:
    - 根据 ID 查询
    - 列表查询（分页）
    - 动态条件查询
    - 存在性检查
    - 计数统计
    - 分页查询

使用方式:
    class UserService\(QueryServiceMixin\[User\]\):
        def \_\_init\_\_\(self, user\_repo: UserRepository\):
            self\.user\_repo = user\_repo
        
        def get\_by\_id\(self, id: int\) -\> Optional\[Dict\]:
            \# 业务逻辑：权限检查
            if not self\.has\_permission\(id\):
                return None
            return self\.user\_repo\.get\_by\_id\(id\)

**Functions:**

<a name="magic_base-data_access-service-base_service_query_mixin-QueryServiceMixin-get_by_id"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\_query\_mixin\.QueryServiceMixin\.get\_by\_id

```python
def get_by_id(self, id: int) -> Optional[Dict]:
```

根据 ID 获取业务对象

业务逻辑可包含:
- 权限检查：验证当前用户是否有权限查看该对象
- 数据转换：将数据库对象转换为前端需要的格式
- 关联数据加载：加载相关联的其他数据
- 缓存处理：从缓存读取或更新缓存

参数:
    id: 业务对象的主键 ID

返回:
    Optional\[Dict\]: 业务对象字典，未找到时返回 None

示例:
    user = user\_service\.get\_by\_id\(1\)
    if user:
        print\(f"用户: \{user\['name'\]\}, 角色: \{user\['role'\]\}"\)
<a name="magic_base-data_access-service-base_service_query_mixin-QueryServiceMixin-get_list"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\_query\_mixin\.QueryServiceMixin\.get\_list

```python
def get_list(self, filters: Optional[Dict] = None, order_by: Optional[str] = None, limit: Optional[int] = None) -> List[Dict]:
```

获取业务对象列表

支持过滤条件、排序和限制返回数量。

业务逻辑可包含:
- 权限过滤：根据用户权限过滤可见数据
- 数据脱敏：隐藏敏感字段
- 格式化输出：转换日期、枚举等字段格式

参数:
    filters: 过滤条件字典，格式为 \{field\_name: value\}
    order\_by: 排序字段，如 "created\_at DESC"
    limit: 返回记录数量限制

返回:
    List\[Dict\]: 业务对象字典列表

示例:
    users = user\_service\.get\_list\(
        filters=\{'is\_active': True\},
        order\_by='created\_at DESC',
        limit=10
    \)
<a name="magic_base-data_access-service-base_service_query_mixin-QueryServiceMixin-find"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\_query\_mixin\.QueryServiceMixin\.find

```python
def find(self, conditions: Optional[Dict[str, Any]] = None, order_by: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None) -> List[Dict]:
```

动态查询业务对象

灵活的查询方法，支持等值条件、排序、分页。

业务逻辑可包含:
- 动态条件构建
- 数据权限过滤
- 字段映射转换

参数:
    conditions: 查询条件字典，格式为 \{field\_name: value\}
    order\_by: 排序字段，如 "created\_at DESC"
    limit: 返回记录数量限制
    offset: 偏移量，用于分页

返回:
    List\[Dict\]: 业务对象字典列表

示例:
    users = user\_service\.find\(
        conditions=\{'is\_active': True, 'age': 25\},
        order\_by='id DESC',
        limit=20,
        offset=0
    \)
<a name="magic_base-data_access-service-base_service_query_mixin-QueryServiceMixin-find_one"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\_query\_mixin\.QueryServiceMixin\.find\_one

```python
def find_one(self, conditions: Dict[str, Any]) -> Optional[Dict]:
```

查询单个业务对象

根据条件查询第一条匹配的记录。

参数:
    conditions: 查询条件字典，格式为 \{field\_name: value\}

返回:
    Optional\[Dict\]: 业务对象字典，未找到时返回 None

示例:
    user = user\_service\.find\_one\(\{'email': 'alice@example\.com'\}\)
<a name="magic_base-data_access-service-base_service_query_mixin-QueryServiceMixin-exists"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\_query\_mixin\.QueryServiceMixin\.exists

```python
def exists(self, **conditions) -> bool:
```

检查业务对象是否存在

快速检查是否存在满足条件的业务对象，常用于唯一性验证。

参数:
    \*\*conditions: 条件字段和值的键值对

返回:
    bool: True 表示存在，False 表示不存在

示例:
    if user\_service\.exists\(email='alice@example\.com'\):
        raise ValueError\("邮箱已被注册"\)
<a name="magic_base-data_access-service-base_service_query_mixin-QueryServiceMixin-count"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\_query\_mixin\.QueryServiceMixin\.count

```python
def count(self, filters: Optional[Dict] = None) -> int:
```

统计业务对象数量

统计满足条件的业务对象总数，常用于数据概览和分页计算。

参数:
    filters: 过滤条件字典，格式为 \{field\_name: value\}

返回:
    int: 符合条件的业务对象数量

示例:
    active\_count = user\_service\.count\(\{'is\_active': True\}\)
<a name="magic_base-data_access-service-base_service_query_mixin-QueryServiceMixin-paginate"></a>
#### 🅵 magic\_base\.data\_access\.service\.base\_service\_query\_mixin\.QueryServiceMixin\.paginate

```python
def paginate(self, page: int = 1, per_page: int = 20, conditions: Optional[Dict[str, Any]] = None, order_by: str = 'id DESC') -> Dict[str, Any]:
```

分页查询业务对象

实现标准的分页查询，返回包含数据和分页信息的字典。

业务逻辑可包含:
- 分页参数验证
- 数据权限过滤
- 结果集转换

参数:
    page: 当前页码，从 1 开始
    per\_page: 每页记录数
    conditions: 查询条件字典
    order\_by: 排序字段，默认为 "id DESC"

返回:
    Dict\[str, Any\]: 分页结果字典，包含以下键：
        - items: 当前页的数据列表 \(List\[Dict\]\)
        - total: 总记录数 \(int\)
        - page: 当前页码 \(int\)
        - per\_page: 每页记录数 \(int\)
        - pages: 总页数 \(int\)
        - has\_next: 是否有下一页 \(bool\)
        - has\_prev: 是否有上一页 \(bool\)

示例:
    result = user\_service\.paginate\(
        page=2,
        per\_page=10,
        conditions=\{'is\_active': True\},
        order\_by='created\_at DESC'
    \)
    for user in result\['items'\]:
        print\(user\['name'\]\)
    print\(f"第 \{result\['page'\]\}/\{result\['pages'\]\} 页"\)
<a name="magic_base-data_access-util"></a>
## 🅼 magic\_base\.data\_access\.util

- **[Exports](#magic_base-data_access-util-exports)**

<a name="magic_base-data_access-util-exports"></a>
### Exports

- 🅼 [`BaseDBCommand`](#magic_base-data_access-util-BaseDBCommand)
- 🅼 [`DBUtil`](#magic_base-data_access-util-DBUtil)
- 🅼 [`TypeConverter`](#magic_base-data_access-util-TypeConverter)
- 🅼 [`converter`](#magic_base-data_access-util-converter)
- 🅼 [`BaseDataImportCommand`](#magic_base-data_access-util-BaseDataImportCommand)
<a name="magic_base-data_access-util-base_data_command"></a>
## 🅼 magic\_base\.data\_access\.util\.base\_data\_command

- **Classes:**
  - 🅲 [BaseDataImportCommand](#magic_base-data_access-util-base_data_command-BaseDataImportCommand)

### Classes

<a name="magic_base-data_access-util-base_data_command-BaseDataImportCommand"></a>
### 🅲 magic\_base\.data\_access\.util\.base\_data\_command\.BaseDataImportCommand

```python
class BaseDataImportCommand(ABC):
```

数据导入命令基类

提供通用的CSV导入功能和数据解析工具，子类需要实现具体的导入逻辑

**Functions:**

<a name="magic_base-data_access-util-base_data_command-BaseDataImportCommand-__init__"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_data\_command\.BaseDataImportCommand\.\_\_init\_\_

```python
def __init__(self, data_dir: Optional[Path] = None):
```

初始化导入器

**Parameters:**

- **data_dir**: 数据目录路径，默认为项目根目录下的 data 文件夹
<a name="magic_base-data_access-util-base_data_command-BaseDataImportCommand-import_all"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_data\_command\.BaseDataImportCommand\.import\_all

```python
def import_all(self) -> bool:
```

导入所有数据

**Returns:**

- `bool`: True表示导入成功，False表示失败
<a name="magic_base-data_access-util-base_data_command-BaseDataImportCommand-parse_datetime"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_data\_command\.BaseDataImportCommand\.parse\_datetime

```python
def parse_datetime(value: str) -> Optional[datetime]:
```

解析日期时间字符串
<a name="magic_base-data_access-util-base_data_command-BaseDataImportCommand-parse_date"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_data\_command\.BaseDataImportCommand\.parse\_date

```python
def parse_date(value: str) -> Optional[date]:
```

解析日期字符串
<a name="magic_base-data_access-util-base_data_command-BaseDataImportCommand-parse_bool"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_data\_command\.BaseDataImportCommand\.parse\_bool

```python
def parse_bool(value) -> bool:
```

解析布尔值

**Parameters:**

- **value**: 可以是字符串、布尔值或数字

**Returns:**

- `bool`: 解析后的布尔值
<a name="magic_base-data_access-util-base_db_command"></a>
## 🅼 magic\_base\.data\_access\.util\.base\_db\_command

- **Functions:**
  - 🅵 [main](#magic_base-data_access-util-base_db_command-main)
- **Classes:**
  - 🅲 [BaseDBCommand](#magic_base-data_access-util-base_db_command-BaseDBCommand)

### Functions

<a name="magic_base-data_access-util-base_db_command-main"></a>
### 🅵 magic\_base\.data\_access\.util\.base\_db\_command\.main

```python
def main():
```

命令行入口（供子类调用）

### Classes

<a name="magic_base-data_access-util-base_db_command-BaseDBCommand"></a>
### 🅲 magic\_base\.data\_access\.util\.base\_db\_command\.BaseDBCommand

```python
class BaseDBCommand(ABC):
```

数据库命令基类

**Functions:**

<a name="magic_base-data_access-util-base_db_command-BaseDBCommand-__init__"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_db\_command\.BaseDBCommand\.\_\_init\_\_

```python
def __init__(self):
```

初始化基类
<a name="magic_base-data_access-util-base_db_command-BaseDBCommand-model_tables"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_db\_command\.BaseDBCommand\.model\_tables

```python
def model_tables(self) -> List[Type]:
```

子类必须提供模型列表
<a name="magic_base-data_access-util-base_db_command-BaseDBCommand-command_name"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_db\_command\.BaseDBCommand\.command\_name

```python
def command_name(self) -> str:
```

命令名称，可用于帮助信息
<a name="magic_base-data_access-util-base_db_command-BaseDBCommand-extra_commands"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_db\_command\.BaseDBCommand\.extra\_commands

```python
def extra_commands(self) -> Dict[str, Callable]:
```

额外命令映射，子类可重写添加自定义命令
<a name="magic_base-data_access-util-base_db_command-BaseDBCommand-execute"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_db\_command\.BaseDBCommand\.execute

```python
def execute(self, args: Optional[List[str]] = None) -> int:
```

执行命令

**Parameters:**

- **args**: 命令行参数列表，默认使用sys\.argv\[1:\]

**Returns:**

- 退出码，0表示成功，非0表示失败
<a name="magic_base-data_access-util-base_db_table_util"></a>
## 🅼 magic\_base\.data\_access\.util\.base\_db\_table\_util

- **Classes:**
  - 🅲 [DBModelUtil](#magic_base-data_access-util-base_db_table_util-DBModelUtil)
  - 🅲 [DBSqlUtil](#magic_base-data_access-util-base_db_table_util-DBSqlUtil)

### Classes

<a name="magic_base-data_access-util-base_db_table_util-DBModelUtil"></a>
### 🅲 magic\_base\.data\_access\.util\.base\_db\_table\_util\.DBModelUtil

```python
class DBModelUtil:
```

数据库迁移管理

**Functions:**

<a name="magic_base-data_access-util-base_db_table_util-DBModelUtil-create_tables_entities"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_db\_table\_util\.DBModelUtil\.create\_tables\_entities

```python
def create_tables_entities(models: List[Type[MagicBaseEntity]] = None, check_first: bool = True) -> None:
```

通过实体类列表创建对应的表（静态方法版本）

**Parameters:**

- **models**: 模型类列表，如 \[User, Order\]
如果为 None，则创建所有实体对应的表
- **check_first**: 是否先检查表是否存在（默认 True）
<a name="magic_base-data_access-util-base_db_table_util-DBModelUtil-create_tables"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_db\_table\_util\.DBModelUtil\.create\_tables

```python
def create_tables(check_first: bool = True) -> None:
```

创建所有表（便捷方法）

**Parameters:**

- **check_first**: 是否先检查表是否存在
<a name="magic_base-data_access-util-base_db_table_util-DBModelUtil-drop_tables"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_db\_table\_util\.DBModelUtil\.drop\_tables

```python
def drop_tables() -> None:
```

删除所有表（谨慎使用）
<a name="magic_base-data_access-util-base_db_table_util-DBModelUtil-get_current_version"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_db\_table\_util\.DBModelUtil\.get\_current\_version

```python
def get_current_version() -> int:
```

获取当前数据库版本

**Returns:**

- `int`: 当前数据库版本号，如果表不存在则返回 0
<a name="magic_base-data_access-util-base_db_table_util-DBModelUtil-drop_tables_entities"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_db\_table\_util\.DBModelUtil\.drop\_tables\_entities

```python
def drop_tables_entities(models: List[Type[MagicBaseEntity]] = None) -> None:
```

通过实体类列表删除对应的表

**Parameters:**

- **models**: 模型类列表，如 \[User, Order\]
如果为 None，则删除所有实体对应的表
<a name="magic_base-data_access-util-base_db_table_util-DBModelUtil-update_version"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_db\_table\_util\.DBModelUtil\.update\_version

```python
def update_version(version: int) -> None:
```

更新数据库版本

**Parameters:**

- **version**: 要更新的版本号
<a name="magic_base-data_access-util-base_db_table_util-DBModelUtil-run"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_db\_table\_util\.DBModelUtil\.run

```python
def run() -> None:
```

执行迁移
<a name="magic_base-data_access-util-base_db_table_util-DBSqlUtil"></a>
### 🅲 magic\_base\.data\_access\.util\.base\_db\_table\_util\.DBSqlUtil

```python
class DBSqlUtil:
```

数据库初始化工具

**Functions:**

<a name="magic_base-data_access-util-base_db_table_util-DBSqlUtil-init_from_sql"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_db\_table\_util\.DBSqlUtil\.init\_from\_sql

```python
def init_from_sql(sql_file: Path, db_path: Path, force: bool = False) -> None:
```

从 SQL 文件初始化数据库

**Parameters:**

- **sql_file**: SQL 脚本文件路径
- **db_path**: 数据库文件路径
- **force**: 是否强制重建（删除现有数据库）
<a name="magic_base-data_access-util-base_db_table_util-DBSqlUtil-get_current_version"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_db\_table\_util\.DBSqlUtil\.get\_current\_version

```python
def get_current_version(db_path: Path) -> Optional[str]:
```

获取当前数据库版本

**Parameters:**

- **db_path**: 数据库文件路径

**Returns:**

- `Optional[str]`: 版本号字符串，如果数据库不存在或无法获取则返回 None
<a name="magic_base-data_access-util-base_db_util"></a>
## 🅼 magic\_base\.data\_access\.util\.base\_db\_util

- **Classes:**
  - 🅲 [DBUtil](#magic_base-data_access-util-base_db_util-DBUtil)

### Classes

<a name="magic_base-data_access-util-base_db_util-DBUtil"></a>
### 🅲 magic\_base\.data\_access\.util\.base\_db\_util\.DBUtil

```python
class DBUtil:
```

数据库工具类，封装所有数据库操作

提供以下公共方法：
- init\(\): 初始化数据库（如果不存在则创建）
- reinit\(\): 重新初始化数据库（删除现有数据库后重建）
- create\_tables\(\): 创建所有表结构
- recreate\_tables\(\): 删除并重建所有表结构

**Functions:**

<a name="magic_base-data_access-util-base_db_util-DBUtil-__init__"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_db\_util\.DBUtil\.\_\_init\_\_

```python
def __init__(self, backup_callback: Optional[Callable] = None):
```

初始化 DBUtil 实例

**Parameters:**

- **backup_callback**: 可选的自定义备份回调函数，接收 db\_path 参数
<a name="magic_base-data_access-util-base_db_util-DBUtil-db_config"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_db\_util\.DBUtil\.db\_config

```python
def db_config(self):
```

获取数据库配置
<a name="magic_base-data_access-util-base_db_util-DBUtil-db_manager"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_db\_util\.DBUtil\.db\_manager

```python
def db_manager(self):
```

获取数据库管理器
<a name="magic_base-data_access-util-base_db_util-DBUtil-close_connections"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_db\_util\.DBUtil\.close\_connections

```python
def close_connections(self) -> None:
```

关闭所有数据库连接
<a name="magic_base-data_access-util-base_db_util-DBUtil-create_tables"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_db\_util\.DBUtil\.create\_tables

```python
def create_tables(self, models: Optional[List[Type[MagicBaseEntity]]] = None) -> bool:
```

创建表结构
<a name="magic_base-data_access-util-base_db_util-DBUtil-drop_tables"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_db\_util\.DBUtil\.drop\_tables

```python
def drop_tables(self, models: Optional[List[Type[MagicBaseEntity]]] = None) -> bool:
```

删除表结构
<a name="magic_base-data_access-util-base_db_util-DBUtil-recreate_tables"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_db\_util\.DBUtil\.recreate\_tables

```python
def recreate_tables(self, models: Optional[List[Type[MagicBaseEntity]]] = None, backup: bool = True) -> bool:
```

删除并重建所有表结构

**Parameters:**

- **backup**: 是否备份数据（默认 True）

**Returns:**

- `bool`: 是否成功重建
<a name="magic_base-data_access-util-base_db_util-DBUtil-init"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_db\_util\.DBUtil\.init

```python
def init(self) -> bool:
```

初始化数据库（如果不存在则创建）

**Returns:**

- `bool`: 是否成功初始化
<a name="magic_base-data_access-util-base_db_util-DBUtil-reinit"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_db\_util\.DBUtil\.reinit

```python
def reinit(self, backup: bool = True) -> bool:
```

重新初始化数据库（删除现有数据库后重建）

**Parameters:**

- **backup**: 是否备份旧数据库（默认 True）

**Returns:**

- `bool`: 是否成功重新初始化
<a name="magic_base-data_access-util-base_db_util-DBUtil-verify"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_db\_util\.DBUtil\.verify

```python
def verify(self) -> bool:
```

验证数据库完整性

**Returns:**

- `bool`: 数据库是否有效
<a name="magic_base-data_access-util-base_type_converter"></a>
## 🅼 magic\_base\.data\_access\.util\.base\_type\_converter

简单的类型转换工具

- **Classes:**
  - 🅲 [TypeConverter](#magic_base-data_access-util-base_type_converter-TypeConverter)

### Classes

<a name="magic_base-data_access-util-base_type_converter-TypeConverter"></a>
### 🅲 magic\_base\.data\_access\.util\.base\_type\_converter\.TypeConverter

```python
class TypeConverter:
```

简单的类型转换工具

**Functions:**

<a name="magic_base-data_access-util-base_type_converter-TypeConverter-parse_datetime"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_type\_converter\.TypeConverter\.parse\_datetime

```python
def parse_datetime(value: Any) -> Any:
```

解析日期时间字符串为 datetime 对象

**Parameters:**

- **value**: 日期时间字符串或 None

**Returns:**

- datetime 对象或原值
<a name="magic_base-data_access-util-base_type_converter-TypeConverter-get_base_fields"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_type\_converter\.TypeConverter\.get\_base\_fields

```python
def get_base_fields(row: Dict[str, Any]) -> Dict[str, Any]:
```

从行数据中提取基类字段（is\_active, created\_at, updated\_at, deleted\_at）

**Parameters:**

- **row**: CSV/字典行数据

**Returns:**

- 包含基类字段的字典
<a name="magic_base-data_access-util-base_type_converter-TypeConverter-to_bool"></a>
#### 🅵 magic\_base\.data\_access\.util\.base\_type\_converter\.TypeConverter\.to\_bool

```python
def to_bool(value: Any, default: bool = False) -> bool:
```

将各种格式的值转换为布尔值

支持的格式：
- 布尔值: True/False
- 数字: 1/0
- 字符串: 'TRUE'/'FALSE', 'true'/'false', '1'/'0', 'yes'/'no'

**Parameters:**

- **value**: 待转换的值
- **default**: 默认值

**Returns:**

- 转换后的布尔值
<a name="magic_base-detector"></a>
## 🅼 magic\_base\.detector
<a name="magic_base-detector-base_detector"></a>
## 🅼 magic\_base\.detector\.base\_detector

检测器基类 - 定义所有检测器的接口

- **Classes:**
  - 🅲 [DetectorBase](#magic_base-detector-base_detector-DetectorBase)
  - 🅲 [BatchDetectorBase](#magic_base-detector-base_detector-BatchDetectorBase)
  - 🅲 [CachingDetectorBase](#magic_base-detector-base_detector-CachingDetectorBase)

### Classes

<a name="magic_base-detector-base_detector-DetectorBase"></a>
### 🅲 magic\_base\.detector\.base\_detector\.DetectorBase

```python
class DetectorBase(ABC):
```

检测器基类

所有具体硬件检测器（GPUDetector、CPUDetector 等）必须继承此类。

**Functions:**

<a name="magic_base-detector-base_detector-DetectorBase-detect"></a>
#### 🅵 magic\_base\.detector\.base\_detector\.DetectorBase\.detect

```python
def detect(self) -> List[HardwareInfoBase]:
```

检测硬件设备

**Returns:**

- `List[HardwareInfoBase]`: 硬件信息列表
<a name="magic_base-detector-base_detector-DetectorBase-is_supported"></a>
#### 🅵 magic\_base\.detector\.base\_detector\.DetectorBase\.is\_supported

```python
def is_supported(self) -> bool:
```

检查当前平台是否支持此检测器

**Returns:**

- `bool`: 支持返回 True
<a name="magic_base-detector-base_detector-BatchDetectorBase"></a>
### 🅲 magic\_base\.detector\.base\_detector\.BatchDetectorBase

```python
class BatchDetectorBase(ABC):
```

批量检测器基类

同时检测多种硬件的检测器应继承此类。

**Functions:**

<a name="magic_base-detector-base_detector-BatchDetectorBase-detect_all"></a>
#### 🅵 magic\_base\.detector\.base\_detector\.BatchDetectorBase\.detect\_all

```python
def detect_all(self) -> Any:
```

检测所有支持的硬件
<a name="magic_base-detector-base_detector-BatchDetectorBase-detect_with_progress"></a>
#### 🅵 magic\_base\.detector\.base\_detector\.BatchDetectorBase\.detect\_with\_progress

```python
def detect_with_progress(self, callback) -> Any:
```

带进度回调的检测
<a name="magic_base-detector-base_detector-CachingDetectorBase"></a>
### 🅲 magic\_base\.detector\.base\_detector\.CachingDetectorBase

```python
class CachingDetectorBase(ABC):
```

缓存检测器基类（可选接口）

需要实现缓存机制的检测器可以实现此接口。

**Functions:**

<a name="magic_base-detector-base_detector-CachingDetectorBase-clear_cache"></a>
#### 🅵 magic\_base\.detector\.base\_detector\.CachingDetectorBase\.clear\_cache

```python
def clear_cache(self) -> None:
```

清除所有缓存
<a name="magic_base-detector-base_detector-CachingDetectorBase-get_cache_stats"></a>
#### 🅵 magic\_base\.detector\.base\_detector\.CachingDetectorBase\.get\_cache\_stats

```python
def get_cache_stats(self) -> Dict[str, Any]:
```

获取缓存统计信息
<a name="magic_base-detector-base_detector-CachingDetectorBase-set_cache_ttl"></a>
#### 🅵 magic\_base\.detector\.base\_detector\.CachingDetectorBase\.set\_cache\_ttl

```python
def set_cache_ttl(self, seconds: int) -> None:
```

设置缓存有效期
<a name="magic_base-detector-base_hardware_define"></a>
## 🅼 magic\_base\.detector\.base\_hardware\_define

硬件信息基类 - 定义统一的硬件数据接口

- **Classes:**
  - 🅲 [HardwareInfoBase](#magic_base-detector-base_hardware_define-HardwareInfoBase)

### Classes

<a name="magic_base-detector-base_hardware_define-HardwareInfoBase"></a>
### 🅲 magic\_base\.detector\.base\_hardware\_define\.HardwareInfoBase

```python
class HardwareInfoBase(ABC):
```

硬件信息基类

所有具体硬件信息类（GPUInfo、CPUInfo 等）必须继承此类。

**Functions:**

<a name="magic_base-detector-base_hardware_define-HardwareInfoBase-to_dict"></a>
#### 🅵 magic\_base\.detector\.base\_hardware\_define\.HardwareInfoBase\.to\_dict

```python
def to_dict(self) -> Dict[str, Any]:
```

转换为字典格式

**Returns:**

- `Dict[str, Any]`: 字典格式的硬件信息
<a name="magic_base-detector-base_hardware_define-HardwareInfoBase-get_type"></a>
#### 🅵 magic\_base\.detector\.base\_hardware\_define\.HardwareInfoBase\.get\_type

```python
def get_type(self) -> str:
```

获取硬件类型

**Returns:**

- `str`: 硬件类型标识（gpu/cpu/memory 等）
<a name="magic_base-detector-base_hardware_result"></a>
## 🅼 magic\_base\.detector\.base\_hardware\_result

检测结果基类

- **Classes:**
  - 🅲 [DetectionResultBase](#magic_base-detector-base_hardware_result-DetectionResultBase)

### Classes

<a name="magic_base-detector-base_hardware_result-DetectionResultBase"></a>
### 🅲 magic\_base\.detector\.base\_hardware\_result\.DetectionResultBase

```python
class DetectionResultBase(ABC):
```

检测结果基类

所有具体检测结果类必须继承此类。

**Functions:**

<a name="magic_base-detector-base_hardware_result-DetectionResultBase-to_dict"></a>
#### 🅵 magic\_base\.detector\.base\_hardware\_result\.DetectionResultBase\.to\_dict

```python
def to_dict(self) -> Dict[str, Any]:
```

转换为字典
<a name="magic_base-detector-base_hardware_result-DetectionResultBase-to_json"></a>
#### 🅵 magic\_base\.detector\.base\_hardware\_result\.DetectionResultBase\.to\_json

```python
def to_json(self) -> str:
```

转换为 JSON 字符串
<a name="magic_base-detector-base_hardware_result-DetectionResultBase-to_table"></a>
#### 🅵 magic\_base\.detector\.base\_hardware\_result\.DetectionResultBase\.to\_table

```python
def to_table(self) -> str:
```

转换为表格格式（用于 CLI）
<a name="magic_base-detector-base_hardware_result-DetectionResultBase-add_error"></a>
#### 🅵 magic\_base\.detector\.base\_hardware\_result\.DetectionResultBase\.add\_error

```python
def add_error(self, component: str, error: str) -> None:
```

添加错误记录
<a name="magic_base-exceptions"></a>
## 🅼 magic\_base\.exceptions
<a name="magic_base-exceptions-base_exceptions"></a>
## 🅼 magic\_base\.exceptions\.base\_exceptions

异常基类

- **Classes:**
  - 🅲 [MagicBaseError](#magic_base-exceptions-base_exceptions-MagicBaseError)
  - 🅲 [PlatformNotSupportedError](#magic_base-exceptions-base_exceptions-PlatformNotSupportedError)
  - 🅲 [DatabaseError](#magic_base-exceptions-base_exceptions-DatabaseError)
  - 🅲 [ConfigurationError](#magic_base-exceptions-base_exceptions-ConfigurationError)
  - 🅲 [DetectionError](#magic_base-exceptions-base_exceptions-DetectionError)
  - 🅲 [CryptoError](#magic_base-exceptions-base_exceptions-CryptoError)
  - 🅲 [ValidationError](#magic_base-exceptions-base_exceptions-ValidationError)

### Classes

<a name="magic_base-exceptions-base_exceptions-MagicBaseError"></a>
### 🅲 magic\_base\.exceptions\.base\_exceptions\.MagicBaseError

```python
class MagicBaseError(Exception):
```

magic-base 基础异常类
<a name="magic_base-exceptions-base_exceptions-PlatformNotSupportedError"></a>
### 🅲 magic\_base\.exceptions\.base\_exceptions\.PlatformNotSupportedError

```python
class PlatformNotSupportedError(MagicBaseError):
```

当前平台不支持
<a name="magic_base-exceptions-base_exceptions-DatabaseError"></a>
### 🅲 magic\_base\.exceptions\.base\_exceptions\.DatabaseError

```python
class DatabaseError(MagicBaseError):
```

数据库错误
<a name="magic_base-exceptions-base_exceptions-ConfigurationError"></a>
### 🅲 magic\_base\.exceptions\.base\_exceptions\.ConfigurationError

```python
class ConfigurationError(MagicBaseError):
```

配置错误
<a name="magic_base-exceptions-base_exceptions-DetectionError"></a>
### 🅲 magic\_base\.exceptions\.base\_exceptions\.DetectionError

```python
class DetectionError(MagicBaseError):
```

检测错误
<a name="magic_base-exceptions-base_exceptions-CryptoError"></a>
### 🅲 magic\_base\.exceptions\.base\_exceptions\.CryptoError

```python
class CryptoError(MagicBaseError):
```

加密错误
<a name="magic_base-exceptions-base_exceptions-ValidationError"></a>
### 🅲 magic\_base\.exceptions\.base\_exceptions\.ValidationError

```python
class ValidationError(MagicBaseError):
```

验证错误
<a name="magic_base-platform"></a>
## 🅼 magic\_base\.platform
<a name="magic_base-platform-base_platform_adapter"></a>
## 🅼 magic\_base\.platform\.base\_platform\_adapter

平台适配器基类 - 定义不同操作系统的适配接口

- **Classes:**
  - 🅲 [PlatformAdapterBase](#magic_base-platform-base_platform_adapter-PlatformAdapterBase)

### Classes

<a name="magic_base-platform-base_platform_adapter-PlatformAdapterBase"></a>
### 🅲 magic\_base\.platform\.base\_platform\_adapter\.PlatformAdapterBase

```python
class PlatformAdapterBase(ABC):
```

平台适配器基类

封装不同操作系统（Linux、Windows、macOS）的特定实现。
具体适配器由上层模块实现。

**Functions:**

<a name="magic_base-platform-base_platform_adapter-PlatformAdapterBase-get_platform_name"></a>
#### 🅵 magic\_base\.platform\.base\_platform\_adapter\.PlatformAdapterBase\.get\_platform\_name

```python
def get_platform_name(self) -> str:
```

获取平台名称

**Returns:**

- `str`: "linux", "windows", "darwin"
<a name="magic_base-platform-base_platform_adapter-PlatformAdapterBase-get_pci_devices"></a>
#### 🅵 magic\_base\.platform\.base\_platform\_adapter\.PlatformAdapterBase\.get\_pci\_devices

```python
def get_pci_devices(self) -> List[Dict[str, str]]:
```

获取所有 PCI 设备列表

**Returns:**

- `List[Dict]`: 设备列表，包含 address, vendor\_id, device\_id 等
<a name="magic_base-platform-base_platform_adapter-PlatformAdapterBase-get_cpu_info"></a>
#### 🅵 magic\_base\.platform\.base\_platform\_adapter\.PlatformAdapterBase\.get\_cpu\_info

```python
def get_cpu_info(self) -> Dict[str, Any]:
```

获取 CPU 信息

**Returns:**

- `Dict`: 包含 model\_name, vendor\_id, cores 等
<a name="magic_base-platform-base_platform_adapter-PlatformAdapterBase-get_memory_info"></a>
#### 🅵 magic\_base\.platform\.base\_platform\_adapter\.PlatformAdapterBase\.get\_memory\_info

```python
def get_memory_info(self) -> List[Dict[str, Any]]:
```

获取内存信息

**Returns:**

- `List[Dict]`: 内存信息列表
<a name="magic_base-platform-base_platform_adapter-PlatformAdapterBase-get_driver_version"></a>
#### 🅵 magic\_base\.platform\.base\_platform\_adapter\.PlatformAdapterBase\.get\_driver\_version

```python
def get_driver_version(self, device_class: str, device_id: str) -> Optional[str]:
```

获取指定设备的驱动版本

**Parameters:**

- **device_class**: 设备类别（gpu/cpu/network）
- **device_id**: 设备标识符

**Returns:**

- `Optional[str]`: 驱动版本号
<a name="magic_base-platform-base_platform_adapter-PlatformAdapterBase-run_command"></a>
#### 🅵 magic\_base\.platform\.base\_platform\_adapter\.PlatformAdapterBase\.run\_command

```python
def run_command(self, cmd: str, timeout: int = 30) -> Tuple[int, str, str]:
```

执行系统命令

**Parameters:**

- **cmd**: 命令字符串
- **timeout**: 超时时间（秒）

**Returns:**

- `Tuple[int, str, str]`: \(返回码, 标准输出, 标准错误\)
<a name="magic_base-types"></a>
## 🅼 magic\_base\.types
<a name="magic_base-types-base_types"></a>
## 🅼 magic\_base\.types\.base\_types

通用类型定义

- **Classes:**
  - 🅲 [BaseEnum](#magic_base-types-base_types-BaseEnum)

### Classes

<a name="magic_base-types-base_types-BaseEnum"></a>
### 🅲 magic\_base\.types\.base\_types\.BaseEnum

```python
class BaseEnum(Enum):
```

枚举基类

**Functions:**

<a name="magic_base-types-base_types-BaseEnum-from_value"></a>
#### 🅵 magic\_base\.types\.base\_types\.BaseEnum\.from\_value

```python
def from_value(cls, value: str):
```

根据值获取枚举成员
<a name="magic_base-utils"></a>
## 🅼 magic\_base\.utils

- **[Exports](#magic_base-utils-exports)**

<a name="magic_base-utils-exports"></a>
### Exports

- 🅼 [`CSVValidator`](#magic_base-utils-CSVValidator)
<a name="magic_base-utils-base_csv_validator"></a>
## 🅼 magic\_base\.utils\.base\_csv\_validator

- **Classes:**
  - 🅲 [CSVIssue](#magic_base-utils-base_csv_validator-CSVIssue)
  - 🅲 [CSVValidator](#magic_base-utils-base_csv_validator-CSVValidator)

### Classes

<a name="magic_base-utils-base_csv_validator-CSVIssue"></a>
### 🅲 magic\_base\.utils\.base\_csv\_validator\.CSVIssue

```python
class CSVIssue:
```
<a name="magic_base-utils-base_csv_validator-CSVValidator"></a>
### 🅲 magic\_base\.utils\.base\_csv\_validator\.CSVValidator

```python
class CSVValidator:
```

CSV格式验证器

**Functions:**

<a name="magic_base-utils-base_csv_validator-CSVValidator-__init__"></a>
#### 🅵 magic\_base\.utils\.base\_csv\_validator\.CSVValidator\.\_\_init\_\_

```python
def __init__(self, csv_path: Path):
```
<a name="magic_base-utils-base_csv_validator-CSVValidator-validate"></a>
#### 🅵 magic\_base\.utils\.base\_csv\_validator\.CSVValidator\.validate

```python
def validate(self) -> Tuple[bool, List[CSVIssue]]:
```

验证CSV文件格式
<a name="magic_base-utils-base_csv_validator-CSVValidator-print_report"></a>
#### 🅵 magic\_base\.utils\.base\_csv\_validator\.CSVValidator\.print\_report

```python
def print_report(self, max_issues: int = 20):
```
