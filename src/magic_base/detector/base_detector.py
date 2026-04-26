# magic_base/detector/base.py
"""
检测器基类 - 定义所有检测器的接口
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from .base_hardware_define import HardwareInfoBase


class DetectorBase(ABC):
    """
    检测器基类
    
    所有具体硬件检测器（GPUDetector、CPUDetector 等）必须继承此类。
    
    Example:
        >>> class MyDetector(DetectorBase):
        ...     def detect(self) -> List[HardwareInfoBase]:
        ...         return [MyHardwareInfo(...)]
        ...     
        ...     def is_supported(self) -> bool:
        ...         return True
    """
    
    @abstractmethod
    def detect(self) -> List[HardwareInfoBase]:
        """
        检测硬件设备
        
        Returns:
            List[HardwareInfoBase]: 硬件信息列表
        """
        pass
    
    @abstractmethod
    def is_supported(self) -> bool:
        """
        检查当前平台是否支持此检测器
        
        Returns:
            bool: 支持返回 True
        """
        pass


class BatchDetectorBase(ABC):
    """
    批量检测器基类
    
    同时检测多种硬件的检测器应继承此类。
    """
    
    @abstractmethod
    def detect_all(self) -> Any:
        """检测所有支持的硬件"""
        pass
    
    @abstractmethod
    def detect_with_progress(self, callback) -> Any:
        """带进度回调的检测"""
        pass


class CachingDetectorBase(ABC):
    """
    缓存检测器基类（可选接口）
    
    需要实现缓存机制的检测器可以实现此接口。
    """
    
    @abstractmethod
    def clear_cache(self) -> None:
        """清除所有缓存"""
        pass
    
    @abstractmethod
    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        pass
    
    @abstractmethod
    def set_cache_ttl(self, seconds: int) -> None:
        """设置缓存有效期"""
        pass