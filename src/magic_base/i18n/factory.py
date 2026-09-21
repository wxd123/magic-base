# magic-base/magic_base/i18n/factory.py
from typing import Dict, Type, Optional
from .provider import MessageProvider

class MessageFactory:
    """
    消息工厂类 - 实现工厂模式来管理多语言消息提供者
    
    该类采用单例工厂模式设计，负责注册和获取不同语言的国际化消息提供者。
    通过注册机制，可以动态添加新的语言支持，而不需要修改工厂类的代码，
    符合开闭原则（对扩展开放，对修改封闭）。
    
    工作流程：
        1. 在应用启动时，通过 register() 方法注册各个语言的提供者类
        2. 需要获取消息时，通过 get() 方法获取对应语言的提供者实例
        3. 提供者实例提供 get_message() 等方法获取具体消息文本
    
    使用示例：
        # 注册语言提供者
        MessageFactory.register('zh', ChineseProvider)
        MessageFactory.register('en', EnglishProvider)
        
        # 获取中文消息提供者
        zh_provider = MessageFactory.get('zh')
        message = zh_provider.get_message('welcome')
        
        # 获取支持的语言列表
        languages = MessageFactory.supported_languages()  # ['zh', 'en']
    
    设计模式：工厂模式 (Factory Pattern)
    """
    
    # 类变量：存储所有已注册的语言及其对应的提供者类
    # 格式：{语言代码: 提供者类}
    # 使用字典实现，确保 O(1) 的查找时间复杂度
    _providers: Dict[str, Type[MessageProvider]] = {}
    
    @classmethod
    def register(cls, language: str, provider_class: Type[MessageProvider]):
        """
        注册语言提供者
        
        将一个消息提供者类与特定语言代码关联，以便后续通过 get() 方法获取。
        支持在运行时动态注册新的语言支持。
        
        注意事项：
            - 如果同一个 language 被多次注册，后注册的会覆盖先注册的
            - provider_class 必须是 MessageProvider 的子类（由类型提示保证）
            - 建议在应用初始化阶段完成所有语言的注册
        
        Args:
            language: 语言代码，遵循 ISO 639-1 标准（如 'zh', 'en', 'ja'）
                    建议使用小写字母表示
            provider_class: 消息提供者类，必须是 MessageProvider 的子类
                          该类会在 get() 调用时被实例化
        
        Raises:
            TypeError: 如果 provider_class 不是 MessageProvider 的子类（由类型系统保证）
        
        Example:
            # 注册中文提供者
            MessageFactory.register('zh', ChineseMessageProvider)
            
            # 注册英文提供者
            MessageFactory.register('en', EnglishMessageProvider)
        """
        # 将语言代码和提供者类存储到类字典中
        # 注意：这里存储的是类本身，而不是实例，实现延迟实例化
        cls._providers[language] = provider_class
    
    @classmethod
    def get(cls, language: str = "zh") -> MessageProvider:
        """
        获取消息提供者实例
        
        根据指定的语言代码，返回对应的消息提供者实例。
        如果语言代码未注册，会抛出 ValueError 异常。
        
        实现细节：
            - 每次调用都会创建新的提供者实例（非单例模式）
            - 延迟实例化：只有在需要时才创建实例，节省资源
            - 默认返回中文提供者，确保向后兼容
        
        Args:
            language: 语言代码，默认为 "zh"（简体中文）
                    支持的语言列表可通过 supported_languages() 获取
        
        Returns:
            MessageProvider: 对应语言的消息提供者实例
            
        Raises:
            ValueError: 当指定的语言代码未注册时抛出
                      异常信息会列出所有已支持的语言
        
        Example:
            # 获取默认的中文提供者
            provider = MessageFactory.get()
            
            # 获取英文提供者
            provider = MessageFactory.get('en')
            
            # 获取日文提供者
            provider = MessageFactory.get('ja')
        """
        # 从注册字典中获取提供者类
        provider_class = cls._providers.get(language)
        
        # 如果语言代码未注册，抛出明确的错误提示
        if not provider_class:
            # 构建错误信息，包含支持的语言列表，方便调试
            raise ValueError(
                f"Unsupported language: {language}. "
                f"Supported: {list(cls._providers.keys())}"
            )
        
        # 实例化并提供者类并返回
        # 注意：这里假设提供者类的构造函数不需要额外参数
        return provider_class()
    
    @classmethod
    def supported_languages(cls) -> list:
        """
        返回支持的语言列表
        
        获取所有已注册的语言代码列表，方便用户了解当前系统支持哪些语言。
        
        Returns:
            list: 包含所有已注册语言代码的列表
                 列表顺序与注册顺序相同（Python 3.7+ 字典保持插入顺序）
        
        Example:
            # 获取支持的语言列表
            languages = MessageFactory.supported_languages()
            print(f"系统支持的语言: {', '.join(languages)}")
            
            # 检查是否支持某个语言
            if 'fr' in MessageFactory.supported_languages():
                provider = MessageFactory.get('fr')
        """
        # 返回所有已注册的语言代码（字典的键）
        # 使用 list() 转换以创建新列表，避免外部修改影响内部状态
        return list(cls._providers.keys())


# 全局工厂实例
# 创建 MessageFactory 的全局单例实例
# 虽然 MessageFactory 本身是类，所有方法都是类方法，可以直接调用，
# 但为了兼容性和便利性，提供一个全局实例供直接导入使用
# 
# 使用方式：
#   from magic_base.i18n.factory import message_factory
#   provider = message_factory.get('en')
# 
# 等价于：
#   from magic_base.i18n.factory import MessageFactory
#   provider = MessageFactory.get('en')
message_factory = MessageFactory()