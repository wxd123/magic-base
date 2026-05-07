# magic_base/data_access/util/csv_validator.py

import csv
from pathlib import Path
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class CSVIssue:
    physical_lines: str  # 物理行号范围，如 "76" 或 "2-4"
    logical_line: int
    column: int
    column_name: str
    message: str
    value: str


class CSVValidator:
    """CSV格式验证器"""
    
    def __init__(self, csv_path: Path):
        self.csv_path = csv_path
        self.issues: List[CSVIssue] = []
        self.headers: List[str] = []
        
    def validate(self) -> Tuple[bool, List[CSVIssue]]:
        """验证CSV文件格式"""
        
        # 读取原始行
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            raw_lines = f.readlines()
        
        # 按逻辑行解析，记录每行对应的物理行范围
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            
            try:
                self.headers = next(reader)
            except StopIteration:
                self.issues.append(CSVIssue("1", 1, 0, "", "文件为空", ""))
                return False, self.issues
            
            # 记录每个逻辑行对应的物理行号
            logical_line = 1  # 表头算第1行
            physical_line_start = 1
            
            for row in reader:
                logical_line += 1
                # 当前位置是读取完一行后的位置
                physical_line_end = reader.line_num
                
                physical_range = f"{physical_line_start}-{physical_line_end}"
                if physical_line_start == physical_line_end:
                    physical_range = str(physical_line_start)
                
                # 检查列数
                if len(row) != len(self.headers):
                    self.issues.append(CSVIssue(
                        physical_range, logical_line, 0, "",
                        f"列数不匹配: 期望{len(self.headers)}列, 实际{len(row)}列",
                        ""
                    ))
                
                # 检查每个字段
                for col_idx, (col_name, value) in enumerate(zip(self.headers, row), 1):
                    if value:
                        # 检查字段内引号不平衡
                        quote_count = 0
                        i = 0
                        while i < len(value):
                            if value[i] == '"':
                                if i + 1 < len(value) and value[i + 1] == '"':
                                    i += 2
                                    continue
                                quote_count += 1
                            i += 1
                        
                        if quote_count % 2 != 0:
                            self.issues.append(CSVIssue(
                                physical_range, logical_line, col_idx, col_name,
                                "字段内引号不平衡",
                                value[:50]
                            ))
                
                physical_line_start = physical_line_end + 1
            
            # 检查文件末尾引号是否闭合
            with open(self.csv_path, 'r', encoding='utf-8') as f2:
                content = f2.read()
                quote_count = 0
                i = 0
                while i < len(content):
                    if content[i] == '"':
                        if i + 1 < len(content) and content[i + 1] == '"':
                            i += 2
                            continue
                        quote_count += 1
                    i += 1
                
                if quote_count % 2 != 0:
                    self.issues.append(CSVIssue(
                        f"{physical_line_start}-{len(raw_lines)}", 0, 0, "",
                        "文件末尾引号未闭合", ""
                    ))
        
        return len([i for i in self.issues if "引号" in i.message or "列数" in i.message]) == 0, self.issues
    
    def print_report(self, max_issues: int = 20):
        if not self.issues:
            print(f"✅ {self.csv_path.name} 格式正确")
            return
        
        print(f"\n❌ {self.csv_path.name} 格式问题:")
        for issue in self.issues[:max_issues]:
            if issue.logical_line > 0:
                print(f"  物理行{issue.physical_lines} (记录{issue.logical_line - 1}): {issue.message}")
            else:
                print(f"  物理行{issue.physical_lines}: {issue.message}")
            
            if issue.column > 0 and issue.column_name:
                print(f"    列: {issue.column_name}")
            if issue.value:
                print(f"    值: {issue.value}")
        
        if len(self.issues) > max_issues:
            print(f"  ... 还有{len(self.issues) - max_issues}个问题")