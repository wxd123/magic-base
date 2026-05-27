# magic-base/magic_base/i18n/provider.py
from abc import ABC, abstractmethod
from typing import Dict

class MessageProvider(ABC):
    """消息提供者抽象基类"""
    
    @property
    @abstractmethod
    def messages(self) -> Dict[str, str]:
        """返回消息字典"""
        pass
    
    def get(self, key: str, **kwargs) -> str:
        """获取格式化后的消息"""
        template = self.messages.get(key)
        if not template:
            return f"Unknown message key: {key}"
        return template.format(**kwargs)