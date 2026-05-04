# magic_base/__init__.py

from magic_base.config.base_config import ConfigBase
from magic_base.data_access.config.base_database_config import DatabaseConfigBase, MagicDatabaseConfig
from magic_base.data_access.manager.base_database_manager import DatabaseManagerBase, MagicDatabaseManager
from magic_base.data_access.model.base_model import Base, BaseModel, MagicBaseModel
from magic_base.data_access.repository.base_repository import BaseRepository, MagicBaseRepository
from magic_base.data_access.service.base_service import BaseService, MagicBaseService
from magic_base.context.application_context import ApplicationContext

__all__ = [
    'ApplicationContext', 
    'ConfigBase', 'DatabaseConfigBase', 'MagicDatabaseConfig',
    'DatabaseManagerBase', 'MagicDatabaseManager',
    'Base', 'BaseModel', 'MagicBaseModel', 
    'BaseRepository', 'MagicBaseRepository',
    'BaseService', 'MagicBaseService'
          ]