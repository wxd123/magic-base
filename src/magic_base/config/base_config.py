# magic_base/config/base_config.py
"""
配置管理基类

提供配置管理的抽象接口，定义了配置获取、设置、加载、保存和重载的标准方法。
所有具体配置管理实现都应继承此类并实现其抽象方法。
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseConfig(ABC):
    """
    配置管理基类（抽象类）
    
    定义了配置管理器的标准接口，包括配置的读取、写入、持久化等操作。
    子类需要实现具体的配置存储方式（如文件、数据库、远程配置中心等）。
    
    使用示例:
        class MyConfig(BaseConfig):
            def get(self, key: str, default: Any = None) -> Any:
                # 实现获取配置逻辑
                return self._config.get(key, default)
            
            def set(self, key: str, value: Any) -> None:
                # 实现设置配置逻辑
                self._config[key] = value
            
            def load(self) -> Dict[str, Any]:
                # 实现加载配置逻辑
                return self._config
            
            def save(self) -> bool:
                # 实现保存配置逻辑
                return True
            
            def reload(self) -> None:
                # 实现重载配置逻辑
                self.load()
    """
    
    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        根据指定的键名获取对应的配置值。如果键不存在，返回默认值。
        
        Args:
            key (str): 配置键名，支持点号分隔的嵌套键（如 'database.host'）
            default (Any, optional): 当键不存在时返回的默认值。默认为 None
        
        Returns:
            Any: 配置值，如果键不存在则返回 default 参数指定的值
        
        Raises:
            KeyError: 当键不存在且未提供 default 参数时可能抛出（具体取决于子类实现）
        
        Example:
            >>> config.get('app.name')
            'MyApp'
            >>> config.get('app.timeout', 30)
            30
        """
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """
        设置配置值
        
        将指定的键值对写入配置中。如果键已存在，则覆盖原有值；
        如果键不存在，则创建新配置项。
        
        Args:
            key (str): 配置键名，支持点号分隔的嵌套键（如 'database.host'）
            value (Any): 要设置的配置值，可以是任意可序列化的 Python 对象
        
        Raises:
            TypeError: 当 value 类型不被支持时抛出
            ValueError: 当 key 格式无效时抛出
        
        Example:
            >>> config.set('app.debug', True)
            >>> config.set('database.port', 3306)
        """
        pass
    
    @abstractmethod
    def load(self) -> Dict[str, Any]:
        """
        加载配置
        
        从存储介质（如文件、数据库等）中读取配置数据并加载到内存中。
        通常用于初始化或手动触发配置加载。
        
        Returns:
            Dict[str, Any]: 加载后的配置字典，包含所有配置项
        
        Raises:
            FileNotFoundError: 当配置文件不存在时抛出
            PermissionError: 当没有读取权限时抛出
            json.JSONDecodeError: 当配置文件格式错误时抛出（针对 JSON 格式）
        
        Example:
            >>> config = MyConfig()
            >>> config.load()
            {'app': {'name': 'MyApp', 'version': '1.0'}}
        """
        pass
    
    @abstractmethod
    def save(self) -> bool:
        """
        保存配置
        
        将当前内存中的配置持久化到存储介质中（如文件、数据库等）。
        
        Returns:
            bool: 保存成功返回 True，失败返回 False
        
        Raises:
            PermissionError: 当没有写入权限时抛出
            IOError: 当写入过程中发生 I/O 错误时抛出
        
        Example:
            >>> if config.save():
            ...     print("配置保存成功")
            ... else:
            ...     print("配置保存失败")
        """
        pass
    
    @abstractmethod
    def reload(self) -> None:
        """
        重新加载配置
        
        丢弃当前内存中的配置，重新从存储介质加载最新的配置数据。
        通常用于配置热更新场景。
        
        注意：重新加载会覆盖所有未保存的配置修改，请谨慎使用。
        
        Raises:
            FileNotFoundError: 当配置文件不存在时抛出
            PermissionError: 当没有读取权限时抛出
        
        Example:
            >>> # 配置文件被外部修改后
            >>> config.reload()  # 重新加载最新配置
            >>> config.get('app.debug')
            True
        """
        pass