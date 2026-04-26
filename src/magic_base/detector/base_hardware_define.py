# magic_base/detector/hardware.py
"""
硬件信息基类 - 定义统一的硬件数据接口
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class HardwareInfoBase(ABC):
    """
    硬件信息基类
    
    所有具体硬件信息类（GPUInfo、CPUInfo 等）必须继承此类。
    """
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典格式
        
        Returns:
            Dict[str, Any]: 字典格式的硬件信息
        """
        pass
    
    @abstractmethod
    def get_type(self) -> str:
        """
        获取硬件类型
        
        Returns:
            str: 硬件类型标识（gpu/cpu/memory 等）
        """
        pass