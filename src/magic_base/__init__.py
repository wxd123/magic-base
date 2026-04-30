# magic_base/__init__.py

from magic_base.config.base_config import ConfigBase
from magic_base.data_access.config.base_database_config import DatabaseConfigBase, MagicDatabaseConfig
from magic_base.data_access.manager.base_database_manager import DatabaseManagerBase, MagicDatabaseManager
from magic_base.data_access.model.base_model import MagicBaseModel
from magic_base.data_access.repository.base_repository import BaseRepository
from magic_base.data_access.service.base_service import BaseService

__all__ = ['ConfigBase', 
           'DatabaseConfigBase', 'MagicDatabaseConfig',
           'DatabaseManagerBase', 'MagicDatabaseManager'
           'MagicBaseModel', 
           'BaseRepository', 
           'BaseService']