# magic_base/data_access/util/type_converter.py
"""
简单的类型转换工具
"""

from typing import Any, Dict
from datetime import datetime  # 添加这行导入


class TypeConverter:
    """简单的类型转换工具"""
    
    @staticmethod
    def parse_datetime(value: Any) -> Any:
        """
        解析日期时间字符串为 datetime 对象
        
        Args:
            value: 日期时间字符串或 None
            
        Returns:
            datetime 对象或原值
        """
        if value is None:
            return None
        
        # 如果已经是 datetime 对象，直接返回
        if isinstance(value, datetime):
            return value
        
        # 如果是字符串，尝试解析
        if isinstance(value, str):
            value_str = value.strip()
            if not value_str:
                return None
            
            # 尝试多种日期格式
            formats = [
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d',
                '%Y/%m/%d %H:%M:%S',
                '%Y/%m/%d'
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(value_str, fmt)
                except ValueError:
                    continue
        
        # 如果无法解析，返回原值
        return None
    
    @staticmethod
    def get_base_fields(row: Dict[str, Any]) -> Dict[str, Any]:
        """
        从行数据中提取基类字段（is_active, created_at, updated_at, deleted_at）
        
        Args:
            row: CSV/字典行数据
            
        Returns:
            包含基类字段的字典
        """
        base_fields = {
            'is_active': TypeConverter.to_bool(row.get('is_active'), default=True)
        }
        
        # 时间字段 - 转换为 datetime 对象
        created_at = TypeConverter.parse_datetime(row.get('created_at'))
        updated_at = TypeConverter.parse_datetime(row.get('updated_at'))
        
        base_fields['created_at'] = created_at if created_at else datetime.now()
        base_fields['updated_at'] = updated_at if updated_at else datetime.now()
        
        # 处理 deleted_at
        deleted_at = TypeConverter.parse_datetime(row.get('deleted_at'))
        if deleted_at:
            base_fields['deleted_at'] = deleted_at
        
        return base_fields
    
    @staticmethod
    def to_bool(value: Any, default: bool = False) -> bool:
        """
        将各种格式的值转换为布尔值
        
        支持的格式：
        - 布尔值: True/False
        - 数字: 1/0
        - 字符串: 'TRUE'/'FALSE', 'true'/'false', '1'/'0', 'yes'/'no'
        
        Args:
            value: 待转换的值
            default: 默认值
            
        Returns:
            转换后的布尔值
        """
        if value is None:
            return default
        
        if isinstance(value, bool):
            return value
        
        if isinstance(value, (int, float)):
            return value != 0
        
        if isinstance(value, str):
            value_upper = value.strip().upper()
            return value_upper in ('1', 'TRUE', 'YES', 'T', 'Y', 'ON', 'ACTIVE')
        
        return default


# 创建全局实例
converter = TypeConverter()