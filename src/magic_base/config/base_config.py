# magic_base/config/base_config.py
"""
配置管理基类
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class ConfigBase(ABC):
    """配置管理基类"""
    
    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """设置配置值"""
        pass
    
    @abstractmethod
    def load(self) -> Dict[str, Any]:
        """加载配置"""
        pass
    
    @abstractmethod
    def save(self) -> bool:
        """保存配置"""
        pass
    
    @abstractmethod
    def reload(self) -> None:
        """重新加载配置"""
        pass