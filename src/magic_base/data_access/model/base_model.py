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
    
    所有业务模型都应继承此类。
    具体的 ORM 实现（如 SQLAlchemy Base）由业务模块自己创建。
    
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
    """
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将模型转换为字典
        
        Returns:
            Dict[str, Any]: 字典格式的模型数据
        """
        result = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                result[key] = value
        return result
    
    def from_dict(self: T, data: Dict[str, Any]) -> T:
        """
        从字典更新模型属性
        
        Args:
            data: 字典数据
        
        Returns:
            self
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self
    
    def validate(self) -> bool:
        """
        验证模型数据
        
        子类可以重写此方法实现自定义验证逻辑。
        
        Returns:
            bool: 验证是否通过
        """
        return True
    
    @classmethod
    def get_table_name(cls) -> str:
        """
        获取表名
        
        子类可以通过定义 __tablename__ 属性来指定表名。
        
        Returns:
            str: 表名
        """
        if hasattr(cls, "__tablename__"):
            return cls.__tablename__
        return cls.__name__.lower()
    
    def __repr__(self) -> str:
        """友好的字符串表示"""
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
    
    提供通用的字段、方法序列化功能以及SQL查询方法。
    """
    
    __abstract__ = True  # 不创建单独的表
    
    # 通用字段
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # 可选：软删除字段
    deleted_at = Column(DateTime, nullable=True)
    
    # ==================== ORM 实例方法 ====================
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将模型实例转换为字典
        
        Returns:
            Dict[str, Any]: 模型数据字典
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
        """字符串表示"""
        return f"<{self.__class__.__name__}(id={self.id})>"