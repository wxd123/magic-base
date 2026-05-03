# magic_base/data_access/model/base_model.py
"""
ORM 基类 - 所有数据模型继承此基类
"""


import datetime
from typing import Any, Dict, Optional, TypeVar

from sqlalchemy import Boolean, Column, DateTime, Integer, func
from sqlalchemy.orm import declarative_base


T = TypeVar('T', bound='BaseModel')


class BaseModel():
    """
    ORM 模型抽象基类
    
    所有业务模型都应继承此类，提供基础的模型转换和验证功能。
    具体的 ORM 实现（如 SQLAlchemy Base）由业务模块自己创建。
    
    设计理念:
        - 与具体的 ORM 框架解耦，提供纯 Python 层面的基础功能
        - 子类需要自行创建 ORM Base 并继承此类
        - 提供字典序列化、反序列化和数据验证等通用方法
    
    主要功能:
        - to_dict(): 模型转字典
        - from_dict(): 字典更新模型
        - validate(): 数据验证接口
        - get_table_name(): 获取表名
        - __repr__(): 友好的字符串表示
    
    Example:
        # 在 magicd 中：
        from sqlalchemy.ext.declarative import declarative_base
        from magic_base.data_access.model import BaseModel
        
        ORMBase = declarative_base()
        
        class User(ORMBase, BaseModel):
            __tablename__ = "users"
            id = Column(Integer, primary_key=True)
            name = Column(String)
            
            def validate(self) -> bool:
                return bool(self.name)
        
        # 使用示例
        user = User()
        user.from_dict({"name": "Alice"})
        print(user.to_dict())  # {'name': 'Alice'}
        print(user.validate())  # True
    """
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将模型转换为字典
        
        遍历模型实例的所有属性，过滤掉以下划线开头的私有属性，
        返回一个包含所有公开属性的字典。
        
        Returns:
            Dict[str, Any]: 字典格式的模型数据，键为属性名，值为属性值
            
        Example:
            user = User(name="Alice", age=25)
            user_dict = user.to_dict()  # {'name': 'Alice', 'age': 25}
        """
        result = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                result[key] = value
        return result
    
    def from_dict(self: T, data: Dict[str, Any]) -> T:
        """
        从字典更新模型属性
        
        遍历字典中的每一项，如果模型存在同名属性则更新其值。
        不会添加模型中不存在的属性。
        
        参数:
            data: 字典数据，键为属性名，值为要设置的值
            
        返回:
            self: 返回当前实例，支持链式调用
            
        Example:
            user = User()
            user.from_dict({"name": "Bob", "age": 30, "invalid_field": "ignored"})
            # user.name = "Bob", user.age = 30, invalid_field 被忽略
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self
    
    def validate(self) -> bool:
        """
        验证模型数据
        
        子类可以重写此方法实现自定义验证逻辑。
        基类默认实现返回 True，表示总是通过验证。
        
        使用场景:
            - 在保存前验证必填字段
            - 检查字段值格式（如邮箱、手机号）
            - 验证业务规则（如年龄范围、金额非负）
            
        返回:
            bool: True 表示验证通过，False 表示验证失败
            
        Example:
            class User(BaseModel):
                name: str
                age: int
                
                def validate(self) -> bool:
                    if not self.name:
                        return False
                    if self.age < 0 or self.age > 150:
                        return False
                    return True
        """
        return True
    
    @classmethod
    def get_table_name(cls) -> str:
        """
        获取表名
        
        优先返回类属性 __tablename__ 定义的表名，
        如果没有定义则返回类名的小写形式。
        
        子类可以通过在类中定义 __tablename__ 属性来显式指定表名。
        
        返回:
            str: 表名
            
        Example:
            class User(BaseModel):
                __tablename__ = "sys_users"
            
            print(User.get_table_name())  # "sys_users"
            
            class Product(BaseModel):
                pass
            
            print(Product.get_table_name())  # "product"
        """
        if hasattr(cls, "__tablename__"):
            return cls.__tablename__
        return cls.__name__.lower()
    
    def __repr__(self) -> str:
        """
        友好的字符串表示
        
        格式为 "ClassName(attr1=value1, attr2=value2, ...)"
        为了方便阅读，每个属性值只显示前50个字符，超长部分用 "..." 替代。
        
        返回:
            str: 模型的字符串表示
            
        Example:
            user = User(name="Alice", email="alice@example.com")
            print(user)  # User(name=Alice, email=alice@example.com)
        """
        class_name = self.__class__.__name__
        attrs = []
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                value_str = str(value)[:50]  # 限制长度
                if len(str(value)) > 50:
                    value_str += "..."
                attrs.append(f"{key}={value_str}")
        return f"{class_name}({', '.join(attrs)})"
    

# 创建基础模型类
Base = declarative_base(cls=BaseModel)

class MagicBaseModel(Base):
    """
    所有 ORM 模型的抽象基类
    
    提供通用的字段、方法序列化功能。
    继承自 SQLAlchemy 的声明式基类，并混合了 BaseModel 的功能。
    
    类属性:
        __abstract__: 标记为抽象类，不会在数据库中创建对应的表
        
    通用字段:
        id: 自增主键，所有表的标准标识字段
        is_active: 是否激活状态，带索引便于查询
        created_at: 创建时间，自动设置为插入时的时间戳
        updated_at: 更新时间，更新时自动修改
        deleted_at: 软删除时间戳，nullable=True 表示未删除
    
    使用场景:
        作为所有 ORM 模型的基类，提供标准字段和通用方法。
    
    Example:
        from sqlalchemy import String
        from sqlalchemy.orm import Mapped, mapped_column
        
        class User(MagicBaseModel):
            __tablename__ = "users"
            
            username: Mapped[str] = mapped_column(String(50), nullable=False)
            email: Mapped[str] = mapped_column(String(100), unique=True)
        
        # 自动包含 id, is_active, created_at, updated_at, deleted_at 字段
        user = User(username="alice", email="alice@example.com")
        print(user.created_at)  # 自动设置当前时间
    """
    
    __abstract__ = True  # 不创建单独的表
    
    # 通用字段
    id = Column(Integer, primary_key=True, autoincrement=True)
    """自增主键，唯一标识每条记录"""
    
    is_active = Column(Boolean, default=True, index=True)
    """激活状态标志，True表示启用，False表示禁用，带索引便于筛选"""
    
    created_at = Column(DateTime, server_default=func.now())
    """创建时间，记录插入数据库的时间戳，由数据库服务器自动设置"""
    
    updated_at = Column(DateTime, onupdate=func.now())
    """更新时间，记录最后一次修改的时间戳，更新时自动修改"""
    
    # 可选：软删除字段
    deleted_at = Column(DateTime, nullable=True)
    """软删除时间戳，非空表示已删除，用于实现软删除功能"""
    
    # ==================== ORM 实例方法 ====================
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将模型实例转换为字典
        
        重写 BaseModel.to_dict 方法，使用 SQLAlchemy 的表列信息来生成字典。
        自动处理日期时间类型的转换，将其格式化为 ISO 格式字符串。
        
        返回:
            Dict[str, Any]: 模型数据字典，键为列名，值为列值
            
        Example:
            user = session.query(User).first()
            user_dict = user.to_dict()
            # {
            #     'id': 1,
            #     'username': 'alice',
            #     'created_at': '2024-01-01T12:00:00',
            #     ...
            # }
        """
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            # 处理日期时间类型
            if isinstance(value, datetime):
                value = value.isoformat()
            result[column.name] = value
        return result
    
    
    
    def __repr__(self) -> str:
        """
        字符串表示
        
        返回简洁的字符串表示，格式为 "<ClassName(id=123)>"
        主要用于调试和日志输出。
        
        返回:
            str: 模型的字符串表示
            
        Example:
            user = User(id=1, username="alice")
            print(user)  # <User(id=1)>
        """
        return f"<{self.__class__.__name__}(id={self.id})>"