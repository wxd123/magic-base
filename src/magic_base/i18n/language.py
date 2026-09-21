# magic_base/i18n/language.py
import locale
import os
from typing import Optional

from magic_base.i18n.provider import MessageProvider
from .factory import message_factory
from .languages import ChineseMessages, EnglishMessages


# 注册语言提供者（在模块加载时执行）
# 当这个模块被导入时，立即将中文和英文的消息提供者注册到工厂中
# 这样在应用启动后，就可以直接使用 get_message_provider() 获取对应语言的提供者
# 
# 支持的语言代码：
#   - "zh_CN": 简体中文（使用 ChineseMessages 提供者）
#   - "en_US": 美国英语（使用 EnglishMessages 提供者）
message_factory.register("zh_CN", ChineseMessages)
message_factory.register("en_US", EnglishMessages)


def get_system_language() -> str:
    """
    获取系统语言，返回 zh_CN 或 en_US
    
    该函数按照优先级顺序检测系统语言设置：
        1. 环境变量（最高优先级）
        2. 系统 locale 设置
        3. 默认语言（zh_CN）
    
    优先级说明：
        - 环境变量优先级最高，便于在部署或测试时临时覆盖语言设置
        - 系统 locale 次之，尊重用户的系统配置
        - 默认中文作为后备选项，确保总有可用的语言
    
    支持的环境变量（按优先级从高到低）：
        - MAGIC_PIPELINE_LANG: 项目特定的语言设置
        - LANG: 标准的 Linux/Unix 语言环境变量
        - LANGUAGE: GNU gettext 使用的语言环境变量
    
    Returns:
        str: 语言代码，总是返回已注册的语言之一
             - "zh_CN": 简体中文
             - "en_US": 美国英语
    
    Example:
        # 假设系统 locale 为中文
        lang = get_system_language()  # 返回 "zh_CN"
        
        # 通过环境变量覆盖
        os.environ['MAGIC_PIPELINE_LANG'] = 'en_US'
        lang = get_system_language()  # 返回 "en_US"
        
        # 系统语言不支持时的处理
        # 如果系统返回 'fr_FR' 但未注册，会自动使用默认的 'zh_CN'
    """
    
    # === 1. 检查环境变量（最高优先级） ===
    # 依次检查三个可能的环境变量，使用第一个存在的
    # 注意：getenv() 返回 None 如果变量不存在
    env_lang = os.getenv("MAGIC_PIPELINE_LANG") or os.getenv("LANG") or os.getenv("LANGUAGE")
    
    if env_lang:
        # 处理完整的 locale 字符串，如 "zh_CN.UTF-8" -> "zh_CN"
        # split('.')[0] 会去掉编码部分（.UTF-8, .GBK 等）
        locale_code = env_lang.split('.')[0]
        
        # 验证该语言是否已被注册支持
        if locale_code in message_factory.supported_languages():
            return locale_code
    
    # === 2. 获取系统 locale 设置（次优先级） ===
    try:
        # getdefaultlocale() 返回 (语言编码, 字符编码) 的元组
        # 例如：('zh_CN', 'UTF-8') 或 ('en_US', 'UTF-8')
        # [0] 获取语言编码部分
        system_locale = locale.getdefaultlocale()[0]
        
        if system_locale:
            # 验证系统语言是否被支持
            if system_locale in message_factory.supported_languages():
                return system_locale
    except Exception:
        # 某些环境下可能无法获取 locale 信息
        # （如 Docker 容器未正确配置 locale，或系统设置异常）
        # 捕获所有异常，使用默认语言而不中断程序
        pass
    
    # === 3. 返回默认语言（最低优先级） ===
    # 当环境变量和系统 locale 都无法获取或不支持时，使用中文作为默认值
    # 这样确保函数总是返回一个有效的语言代码
    return "zh_CN"


def get_message_provider(language: Optional[str] = None) -> MessageProvider:
    """
    获取消息提供者
    
    这是一个便捷函数，用于获取指定语言或系统语言的国际化消息提供者实例。
    通过该函数可以轻松访问多语言消息，无需直接操作 message_factory。
    
    工作流程：
        1. 如果指定了 language 参数，直接使用该语言
        2. 如果未指定 language，自动检测系统语言
        3. 从消息工厂获取对应语言的提供者实例
        4. 返回该实例供调用方使用
    
    Args:
        language: 语言代码，可选参数
                 - 如果提供：必须是在 factory 中已注册的语言
                 - 如果为 None：自动调用 get_system_language() 检测
                 
                 支持的值示例：'zh_CN', 'en_US'
    
    Returns:
        MessageProvider: 消息提供者实例，可用于获取国际化消息文本
    
    Raises:
        ValueError: 当指定的语言代码未注册时抛出
    
    Example:
        # 获取系统语言的消息提供者
        provider = get_message_provider()
        msg = provider.get_message('welcome')
        
        # 强制获取英文消息提供者
        en_provider = get_message_provider('en_US')
        error_msg = en_provider.get_message('error.connection_refused')
        
        # 在函数中使用
        def show_message(lang=None):
            provider = get_message_provider(lang)
            print(provider.get_message('hello'))
        
        show_message()           # 使用系统语言
        show_message('zh_CN')    # 使用中文
        show_message('en_US')    # 使用英文
    
    注意：
        该函数每次调用都会创建新的 MessageProvider 实例。
        如果性能敏感且频繁调用，建议缓存返回的实例。
    """
    # 如果未指定语言，自动检测系统语言
    if language is None:
        language = get_system_language()
    
    # 从工厂获取对应语言的提供者实例并返回
    return message_factory.get(language)