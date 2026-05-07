
   
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# magic_base/data_access/util/data_commands.py

import csv
from pathlib import Path
import pandas as pd
import traceback
from typing import Dict, Any, Optional, Callable, Tuple, List
from abc import ABC, abstractmethod
from datetime import datetime, date
from magic_base.data_access.util.base_type_converter import TypeConverter as converter
from magic_base import CSVValidator

class BaseDataImportCommand(ABC):
    """数据导入命令基类
    
    提供通用的CSV导入功能和数据解析工具，子类需要实现具体的导入逻辑
    """
    
    def __init__(self, data_dir: Optional[Path] = None):
        """初始化导入器
        
        Args:
            data_dir: 数据目录路径，默认为项目根目录下的 data 文件夹
        """
        if data_dir is None:
            # 从当前文件向上找到项目根目录
            data_dir = Path(__file__).parent.parent.parent.parent / "data"
        self.data_dir = Path(data_dir)
        self.stats = {}
    
    @abstractmethod
    def import_all(self) -> bool:
        """导入所有数据
        
        Returns:
            bool: True表示导入成功，False表示失败
        """
        pass
    
    # ========== 辅助方法 ==========
    
    @staticmethod
    def parse_datetime(value: str) -> Optional[datetime]:
        """解析日期时间字符串"""
        if not value or not value.strip():
            return None
        for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d']:
            try:
                return datetime.strptime(value.strip(), fmt)
            except ValueError:
                continue
        return None
    
    @staticmethod
    def parse_date(value: str) -> Optional[date]:
        """解析日期字符串"""
        if not value or not value.strip():
            return None
        try:
            return datetime.strptime(value.strip(), '%Y-%m-%d').date()
        except ValueError:
            return None
    
    
    @staticmethod
    def parse_bool(value) -> bool:
        """解析布尔值
        
        Args:
            value: 可以是字符串、布尔值或数字
            
        Returns:
            bool: 解析后的布尔值
        """
        if value is None:
            return False
        
        # 如果已经是布尔类型，直接返回
        if isinstance(value, bool):
            return value
        
        # 如果是数字类型
        if isinstance(value, (int, float)):
            return bool(value)
        
        # 转换为字符串处理
        value_str = str(value).strip()
        if not value_str:
            return False
        
        return value_str.upper() in ['1', 'TRUE', 'YES', 'ACTIVE', 'ON']
    
    def _import_csv(self, filename: str, processor: Callable[[Dict[str, str]], bool], 
                   required: bool = True) -> bool:
        """通用的CSV导入方法
        
        Args:
            filename: CSV文件名
            processor: 处理每行数据的回调函数，参数为行数据字典，返回是否成功
            required: 文件是否必需，False时文件不存在只警告不报错
            
        Returns:
            bool: 是否成功导入（文件不存在时根据required决定）
        """
        csv_path = self.data_dir / filename
        if not csv_path.exists():
            if required:
                print(f"✗ Required file not found: {csv_path}")
                return False
            else:
                print(f"⚠️  Optional file not found: {csv_path}, skipping...")
                return True
        
        _validator = CSVValidator(csv_path)
        is_valid, issues = _validator.validate()
        
        if is_valid:
            try:
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    count = 0
                    errors = []
                    for idx, row in enumerate(reader, 2):  # 从第2行开始（第1行是表头）
                        try:
                            # 获取公共列数据
                            base_fields = converter.get_base_fields(row)
                            row.update(base_fields)
                            if processor(row):
                                count += 1
                        except Exception as e:
                            error_msg = str(e) or f"{type(e).__name__}"
                            errors.append(f"行 {idx}: {error_msg}")
                            # 只打印前5个错误避免刷屏
                            if len(errors) <= 5:
                                print(f"  ✗ 行 {idx} 失败: {error_msg}")
                    
                    if errors:
                        print(f"⚠️ 共有 {len(errors)} 行处理失败")
                        if len(errors) > 5:
                            print(f"   (仅显示了前5个错误)")
                    
                    print(f"✓ Imported {count} records from {filename}")
                    self.stats[filename] = {"total": count, "errors": len(errors)}
                    return True
            except Exception as e:
                print(f"✗ Failed to import {filename}: {e}")
                traceback.print_exc()
                return False
        else:
            _validator.print_report()
            print(f"✗ CSV格式验证失败，请修复后重试")
            return False  # 返回失败而不是抛出异常
        
    def _import_csv_batch(self, filename: str, processor: Callable[[Dict[str, str]], Optional[Dict]], 
                   required: bool = True) -> Tuple[bool, List[Dict[str, str]]]:
        """通用的CSV导入方法
        
        Args:
            filename: CSV文件名
            processor: 处理每行数据的回调函数，接收行数据字典，返回处理后的数据字典或None
            required: 文件是否必需
            
        Returns:
            Tuple[bool, List[Dict]]: (是否成功导入, 处理后的结果集)
        """
        csv_path = self.data_dir / filename
        results = []
        
        if not csv_path.exists():
            if required:
                print(f"✗ Required file not found: {csv_path}")
                return False, results
            else:
                print(f"⚠️  Optional file not found: {csv_path}, skipping...")
                return True, results
        _validator = CSVValidator(csv_path)
        is_valid, issues = _validator.validate()
        
        if is_valid:
            try:
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)

                    count = 0
                    errors = []
                    
                    for idx, row in enumerate(reader, 2):  # 从第2行开始（第1行是表头）
                        
                        try:
                            # 调用 processor，获取处理后的数据
                            processed_data = processor(row)

                            if processed_data:  # 如果成功返回数据
                                # 如果需要在数据中添加基础字段，可以这样：                            
                                base_fields = converter.get_base_fields(row)
                                # 打印调试信息
                                # print(f"Base fields: {base_fields}")  # 调试

                                processed_data.update(base_fields)
                                # print(f"After base_fields: {processed_data}")  # 调试
                                count += 1
                                results.append(processed_data)
                                
                        except Exception as e:
                            error_msg = str(e) or f"{type(e).__name__}"
                            errors.append(f"行 {idx}: {error_msg}")
                            if len(errors) <= 5:
                                print(f"  ✗ 行 {idx} 失败: {error_msg}")
                    
                    if errors:
                        print(f"⚠️ 共有 {len(errors)} 行处理失败")
                        if len(errors) > 5:
                            print(f"   (仅显示了前5个错误)")
                    
                    print(f"✓ Imported {count} records from {filename}")
                    self.stats[filename] = {"total": count, "errors": len(errors)}
                    return True, results
                    
            except Exception as e:
                print(f"✗ Failed to import {filename}: {e}")
                traceback.print_exc()
                return False, results
        else:
            _validator.print_report()
            print(f"✗ CSV格式验证失败，请修复后重试")
            return False, results  # 返回失败而不是抛出异常




