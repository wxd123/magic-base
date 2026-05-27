# magic_base/i18n/language.py
import locale
import os
from typing import Optional

from magic_base.i18n.provider import MessageProvider
from .factory import message_factory
from .languages import ChineseMessages, EnglishMessages


# 注册语言提供者（在模块加载时执行）
message_factory.register("zh_CN", ChineseMessages)
message_factory.register("en_US", EnglishMessages)

def get_system_language() -> str:
    """获取系统语言，返回 zh_CN 或 en_US"""
    # 1. 环境变量
    env_lang = os.getenv("MAGIC_PIPELINE_LANG") or os.getenv("LANG") or os.getenv("LANGUAGE")
    if env_lang:
        locale_code = env_lang.split('.')[0]
        if locale_code in message_factory.supported_languages():
            return locale_code
    
    # 2. 系统 locale
    try:
        system_locale = locale.getdefaultlocale()[0]
        if system_locale:
            if system_locale in message_factory.supported_languages():
                return system_locale
    except:
        pass
    
    # 3. 默认中文
    return "zh_CN"

def get_message_provider(language: Optional[str] = None) -> MessageProvider:
    """获取消息提供者"""
    if language is None:
        language = get_system_language()
    return message_factory.get(language)