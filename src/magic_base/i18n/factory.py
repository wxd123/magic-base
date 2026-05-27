# magic-base/magic_base/i18n/factory.py
from typing import Dict, Type, Optional
from .provider import MessageProvider

class MessageFactory:
    """消息工厂"""
    
    _providers: Dict[str, Type[MessageProvider]] = {}
    
    @classmethod
    def register(cls, language: str, provider_class: Type[MessageProvider]):
        """注册语言提供者"""
        cls._providers[language] = provider_class
    
    @classmethod
    def get(cls, language: str = "zh") -> MessageProvider:
        """获取消息提供者实例"""
        provider_class = cls._providers.get(language)
        if not provider_class:
            raise ValueError(f"Unsupported language: {language}. Supported: {list(cls._providers.keys())}")
        return provider_class()
    
    @classmethod
    def supported_languages(cls) -> list:
        """返回支持的语言列表"""
        return list(cls._providers.keys())


# 全局工厂实例
message_factory = MessageFactory()