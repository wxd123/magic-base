# magic-base/magic_base/i18n/provider.py
from abc import ABC, abstractmethod
from typing import Dict

class MessageProvider(ABC):
    """
    消息提供者抽象基类
    
    该类定义了国际化（i18n）消息提供者的标准接口。所有具体语言的
    消息提供者都必须继承此类并实现 messages 属性。
    
    设计模式：
        - 模板方法模式：定义获取消息的算法骨架（get 方法）
        - 策略模式：不同语言的消息提供者可以互换使用
    
    主要功能：
        1. 提供统一的消息访问接口
        2. 支持消息模板的格式化（使用 str.format() 语法）
        3. 优雅处理缺失的消息键
    
    消息模板语法：
        使用 Python 的 str.format() 格式化语法，支持命名参数替换。
        
        示例模板：
            - "欢迎, {name}" 
            - "您有 {count} 条新消息"
            - "错误代码：{code}，详情：{detail}"
    
    使用示例：
        # 定义中文消息提供者
        class ChineseMessages(MessageProvider):
            @property
            def messages(self) -> Dict[str, str]:
                return {
                    'welcome': '欢迎使用 {app_name}',
                    'error_not_found': '未找到 {resource}',
                    'success': '操作成功',
                }
        
        # 使用提供者
        provider = ChineseMessages()
        msg = provider.get('welcome', app_name='Magic Base')
        # 返回: "欢迎使用 Magic Base"
        
        # 处理缺失的键
        msg = provider.get('unknown_key')
        # 返回: "Unknown message key: unknown_key"
    
    扩展说明：
        子类只需实现 messages 属性返回消息字典，get 方法会自动处理
        消息查找和格式化，无需重复实现。
    """
    
    @property
    @abstractmethod
    def messages(self) -> Dict[str, str]:
        """
        返回消息字典
        
        该属性必须被子类实现，返回一个字典，其中：
            - 键（key）：消息标识符，通常使用点号分隔的命名空间
                       例如：'common.ok', 'error.database', 'user.welcome'
            - 值（value）：消息模板字符串，可以包含格式化占位符
                         占位符使用 {name} 格式，支持 Python str.format() 语法
        
        设计建议：
            - 使用有意义的键名，推荐按模块或功能组织
            - 错误消息建议以 'error.' 为前缀
            - 使用英文键名，便于代码阅读和维护
        
        Returns:
            Dict[str, str]: 消息键到模板字符串的映射字典
            
        Example:
            @property
            def messages(self) -> Dict[str, str]:
                return {
                    # 通用消息
                    'common.ok': '确定',
                    'common.cancel': '取消',
                    'common.confirm': '确认',
                    
                    # 错误消息
                    'error.connection': '连接失败：{reason}',
                    'error.timeout': '操作超时（{timeout}秒）',
                    'error.permission': '权限不足：需要 {role} 角色',
                    
                    # 业务消息
                    'user.created': '用户 {username} 创建成功',
                    'user.deleted': '用户 {username} 已删除',
                    'order.submitted': '订单 {order_id} 已提交，金额：{amount}',
                }
        """
        pass
    
    def get(self, key: str, **kwargs) -> str:
        """
        获取格式化后的消息
        
        根据消息键查找对应的消息模板，并使用提供的参数进行格式化。
        该方法提供了以下特性：
            1. 自动查找：根据键从 messages 字典中查找模板
            2. 参数格式化：支持任意数量的命名参数
            3. 容错处理：当消息键不存在时返回友好的错误提示
            4. 类型安全：使用 str.format() 自动处理参数类型转换
        
        Args:
            key: 消息键，必须与 messages 字典中的键匹配
                建议使用点号分隔的命名空间，如 'error.database'
            **kwargs: 格式化参数，键值对形式
                      参数名必须与模板中的占位符名称匹配
                      如果模板没有占位符，可以省略此参数
        
        Returns:
            str: 格式化后的消息字符串
                - 成功：返回格式化后的消息
                - 失败：返回 "Unknown message key: {key}"
        
        Example:
            provider = SomeMessageProvider()
            
            # 简单消息（无参数）
            msg = provider.get('common.ok')
            # 返回: "确定"
            
            # 带参数的消息
            msg = provider.get('user.welcome', name='张三', role='管理员')
            # 假设模板为 "欢迎 {name}（{role}）"
            # 返回: "欢迎 张三（管理员）"
            
            # 多个参数
            msg = provider.get('order.summary', 
                              order_id='ORD-001', 
                              amount=99.99, 
                              status='已完成')
            # 假设模板为 "订单 {order_id}：{amount} 元，状态：{status}"
            # 返回: "订单 ORD-001：99.99 元，状态：已完成"
            
            # 参数类型自动转换
            msg = provider.get('item.count', count=5)
            # 假设模板为 "共 {count} 件商品"
            # 返回: "共 5 件商品"
            
            # 缺失键的处理
            msg = provider.get('nonexistent.key')
            # 返回: "Unknown message key: nonexistent.key"
            
            # 缺少必要参数的处理（会抛出 KeyError）
            # msg = provider.get('user.welcome')  
            # 假设模板需要 {name} 但未提供，抛出 KeyError: 'name'
        
        Note:
            该方法使用 str.format(**kwargs) 进行格式化，如果模板中
            的占位符在 kwargs 中找不到对应的参数，会抛出 KeyError。
            建议在调用前确保所有必需的参数都已提供。
        
        Warning:
            如果模板中的占位符数量较多或参数可选，建议在子类中
            重写此方法以提供更友好的错误处理或默认值替换。
        """
        # 从消息字典中获取模板
        # 使用 get 方法避免 KeyError，当键不存在时返回 None
        template = self.messages.get(key)
        
        # 如果找不到对应的消息模板，返回友好的错误提示
        if not template:
            # 返回包含键名的错误信息，便于开发者定位问题
            return f"Unknown message key: {key}"
        
        # 使用提供的参数格式化模板字符串
        # **kwargs 会将参数字典解包为命名参数
        # 例如：template.format(name='张三', age=18)
        return template.format(**kwargs)