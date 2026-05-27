# magic-base/magic_base/i18n/__init__.py
from .provider import MessageProvider
from .factory import message_factory, MessageFactory
from .language import get_system_language, get_message_provider

# 默认消息实例
msg = get_message_provider()

__all__ = [
    "MessageProvider",
    "message_factory",
    "MessageFactory", 
    "get_system_language",
    "get_message_provider",
    "msg",
]