# magic_base/data_access/util/csv_validator.py

import csv
from pathlib import Path
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class CSVIssue:
    """
    CSV 格式问题记录数据类
    
    用于记录在 CSV 文件验证过程中发现的每个问题，包含问题的位置、
    类型和详细信息，便于后续定位和修复。
    
    Attributes:
        physical_lines: 物理行号范围，表示问题在原始文件中的实际行号
                       格式：单行如 "76"，多行如 "2-4"
        logical_line: 逻辑行号，表示 CSV 记录的行号（表头为第1行）
        column: 列号（从1开始），0表示列级别问题（如列数不匹配）
        column_name: 列名，来自 CSV 表头
        message: 问题描述信息
        value: 问题字段的值（截断至50字符），便于查看具体内容
    """
    physical_lines: str  # 物理行号范围，如 "76" 或 "2-4"
    logical_line: int    # 逻辑行号（CSV记录行）
    column: int          # 列号（1-based），0表示整行问题
    column_name: str     # 列名
    message: str         # 问题描述
    value: str           # 字段值（截断处理）


class CSVValidator:
    """
    CSV 格式验证器
    
    提供 CSV 文件的格式验证功能，包括：
        1. 文件空值检查
        2. 列数一致性验证
        3. 字段内引号平衡检查（处理转义引号）
        4. 文件整体引号闭合检查
    
    设计特点：
        - 物理行 vs 逻辑行：正确处理 CSV 中字段内换行的情况
        - 引号转义：正确处理 "" 作为转义引号的情况
        - 详细的错误定位：提供物理行号和逻辑行号双重定位
    
    使用场景：
        - 上传 CSV 文件前的预验证
        - 数据导入前的质量检查
        - 批量文件格式校验
    
    使用示例：
        from pathlib import Path
        
        # 创建验证器实例
        validator = CSVValidator(Path("data.csv"))
        
        # 执行验证
        is_valid, issues = validator.validate()
        
        # 打印报告
        validator.print_report()
        
        # 处理验证结果
        if is_valid:
            print("文件格式正确，可以导入")
        else:
            print(f"发现 {len(issues)} 个问题，请修复后重试")
            for issue in issues:
                print(f"行 {issue.logical_line}, 列 {issue.column_name}: {issue.message}")
    
    验证规则说明：
        规则1：文件不能为空
        规则2：所有数据行的列数必须与表头一致
        规则3：字段内的引号必须成对出现（处理转义序列 ""）
        规则4：整个文件的引号总数必须为偶数（全局闭合检查）
    """
    
    def __init__(self, csv_path: Path):
        """
        初始化 CSV 验证器
        
        Args:
            csv_path: CSV 文件的路径（Path 对象）
        
        Example:
            validator = CSVValidator(Path("/path/to/file.csv"))
        """
        self.csv_path = csv_path
        self.issues: List[CSVIssue] = []  # 存储发现的所有问题
        self.headers: List[str] = []      # CSV 表头字段列表
        
    def validate(self) -> Tuple[bool, List[CSVIssue]]:
        """
        验证 CSV 文件格式
        
        执行完整的 CSV 格式验证，包括：
            - 文件空值检查
            - 表头检查
            - 列数一致性验证
            - 字段内引号平衡检查
            - 文件整体引号闭合检查
        
        验证流程：
            1. 读取文件原始内容用于物理行号计算
            2. 解析 CSV 获取表头和数据行
            3. 对每一行进行列数检查
            4. 对每个字段进行引号平衡检查
            5. 对整体文件进行引号闭合检查
        
        Returns:
            Tuple[bool, List[CSVIssue]]: 
                - bool: 验证是否通过（True=无严重问题，False=存在格式错误）
                - List[CSVIssue]: 发现的所有问题列表
            
            Note: 
                只要存在列数错误或引号错误，返回 False
                仅存在其他非致命问题时，返回 True
        
        Example:
            is_valid, issues = validator.validate()
            if not is_valid:
                for issue in issues:
                    print(f"问题: {issue.message} at 行{issue.logical_line}")
        """
        
        # ===== 第1步：读取原始行（用于物理行号定位） =====
        # 读取文件的每一行原始内容，用于计算物理行号范围
        # 这对于包含换行符的字段特别重要（物理行可能跨多行）
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            raw_lines = f.readlines()
        
        # ===== 第2步：按 CSV 格式解析（处理引号、转义等） =====
        # 使用 csv.reader 正确解析 CSV 格式，自动处理引号内的逗号和换行
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            
            # ---------- 2.1 读取表头 ----------
            try:
                self.headers = next(reader)
            except StopIteration:
                # 文件为空的情况
                self.issues.append(CSVIssue(
                    "1",      # 物理行号
                    1,        # 逻辑行号（表头行）
                    0,        # 列号（0表示整行问题）
                    "",       # 列名
                    "文件为空",  # 问题描述
                    ""        # 相关值
                ))
                return False, self.issues
            
            # ---------- 2.2 初始化物理行号跟踪 ----------
            # 记录每个逻辑行对应的物理行号
            logical_line = 1       # 表头算第1行
            physical_line_start = 1  # 当前逻辑行的起始物理行号
            
            # ---------- 2.3 逐行解析数据 ----------
            for row in reader:
                logical_line += 1
                # reader.line_num 是 csv.reader 维护的当前物理行号
                # 当字段内包含换行符时，line_num 会自动增加
                physical_line_end = reader.line_num
                
                # 构建物理行号范围字符串
                # 单行: "5" | 多行: "2-4"
                physical_range = f"{physical_line_start}-{physical_line_end}"
                if physical_line_start == physical_line_end:
                    physical_range = str(physical_line_start)
                
                # ---------- 2.4 列数验证 ----------
                # 检查当前行的列数是否与表头一致
                if len(row) != len(self.headers):
                    self.issues.append(CSVIssue(
                        physical_range,     # 物理行范围
                        logical_line,       # 逻辑行号
                        0,                  # 列号0表示整行问题
                        "",                 # 无列名
                        f"列数不匹配: 期望{len(self.headers)}列, 实际{len(row)}列",
                        ""                  # 无具体值
                    ))
                
                # ---------- 2.5 字段级验证 ----------
                # 逐列检查每个字段的内容
                for col_idx, (col_name, value) in enumerate(zip(self.headers, row), 1):
                    if value:  # 只检查非空字段
                        # 检查字段内引号是否平衡
                        # CSV 中引号转义规则：两个双引号 "" 表示一个双引号字符
                        quote_count = 0
                        i = 0
                        while i < len(value):
                            if value[i] == '"':
                                # 检查是否是转义序列 ""
                                if i + 1 < len(value) and value[i + 1] == '"':
                                    i += 2  # 跳过转义序列
                                    continue
                                # 非转义的引号
                                quote_count += 1
                            i += 1
                        
                        # 引号数量应为偶数（成对出现）
                        if quote_count % 2 != 0:
                            self.issues.append(CSVIssue(
                                physical_range,
                                logical_line,
                                col_idx,
                                col_name,
                                "字段内引号不平衡",
                                value[:50]  # 截取前50字符避免过长
                            ))
                
                # 更新下一行的起始物理行号
                physical_line_start = physical_line_end + 1
            
            # ===== 第3步：全局引号闭合检查 =====
            # 检查整个文件中是否存在未闭合的引号
            # 这可以捕获字段跨越多行但引号未正确闭合的情况
            with open(self.csv_path, 'r', encoding='utf-8') as f2:
                content = f2.read()
                quote_count = 0
                i = 0
                while i < len(content):
                    if content[i] == '"':
                        # 检查是否是转义序列
                        if i + 1 < len(content) and content[i + 1] == '"':
                            i += 2  # 跳过转义序列
                            continue
                        # 非转义的引号
                        quote_count += 1
                    i += 1
                
                # 整个文件的引号总数应为偶数
                if quote_count % 2 != 0:
                    self.issues.append(CSVIssue(
                        f"{physical_line_start}-{len(raw_lines)}",  # 从最后处理的行到文件末尾
                        0,      # 逻辑行号0表示不属于特定记录
                        0,      # 列号0
                        "",     # 无列名
                        "文件末尾引号未闭合",
                        ""
                    ))
        
        # ===== 第4步：返回验证结果 =====
        # 判断是否存在严重问题（引号问题或列数问题）
        has_critical_issues = len([
            i for i in self.issues 
            if "引号" in i.message or "列数" in i.message
        ]) > 0
        
        # 返回：是否通过验证（无严重问题），以及所有问题的列表
        return not has_critical_issues, self.issues
    
    def print_report(self, max_issues: int = 20):
        """
        打印验证报告
        
        将验证结果以易读的格式输出到控制台，包括：
            - 验证通过：显示成功信息
            - 验证失败：显示所有问题详情（可限制显示数量）
        
        Args:
            max_issues: 最多显示的问题数量，默认20个
                       防止问题过多时输出过长
        
        Example:
            validator = CSVValidator(Path("data.csv"))
            validator.validate()
            validator.print_report()  # 打印完整报告
            
            # 只显示前10个问题
            validator.print_report(max_issues=10)
        
        输出示例：
            ✅ data.csv 格式正确
            
            ❌ data.csv 格式问题:
              物理行5-7 (记录4): 列数不匹配: 期望5列, 实际3列
              物理行10 (记录8): 字段内引号不平衡
                列: description
                值: 这是一个"未闭合的字段
              物理行12-15: 文件末尾引号未闭合
        """
        # 如果没有发现问题，输出成功信息
        if not self.issues:
            print(f"✅ {self.csv_path.name} 格式正确")
            return
        
        # 发现问题，输出问题报告
        print(f"\n❌ {self.csv_path.name} 格式问题:")
        
        # 遍历问题列表（限制显示数量）
        for issue in self.issues[:max_issues]:
            # 根据是否有逻辑行号输出位置信息
            if issue.logical_line > 0:
                # 有逻辑行号：显示物理行范围和记录号
                # logical_line - 1 是因为表头算第1行，数据记录从第1条开始
                print(f"  物理行{issue.physical_lines} (记录{issue.logical_line - 1}): {issue.message}")
            else:
                # 无逻辑行号（文件级问题）
                print(f"  物理行{issue.physical_lines}: {issue.message}")
            
            # 如果有列信息，显示列名
            if issue.column > 0 and issue.column_name:
                print(f"    列: {issue.column_name}")
            
            # 如果有具体的值，显示值内容
            if issue.value:
                print(f"    值: {issue.value}")
        
        # 如果问题数量超过限制，显示剩余问题数量
        if len(self.issues) > max_issues:
            print(f"  ... 还有{len(self.issues) - max_issues}个问题")