magic-base 架构

定位

magic-base 是 magic 生态的基础设施库。

它为零依赖、纯契约之外的所有项目提供可继承的实现底座：配置、加密、数据访问、检测、平台适配、异常、类型、工具。

它不是组件，也不是应用。它是被继承的基类库——任何 magic 项目通过继承它获得统一的持久化能力、统一的异常体系、统一的配置接口，而不必自己重写。

依赖：无外部 magic 项目依赖。它是生态中最底层的实现库。

包名：magic-base。
Python 包名：magic_base。
版本：0.1.0。
许可证：MIT。
Python 要求：3.11 及以上。

待完成工作：protocol 迁移

当前 src/magic_base/protocol/ 目录内置了一份协议类型副本，包括：

pipeline/cmd/command.py，Command。
pipeline/data_class/command_config.py，CommandConfig。
pipeline/data_class/step.py，Step。
pipeline/model.py。
request/request.py。
result/result.py，Result。
result/result_helper.py。

这些类型属于跨项目共享类型，按 magic-protocol 的准入标准，应当定义在 magic-protocol，而不是内置在 magic-base。

迁移方向：

一，这些类型全部迁移到 magic-protocol。
二，magic-base 改为依赖 magic-protocol，从 magic-protocol 导入这些类型。
三，删除 magic-base 内的 protocol 目录。

迁移原因：

一，跨项目共享类型必须唯一定义，不能有副本。
二，magic-base 的定位是基础设施库，不应承载协议类型。
三，magic-protocol 的准入标准是"跨项目引用"，Command、CommandConfig、Result 等符合标准。
四，避免类型分叉：如果 magic-base 和 magic-protocol 各有一份，会出现两个同名不同类型，破坏生态一致性。

迁移影响：

一，magic-base 增加对 magic-protocol 的依赖。
二，所有从 magic_base.protocol 导入这些类型的代码，改为从 magic_protocol 导入。
三，magic-pipeline 等消费方，改为从 magic-protocol 导入。

状态：待完成。

职责

提供：

配置管理基类：BaseConfig。
加密与证书基类：CryptoBase、CertValidatorBase。
数据访问基础设施：Entity、Repository、Service、Manager、Config、Util。
硬件检测基类：DetectorBase、BatchDetectorBase、CachingDetectorBase、HardwareInfoBase、DetectionResultBase。
平台适配基类：PlatformAdapterBase。
异常基类：MagicBaseError 及派生。
枚举基类：BaseEnum。
工具：CSVValidator。

不做：

不做解析（归具体项目）。
不做校验（归具体项目）。
不做规范化（归具体项目）。
不做渲染（归具体项目）。
不定义跨项目共享的类型（归 magic-protocol）。
不定义业务 schema（归应用）。
不实现具体业务逻辑。

项目结构

src/magic_base/
  __init__.py
  py.typed

  config/                       配置管理
    base_config.py              BaseConfig

  constants/                    常量
    tables.py                   表名

  context/                      上下文
    application_context.py      ApplicationContext

  crypto/                       加密与证书
    base_cert.py                CertValidatorBase
    base_crypto.py              CryptoBase

  data_access/                  数据访问
    config/                     数据库配置
      base_database_config.py   DatabaseType、BaseDatabaseConfig、MagicDatabaseConfig
    manager/                    数据库管理器
      base_database_manager.py  BaseDatabaseManager、MagicDatabaseManager
    model/                      模型基类
      base_dataclass.py
      base_entity.py            BaseEntity、MagicBaseEntity
    repository/                 仓储
      base_repository_core_mixin.py    RepositoryCoreMixin
      base_repository_cud_mixin.py     CUDRepositoryMixin
      base_repository_query_mixin.py   QueryRepositoryMixin
      base_repository.py               BaseRepository、MagicBaseRepository
      base_sqlalchemy_repository.py    SQLAlchemyRepository
    service/                    服务
      base_service_core_mixin.py       ServiceCoreMixin
      base_service_cud_mixin.py        CUDServiceMixin
      base_service_query_mixin.py      QueryServiceMixin
      base_service.py                  BaseService、MagicBaseService
    util/                       数据访问工具
      base_data_command.py      BaseDataImportCommand
      base_db_command.py        BaseDBCommand
      base_db_table_util.py     DBModelUtil、DBSqlUtil
      base_db_util.py           DBUtil
      base_type_converter.py    TypeConverter

  detector/                     硬件检测
    base_detector.py            DetectorBase、BatchDetectorBase、CachingDetectorBase
    base_hardware_define.py     HardwareInfoBase
    base_hardware_result.py     DetectionResultBase

  exceptions/                   异常
    base_exceptions.py          MagicBaseError 及派生

  i18n/                         国际化
    factory.py
    language.py
    provider.py
    languages/
      en_US.py
      zh_CN.py

  platform/                     平台适配
    base_platform_adapter.py    PlatformAdapterBase

  protocol/                     协议（待迁移到 magic-protocol）
    pipeline/                   编排协议
      cmd/command.py            Command
      data_class/command_config.py  CommandConfig
      data_class/step.py        Step
      model.py
    request/request.py
    result/                     Result
      result.py
      result_helper.py

  types/                        类型
    base_types.py               BaseEnum

  utils/                        工具
    base_csv_validator.py       CSVValidator、CSVIssue

模块职责

config/

配置管理基类。BaseConfig 提供 get、set、load、save、reload 接口。

constants/

常量。tables.py 定义表名。

context/

应用上下文。ApplicationContext。

crypto/

加密与证书基类。CryptoBase 提供 encrypt、decrypt、hash、generate_key。CertValidatorBase 提供 verify_signature、get_cert_info、verify_chain。

data_access/

数据访问基础设施，核心模块。

config 子模块：

DatabaseType 枚举：SQLITE、POSTGRESQL、MYSQL。
BaseDatabaseConfig 抽象基类：get_connection_string、get_engine_options、get_db_path。
MagicDatabaseConfig：默认实现，支持三种数据库，自动处理目录创建与路径解析。
类属性 MAGIC_DATA_DIR 指向用户家目录下 magic/data。

manager 子模块：

BaseDatabaseManager 抽象基类：engine、SessionLocal、session 上下文管理器、get_session、close、上下文管理器协议、init_database。
MagicDatabaseManager：共享实现，提供 set_base、init_database。

model 子模块：

BaseEntity：ORM 模型抽象基类，提供 to_dict、from_dict、validate、get_table_name。
MagicBaseEntity：SQLAlchemy 声明式基类，含通用字段 id、is_active、created_at、updated_at、deleted_at。

repository 子模块，采用 Mixin 组合：

RepositoryCoreMixin：核心基础设施，模型类提取、会话管理、表名推断。
CUDRepositoryMixin：ORM 写操作，create、create_from_model、update、update_from_model、delete、batch_create、batch_update、get_orm_instance。
QueryRepositoryMixin：原生 SQL 读操作，fetch_one、fetch_all、get_by_id、get_all、find、find_one、exists、count、paginate。
BaseRepository：组合 CUD 与 Query 两个 Mixin，抽象基类，不能直接实例化。
MagicBaseRepository：Magic 生态统一 Repository 基类，含 ABC 抽象标记。
SQLAlchemyRepository：可选的 SQLAlchemy 仓储实现，ORM 与参数化 SQL 两种方式。

service 子模块，与 repository 对应：

ServiceCoreMixin：核心验证接口 validate。
CUDServiceMixin：业务写操作，create、create_from_model、update、update_from_model、delete、get_orm_instance、batch_create、batch_update。
QueryServiceMixin：业务读操作，get_by_id、get_list、find、find_one、exists、count、paginate。
BaseService：Service 抽象基类，透传 Repository 的基础 CRUD。
MagicBaseService：Magic 生态统一 Service 基类。

util 子模块：

BaseDataImportCommand：CSV 导入基类，import_all、parse_datetime、parse_date、parse_bool。
BaseDBCommand：数据库命令基类，model_tables、command_name、extra_commands、execute。
DBModelUtil：数据库迁移管理，create_tables、create_tables_entities、drop_tables、drop_tables_entities、get_current_version、update_version、run。
DBSqlUtil：从 SQL 文件初始化数据库，init_from_sql、get_current_version。
DBUtil：数据库工具封装，init、reinit、create_tables、drop_tables、recreate_tables、verify、close_connections。
TypeConverter：类型转换，parse_datetime、get_base_fields、to_bool。

detector/

硬件检测基类。DetectorBase 提供 detect、is_supported。BatchDetectorBase 提供 detect_all、detect_with_progress。CachingDetectorBase 提供 clear_cache、get_cache_stats、set_cache_ttl。HardwareInfoBase 提供 to_dict、get_type。DetectionResultBase 提供 to_dict、to_json、to_table、add_error。

exceptions/

异常基类。MagicBaseError 及派生：PlatformNotSupportedError、DatabaseError、ConfigurationError、DetectionError、CryptoError、ValidationError。

i18n/

国际化。factory、language、provider，及 en_US、zh_CN 两套语言。

platform/

平台适配基类。PlatformAdapterBase 提供 get_platform_name、get_pci_devices、get_cpu_info、get_memory_info、get_driver_version、run_command。

protocol/

内置协议副本。含 pipeline（Command、CommandConfig、Step、Model）、request、result（Result、result_helper）。

此目录待迁移到 magic-protocol，详见"待完成工作：protocol 迁移"。

types/

类型。BaseEnum，提供 from_value。

utils/

工具。CSVValidator、CSVIssue。

数据访问设计

设计理念

写操作使用 ORM：获得对象关系映射的便利性、自动事务管理、关联关系处理。
读操作使用原生 SQL：获得更好的性能、更灵活的查询、复杂 JOIN 支持。

Mixin 组合

Repository 与 Service 均采用 Mixin 组合，职责分离，可灵活组合。

BaseRepository 继承关系：

BaseRepository
  CUDRepositoryMixin
    RepositoryCoreMixin
  QueryRepositoryMixin
    RepositoryCoreMixin

可以只继承 QueryRepositoryMixin 获得只读能力。

泛型自动提取

RepositoryCoreMixin 与 BaseRepository 在 __new__ 中自动提取子类指定的泛型模型类，无需手动设置。

软删除

delete 方法支持软删除（soft=True，默认）与硬删除（soft=False）。软删除设置 is_active 为 False。

数据库配置

MagicDatabaseConfig 是默认实现，支持 SQLite、PostgreSQL、MySQL。

SQLite 默认路径为 magic.db，可自定义。
PostgreSQL 默认 host 为 localhost，port 为 5432。
MySQL 默认 host 为 localhost，port 为 3306。

SQLite 自动添加 connect_args 的 check_same_thread 为 False，支持多线程。

是否与其他项目共享 DB 是部署选择，不是架构约束。配置能力使这个问题不成为问题。

通用字段

MagicBaseEntity 提供统一字段：

id 自增主键
is_active 是否激活，带索引
created_at 创建时间
updated_at 更新时间
deleted_at 软删除时间戳

核心原则

一，基础设施库，不是组件，不是应用。
二，只提供机制，不提供业务 schema。
三，跨项目共享类型归 magic-protocol，本库不定义。
四，写用 ORM，读用 SQL，各取所长。
五，Mixin 组合，职责分离，可灵活裁剪。
六，配置能力开放，DB 共享与否是部署选择。
七，不做解析、校验、规范化、渲染。
八，不做具体业务逻辑。
九，最小覆盖约定：继承项目应尽量少覆盖 base 的通用实现，除非 base 不满足要求。

覆盖时必须在继承项目自己的两处文档标注：

继承项目的架构文档，记录覆盖点、原因、是否临时、base 是否计划补齐、对架构的影响。
继承项目的 api 文档，记录覆盖了 base 的哪个方法、签名或行为差异、调用方注意事项。

base 的架构文档只声明此约定；base 的 api 文档只描述 base 自身能力，不记录任何继承项目的覆盖。

与其他项目的关系

magic-protocol：类型契约底座，magic-base 的 protocol 目录待迁移到此。
magic-pipeline：通用编排，其 data_access 继承 magic-base，并遵守最小覆盖约定，覆盖记录在 pipeline 自己的架构文档与 api 文档。
magic-ast：语义专用，可使用 magic-base 的配置、异常等，遵守最小覆盖约定，覆盖记录在 ast 自己的架构文档与 api 文档。
magic-codegen：应用，其数据层继承 magic-base 的 Entity、Repository、Service、Manager、Config，遵守最小覆盖约定，覆盖记录在 codegen 自己的架构文档与 api 文档。

magic-base 是"实现底座"，与 magic-protocol 的"契约底座"互补。

已知问题

一，protocol 目录内置了 Command、CommandConfig、Result、Step、Model 等协议类型。这些属于跨项目共享类型，必须迁移到 magic-protocol。当前是待完成工作。

二，i18n 目录提供国际化，但 magic-pipeline 的 messages 目录也提供国际化。两者是否需要统一，需确认。

三，constants/tables.py 与各项目自己的表名定义的关系，需确认。

四，context/application_context.py 的定位，需确认。

演进方向

短期：

完成 protocol 迁移：删除 magic_base/protocol 目录，改为依赖 magic-protocol。
确认 i18n 与 pipeline messages 的关系。
补全 py.typed 与 schema 打包。

中期：

扩展 provider 相关支持，若需要。
完善 data_access 的文档与测试。

长期：

保持基础设施库定位，不引入业务逻辑。
保持"机制提供者"角色，不定义 schema。

一句话总纲

magic-base 是 magic 生态的基础设施库，提供可继承的实现底座：配置、加密、数据访问、检测、平台适配、异常、类型、工具；数据访问采用 Mixin 组合，写用 ORM、读用 SQL，提供统一的 Entity、Repository、Service、Manager、Config；它是"实现底座"，与 magic-protocol 的"契约底座"互补，被 pipeline、ast、codegen 继承使用；继承项目遵守最小覆盖约定，覆盖记录在继承项目自己的架构文档与 api 文档；当前 protocol 目录内的协议类型待迁移到 magic-protocol，这是待完成工作。