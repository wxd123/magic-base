# magic_base/detector/result.py
"""
检测结果基类
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class DetectionResultBase(ABC):
    """
    检测结果基类
    
    所有具体检测结果类必须继承此类。
    """
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        pass
    
    @abstractmethod
    def to_json(self) -> str:
        """转换为 JSON 字符串"""
        pass
    
    @abstractmethod
    def to_table(self) -> str:
        """转换为表格格式（用于 CLI）"""
        pass
    
    @abstractmethod
    def add_error(self, component: str, error: str) -> None:
        """添加错误记录"""
        pass