# magic_base/data_access/model/base_dataclass.py
from dataclasses import dataclass, asdict, fields, is_dataclass
from typing import Dict, Any, TypeVar, Type, Union
import json


T = TypeVar('T', bound='BaseDataClass')


class BaseDataClass:
    """
    数据类基类
    
    提供 to_dict、from_dict、update_from_dict 等通用方法。
    所有使用 @dataclass 装饰的类都应该继承此类。
    
    使用示例：
        @dataclass
        class ProjectInfo(BaseDataClass):
            name: str
            version: str = "1.0.0"
        
        # 转换
        project = ProjectInfo(name="test")
        data = project.to_dict()  # {'name': 'test', 'version': '1.0.0'}
        
        # 创建
        new_project = ProjectInfo.from_dict({'name': 'test', 'version': '2.0.0'})
        
        # 更新
        project.update_from_dict({'version': '2.0.0'})
    """
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将数据类实例转换为字典
        
        Returns:
            Dict[str, Any]: 包含所有字段的字典，嵌套的数据类也会被递归转换
            
        Example:
            >>> @dataclass
            ... class SubConfig(BaseDataClass):
            ...     key: str
            ... 
            >>> @dataclass
            ... class MainConfig(BaseDataClass):
            ...     name: str
            ...     sub: SubConfig
            ... 
            >>> main = MainConfig(name="test", sub=SubConfig(key="value"))
            >>> main.to_dict()
            {'name': 'test', 'sub': {'key': 'value'}}
        """
        return self._to_dict_recursive(self)
    
    def _to_dict_recursive(self, obj: Any) -> Any:
        """递归转换嵌套的数据类"""
        if is_dataclass(obj):
            result = {}
            for field in fields(obj):
                value = getattr(obj, field.name)
                result[field.name] = self._to_dict_recursive(value)
            return result
        elif isinstance(obj, list):
            return [self._to_dict_recursive(item) for item in obj]
        elif isinstance(obj, dict):
            return {k: self._to_dict_recursive(v) for k, v in obj.items()}
        else:
            return obj
    
    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """
        从字典创建数据类实例
        
        Args:
            data: 包含字段的字典
            
        Returns:
            T: 数据类实例
        """
        if not is_dataclass(cls):
            raise TypeError(f"{cls.__name__} 必须是 dataclass")
        
        return cls._from_dict_recursive(cls, data)
    
    @classmethod
    def _from_dict_recursive(cls, target_class: Type, data: Dict[str, Any]) -> Any:
        """递归创建嵌套的数据类"""
        if not is_dataclass(target_class):
            return data
        
        field_types = {f.name: f.type for f in fields(target_class)}
        processed = {}
        
        for field_name, field_value in data.items():
            if field_name not in field_types:
                continue
            
            field_type = field_types[field_name]
            # 处理 Optional 类型（简化处理）
            if hasattr(field_type, '__origin__') and field_type.__origin__ is Union:
                # 提取 Union 中的实际类型
                for arg in field_type.__args__:
                    if is_dataclass(arg):
                        field_type = arg
                        break
            
            if is_dataclass(field_type):
                processed[field_name] = cls._from_dict_recursive(field_type, field_value)
            elif isinstance(field_value, list) and field_value:
                # 处理列表中的嵌套数据类
                processed[field_name] = [
                    cls._from_dict_recursive(field_type.__args__[0], item) 
                    if hasattr(field_type, '__args__') and is_dataclass(field_type.__args__[0])
                    else item
                    for item in field_value
                ]
            else:
                processed[field_name] = field_value
        
        return target_class(**processed)
    
    def update_from_dict(self, data: Dict[str, Any]) -> 'BaseDataClass':
        """
        从字典更新当前实例
        
        Args:
            data: 包含待更新字段的字典
            
        Returns:
            BaseDataClass: 当前实例（支持链式调用）
        """
        for key, value in data.items():
            if hasattr(self, key):
                current_value = getattr(self, key)
                # 如果当前值是数据类，且新值也是字典，递归更新
                if is_dataclass(current_value) and isinstance(value, dict):
                    current_value.update_from_dict(value)
                else:
                    setattr(self, key, value)
        return self
    
    def to_json(self, indent: int = None) -> str:
        """
        转换为 JSON 字符串
        
        Args:
            indent: JSON 缩进空格数
            
        Returns:
            str: JSON 字符串
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)
    
    @classmethod
    def from_json(cls: Type[T], json_str: str) -> T:
        """
        从 JSON 字符串创建实例
        
        Args:
            json_str: JSON 字符串
            
        Returns:
            T: 数据类实例
        """
        data = json.loads(json_str)
        return cls.from_dict(data)