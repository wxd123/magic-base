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
- 🅼 [magic\_base\.data\_access\.model\.base\_model](#magic_base-data_access-model-base_model)
- 🅼 [magic\_base\.data\_access\.repository](#magic_base-data_access-repository)
- 🅼 [magic\_base\.data\_access\.repository\.base\_repository](#magic_base-data_access-repository-base_repository)
- 🅼 [magic\_base\.data\_access\.service](#magic_base-data_access-service)
- 🅼 [magic\_base\.data\_access\.service\.base\_service](#magic_base-data_access-service-base_service)
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

<a name="magic_base"></a>
## 🅼 magic\_base
<a name="magic_base-config"></a>
## 🅼 magic\_base\.config
<a name="magic_base-config-base_config"></a>
## 🅼 magic\_base\.config\.base\_config

配置管理基类

- **Classes:**
  - 🅲 [ConfigBase](#magic_base-config-base_config-ConfigBase)

### Classes

<a name="magic_base-config-base_config-ConfigBase"></a>
### 🅲 magic\_base\.config\.base\_config\.ConfigBase

```python
class ConfigBase(ABC):
```

配置管理基类

**Functions:**

<a name="magic_base-config-base_config-ConfigBase-get"></a>
#### 🅵 magic\_base\.config\.base\_config\.ConfigBase\.get

```python
def get(self, key: str, default: Any = None) -> Any:
```

获取配置值
<a name="magic_base-config-base_config-ConfigBase-set"></a>
#### 🅵 magic\_base\.config\.base\_config\.ConfigBase\.set

```python
def set(self, key: str, value: Any) -> None:
```

设置配置值
<a name="magic_base-config-base_config-ConfigBase-load"></a>
#### 🅵 magic\_base\.config\.base\_config\.ConfigBase\.load

```python
def load(self) -> Dict[str, Any]:
```

加载配置
<a name="magic_base-config-base_config-ConfigBase-save"></a>
#### 🅵 magic\_base\.config\.base\_config\.ConfigBase\.save

```python
def save(self) -> bool:
```

保存配置
<a name="magic_base-config-base_config-ConfigBase-reload"></a>
#### 🅵 magic\_base\.config\.base\_config\.ConfigBase\.reload

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

数据访问基类 - 提供数据库连接和会话管理

- **Classes:**
  - 🅲 [DatabaseConfigBase](#magic_base-data_access-config-base_database_config-DatabaseConfigBase)
  - 🅲 [DatabaseManagerBase](#magic_base-data_access-config-base_database_config-DatabaseManagerBase)

### Classes

<a name="magic_base-data_access-config-base_database_config-DatabaseConfigBase"></a>
### 🅲 magic\_base\.data\_access\.config\.base\_database\_config\.DatabaseConfigBase

```python
class DatabaseConfigBase(ABC):
```

数据库配置基类

**Functions:**

<a name="magic_base-data_access-config-base_database_config-DatabaseConfigBase-get_connection_string"></a>
#### 🅵 magic\_base\.data\_access\.config\.base\_database\_config\.DatabaseConfigBase\.get\_connection\_string

```python
def get_connection_string(self) -> str:
```

获取数据库连接字符串
<a name="magic_base-data_access-config-base_database_config-DatabaseConfigBase-get_engine_options"></a>
#### 🅵 magic\_base\.data\_access\.config\.base\_database\_config\.DatabaseConfigBase\.get\_engine\_options

```python
def get_engine_options(self) -> Dict[str, Any]:
```

获取引擎选项
<a name="magic_base-data_access-config-base_database_config-DatabaseManagerBase"></a>
### 🅲 magic\_base\.data\_access\.config\.base\_database\_config\.DatabaseManagerBase

```python
class DatabaseManagerBase(ABC):
```

数据库管理器基类

提供统一的会话管理，具体模块继承此类实现自己的数据库管理。

**Functions:**

<a name="magic_base-data_access-config-base_database_config-DatabaseManagerBase-__init__"></a>
#### 🅵 magic\_base\.data\_access\.config\.base\_database\_config\.DatabaseManagerBase\.\_\_init\_\_

```python
def __init__(self, config: DatabaseConfigBase):
```
<a name="magic_base-data_access-config-base_database_config-DatabaseManagerBase-engine"></a>
#### 🅵 magic\_base\.data\_access\.config\.base\_database\_config\.DatabaseManagerBase\.engine

```python
def engine(self) -> Engine:
```

获取数据库引擎（延迟初始化）
<a name="magic_base-data_access-config-base_database_config-DatabaseManagerBase-SessionLocal"></a>
#### 🅵 magic\_base\.data\_access\.config\.base\_database\_config\.DatabaseManagerBase\.SessionLocal

```python
def SessionLocal(self) -> sessionmaker:
```

获取会话工厂
<a name="magic_base-data_access-config-base_database_config-DatabaseManagerBase-session"></a>
#### 🅵 magic\_base\.data\_access\.config\.base\_database\_config\.DatabaseManagerBase\.session

```python
def session(self) -> Generator[Session, None, None]:
```

获取数据库会话（上下文管理器）
<a name="magic_base-data_access-config-base_database_config-DatabaseManagerBase-get_session"></a>
#### 🅵 magic\_base\.data\_access\.config\.base\_database\_config\.DatabaseManagerBase\.get\_session

```python
def get_session(self) -> Session:
```

获取数据库会话（手动管理）
<a name="magic_base-data_access-config-base_database_config-DatabaseManagerBase-init_database"></a>
#### 🅵 magic\_base\.data\_access\.config\.base\_database\_config\.DatabaseManagerBase\.init\_database

```python
def init_database(self, drop_first: bool = False):
```

初始化数据库

具体模块需要实现此方法，创建自己的表。
<a name="magic_base-data_access-manager"></a>
## 🅼 magic\_base\.data\_access\.manager
<a name="magic_base-data_access-manager-base_database_manager"></a>
## 🅼 magic\_base\.data\_access\.manager\.base\_database\_manager
<a name="magic_base-data_access-model"></a>
## 🅼 magic\_base\.data\_access\.model
<a name="magic_base-data_access-model-base_model"></a>
## 🅼 magic\_base\.data\_access\.model\.base\_model

ORM 基类 - 所有数据模型继承此基类
<a name="magic_base-data_access-repository"></a>
## 🅼 magic\_base\.data\_access\.repository
<a name="magic_base-data_access-repository-base_repository"></a>
## 🅼 magic\_base\.data\_access\.repository\.base\_repository

仓储基类 - 提供通用 CRUD 操作模板

- **Classes:**
  - 🅲 [BaseRepository](#magic_base-data_access-repository-base_repository-BaseRepository)

### Classes

<a name="magic_base-data_access-repository-base_repository-BaseRepository"></a>
### 🅲 magic\_base\.data\_access\.repository\.base\_repository\.BaseRepository

```python
class BaseRepository(ABC, Generic[ModelType]):
```

仓储基类

提供通用的 CRUD 模板方法，具体模块需要继承并绑定自己的 Model。

**Functions:**

<a name="magic_base-data_access-repository-base_repository-BaseRepository-__init__"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\.BaseRepository\.\_\_init\_\_

```python
def __init__(self, session: Session, model_class: Type[ModelType]):
```
<a name="magic_base-data_access-repository-base_repository-BaseRepository-get_by_id"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\.BaseRepository\.get\_by\_id

```python
def get_by_id(self, id: int) -> Optional[ModelType]:
```

根据 ID 获取
<a name="magic_base-data_access-repository-base_repository-BaseRepository-get_by"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\.BaseRepository\.get\_by

```python
def get_by(self, **kwargs) -> Optional[ModelType]:
```

根据条件获取一条
<a name="magic_base-data_access-repository-base_repository-BaseRepository-get_all"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\.BaseRepository\.get\_all

```python
def get_all(self, **kwargs) -> List[ModelType]:
```

获取所有符合条件的
<a name="magic_base-data_access-repository-base_repository-BaseRepository-add"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\.BaseRepository\.add

```python
def add(self, instance: ModelType) -> ModelType:
```

添加
<a name="magic_base-data_access-repository-base_repository-BaseRepository-add_all"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\.BaseRepository\.add\_all

```python
def add_all(self, instances: List[ModelType]) -> List[ModelType]:
```

批量添加
<a name="magic_base-data_access-repository-base_repository-BaseRepository-update"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\.BaseRepository\.update

```python
def update(self, id: int, **kwargs) -> Optional[ModelType]:
```

更新
<a name="magic_base-data_access-repository-base_repository-BaseRepository-delete"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\.BaseRepository\.delete

```python
def delete(self, id: int) -> bool:
```

删除
<a name="magic_base-data_access-repository-base_repository-BaseRepository-exists"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\.BaseRepository\.exists

```python
def exists(self, **kwargs) -> bool:
```

检查是否存在
<a name="magic_base-data_access-repository-base_repository-BaseRepository-count"></a>
#### 🅵 magic\_base\.data\_access\.repository\.base\_repository\.BaseRepository\.count

```python
def count(self, **kwargs) -> int:
```

计数
<a name="magic_base-data_access-service"></a>
## 🅼 magic\_base\.data\_access\.service
<a name="magic_base-data_access-service-base_service"></a>
## 🅼 magic\_base\.data\_access\.service\.base\_service
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
