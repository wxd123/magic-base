# magic_base/protocol/pipeline/data_class/step.py

from abc import ABC, abstractmethod
from typing import Optional

class Step(ABC):
    """步骤基类 - 只定义接口"""
    
    @property
    @abstractmethod
    def id(self) -> str:
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def type(self) -> str:
        pass