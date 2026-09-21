# magic_base/types/common.py
"""
通用类型定义模块

该模块提供了整个 magic-base 项目中使用的通用类型别名和基础枚举类。
通过集中定义常用的类型，提高代码的可读性和一致性，减少重复的类型注解。

主要功能：
    1. 定义常用类型别名（Type Aliases），简化复杂的类型注解
    2. 提供枚举基类，统一枚举的扩展功能
    3. 为整个项目提供统一的类型规范

使用示例：
    from magic_base.types.common import JSONDict, BaseEnum
    
    # 使用类型别名
    def process_data(data: JSONDict) -> None:
        pass
    
    # 继承枚举基类
    class Status(BaseEnum):
        ACTIVE = "active"
        INACTIVE = "inactive"
"""

from typing import Dict, Any, Union, List
from enum import Enum


# ============================================================================
# 类型别名定义
# ============================================================================

# JSON 对象类型：键为字符串，值为任意类型的字典
# 用于表示 JSON 格式的对象数据
# 应用场景：API 响应、配置文件、数据交换等
# 
# 示例：
#   config: JSONDict = {"host": "localhost", "port": 8080}
#   response: JSONDict = {"status": "success", "data": {...}}
JSONDict = Dict[str, Any]

# JSON 数组类型：元素类型为任意的列表
# 用于表示 JSON 格式的数组数据
# 
# 示例：
#   items: JSONList = [1, "text", {"key": "value"}, [1, 2, 3]]
#   users: JSONList = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
JSONList = List[Any]

# 原始数据类型联合类型：表示 JSON 支持的基本数据类型
# 对应 JSON 规范中的基础数据类型
# 
# 包含类型：
#   - str: 字符串
#   - int: 整数
#   - float: 浮点数
#   - bool: 布尔值
#   - None: 空值（对应 JSON 的 null）
# 
# 应用场景：配置值、函数参数、返回值等需要限制为原始类型的场合
# 
# 示例：
#   def set_config(key: str, value: Primitive) -> None:
#       config[key] = value
#   
#   set_config("timeout", 30)        # ✓ int
#   set_config("enabled", True)      # ✓ bool
#   set_config("name", "test")       # ✓ str
#   set_config("debug", None)        # ✓ None
#   set_config("data", {"a": 1})     # ✗ 字典不是 Primitive 类型
Primitive = Union[str, int, float, bool, None]


# ============================================================================
# 枚举基类
# ============================================================================

class BaseEnum(Enum):
    """
    枚举基类
    
    提供枚举类型的通用扩展功能，所有项目中的枚举都应该继承此类。
    相比 Python 标准库的 Enum，增加了以下功能：
        1. 根据值反向查找枚举成员
        2. 统一的枚举基础功能扩展点
    
    设计理念：
        - 枚举值通常使用字符串或整数，便于序列化和存储
        - 提供 from_value 方法实现值到枚举的转换
        - 保持枚举的单例特性（每个枚举成员是唯一的）
    
    使用场景：
        - 状态码定义（如订单状态、用户状态）
        - 类型分类（如日志级别、错误类型）
        - 配置选项（如环境类型、部署模式）
        - 业务常量（如性别、星期、月份）
    
    使用示例：
        # 定义状态枚举
        class Status(BaseEnum):
            PENDING = "pending"
            ACTIVE = "active"
            INACTIVE = "inactive"
            DELETED = "deleted"
        
        # 直接使用枚举成员
        current_status = Status.ACTIVE
        print(current_status.value)  # 输出: "active"
        print(current_status.name)   # 输出: "ACTIVE"
        
        # 根据值获取枚举成员（最常用的扩展功能）
        status = Status.from_value("active")
        print(status)  # 输出: Status.ACTIVE
        
        # 处理不存在的值
        status = Status.from_value("unknown")
        print(status)  # 输出: None
        
        # 在函数参数中使用
        def update_status(status: Status) -> None:
            if status == Status.ACTIVE:
                print("状态已激活")
            elif status == Status.INACTIVE:
                print("状态已禁用")
        
        update_status(Status.ACTIVE)
        update_status(Status.from_value("pending"))  # 传递转换后的值
    
    扩展建议：
        如果需要在子类中添加更多通用功能，可以在此类中定义，
        例如：
            - to_dict(): 转换为字典格式
            - get_description(): 获取枚举描述
            - is_valid(value): 验证值是否有效
    """
    
    @classmethod
    def from_value(cls, value: str):
        """
        根据值获取枚举成员
        
        反向查找方法：通过枚举成员的值来获取对应的枚举成员对象。
        这在处理从外部系统（如数据库、API、配置文件）获取的数据时非常有用，
        因为外部数据通常以值的形式存在，而不是枚举对象。
        
        查找算法：
            遍历枚举类的所有成员，比较成员的值与目标值是否相等。
            时间复杂度：O(n)，n 为枚举成员数量（通常很小，可接受）。
        
        Args:
            value: 枚举成员的值
                 通常为字符串或整数类型，应与枚举定义时的 value 类型一致
        
        Returns:
            找到时：返回对应的枚举成员对象
            未找到时：返回 None（而不是抛出异常）
            
            返回 None 而不是抛异常的原因：
                - 避免程序因无效数据而崩溃
                - 调用方可以根据需要自行处理 None 的情况
                - 更符合 Python 的 "请求宽恕比请求许可" 原则
        
        Example:
            class Color(BaseEnum):
                RED = "#FF0000"
                GREEN = "#00FF00"
                BLUE = "#0000FF"
            
            # 有效值查找
            color = Color.from_value("#FF0000")
            print(color)  # 输出: Color.RED
            print(color.name)   # 输出: "RED"
            print(color.value)  # 输出: "#FF0000"
            
            # 无效值处理
            color = Color.from_value("#FFFFFF")
            print(color)  # 输出: None
            
            # 配合条件判断使用
            if color:
                print(f"找到颜色: {color.name}")
            else:
                print("未找到匹配的颜色")
            
            # 实际应用：从数据库读取状态值
            db_status = "active"  # 从数据库读取的值
            status = Status.from_value(db_status)
            if status:
                process_by_status(status)
            else:
                logger.warning(f"未知的状态值: {db_status}")
        
        Note:
            此方法只比较 value，不比较 name。
            如果需要根据 name 查找，可以直接使用枚举类的 __members__ 属性：
                status = Status.__members__.get("ACTIVE")
        
        Warning:
            如果枚举值存在重复（虽然不推荐），此方法返回第一个匹配的成员。
            建议确保枚举值的唯一性。
        """
        # 遍历枚举类的所有成员
        for member in cls:
            # 比较当前成员的值与目标值
            if member.value == value:
                # 找到匹配的成员，立即返回
                return member
        
        # 未找到任何匹配的成员，返回 None
        # 注意：返回 None 而不是抛出异常，让调用方决定如何处理
        return None