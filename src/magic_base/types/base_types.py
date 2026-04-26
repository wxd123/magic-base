# magic_base/types/common.py
"""
通用类型定义
"""

from typing import Dict, Any, Optional, Union, List, Tuple
from enum import Enum

# 常用类型别名
JSONDict = Dict[str, Any]
JSONList = List[Any]
Primitive = Union[str, int, float, bool, None]

# 枚举基类
class BaseEnum(Enum):
    """枚举基类"""
    
    @classmethod
    def from_value(cls, value: str):
        """根据值获取枚举成员"""
        for member in cls:
            if member.value == value:
                return member
        return None