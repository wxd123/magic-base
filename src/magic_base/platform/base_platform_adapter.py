# magic_base/platform/adapter.py
"""
平台适配器基类 - 定义不同操作系统的适配接口
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple, Optional


class PlatformAdapterBase(ABC):
    """
    平台适配器基类
    
    封装不同操作系统（Linux、Windows、macOS）的特定实现。
    具体适配器由上层模块实现。
    """
    
    @abstractmethod
    def get_platform_name(self) -> str:
        """
        获取平台名称
        
        Returns:
            str: "linux", "windows", "darwin"
        """
        pass
    
    @abstractmethod
    def get_pci_devices(self) -> List[Dict[str, str]]:
        """
        获取所有 PCI 设备列表
        
        Returns:
            List[Dict]: 设备列表，包含 address, vendor_id, device_id 等
        """
        pass
    
    @abstractmethod
    def get_cpu_info(self) -> Dict[str, Any]:
        """
        获取 CPU 信息
        
        Returns:
            Dict: 包含 model_name, vendor_id, cores 等
        """
        pass
    
    @abstractmethod
    def get_memory_info(self) -> List[Dict[str, Any]]:
        """
        获取内存信息
        
        Returns:
            List[Dict]: 内存信息列表
        """
        pass
    
    @abstractmethod
    def get_driver_version(self, device_class: str, device_id: str) -> Optional[str]:
        """
        获取指定设备的驱动版本
        
        Args:
            device_class: 设备类别（gpu/cpu/network）
            device_id: 设备标识符
            
        Returns:
            Optional[str]: 驱动版本号
        """
        pass
    
    @abstractmethod
    def run_command(self, cmd: str, timeout: int = 30) -> Tuple[int, str, str]:
        """
        执行系统命令
        
        Args:
            cmd: 命令字符串
            timeout: 超时时间（秒）
            
        Returns:
            Tuple[int, str, str]: (返回码, 标准输出, 标准错误)
        """
        pass