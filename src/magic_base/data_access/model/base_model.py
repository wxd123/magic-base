# magic_base/data_access/model/base_model.py
"""
ORM 基类 - 所有数据模型继承此基类
"""


from typing import Any, Dict, Optional, TypeVar


T = TypeVar('T', bound='MagicBaseModel')


class MagicBaseModel():
    """
    ORM 模型抽象基类
    
    所有业务模型都应继承此类。
    具体的 ORM 实现（如 SQLAlchemy Base）由业务模块自己创建。
    
    Example:
        # 在 magicd 中：
        from sqlalchemy.ext.declarative import declarative_base
        from magic_base.data_access.model import MagicBaseModel
        
        ORMBase = declarative_base()
        
        class User(ORMBase, MagicBaseModel):
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