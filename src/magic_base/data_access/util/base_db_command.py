#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# magic_base/data_access/util/base_db_command.py

import sys
import argparse
from abc import ABC, abstractmethod
from typing import List, Type, Dict, Callable, Optional
from magic_base.data_access.util.base_db_util import db_util


class BaseDBCommand(ABC):
    """
    数据库命令基类
    
    该类提供了一个抽象基类，用于构建数据库管理命令行工具。
    子类需要实现 model_tables 属性来指定数据库模型，
    并可以通过 extra_commands 属性扩展自定义命令。
    
    支持的基础命令:
        - init: 初始化数据库
        - create-tables: 创建表结构
        - recreate-tables: 重建表结构
        - version: 查看版本信息
        - migrate: 执行数据库迁移
    
    使用示例:
        class MyDBCommand(BaseDBCommand):
            @property
            def model_tables(self) -> List[Type]:
                return [User, Product, Order]
            
            @property
            def extra_commands(self) -> Dict[str, Callable]:
                return {
                    'backup': self._backup,
                    'restore': self._restore,
                }
            
            def _backup(self, args) -> bool:
                # 实现备份逻辑
                return True
            
            def _restore(self, args) -> bool:
                # 实现恢复逻辑
                return True
    """
    
    def __init__(self):
        """
        初始化基类
        
        创建命令解析器并设置基础命令结构。
        子类在实例化时会自动调用此方法。
        """
        self.parser = None  # 命令行参数解析器实例
        self._setup_parser()  # 配置解析器
    
    @property
    @abstractmethod
    def model_tables(self) -> List[Type]:
        """
        子类必须提供模型列表
        
        返回需要被数据库管理的ORM模型类列表。
        这些模型将用于创建、重建数据库表结构。
        
        Returns:
            List[Type]: ORM模型类的列表
        
        Example:
            @property
            def model_tables(self) -> List[Type]:
                return [UserModel, ProductModel]
        """
        pass
    
    @property
    def command_name(self) -> str:
        """
        命令名称，可用于帮助信息
        
        子类可以重写此属性以提供更具体的命令描述。
        
        Returns:
            str: 命令工具的名称，默认为"数据库管理工具"
        """
        return "数据库管理工具"
    
    @property
    def extra_commands(self) -> Dict[str, Callable]:
        """
        额外命令映射，子类可重写添加自定义命令
        
        返回一个字典，键为命令名称，值为对应的处理函数。
        这些命令会自动添加到命令行解析器中。
        
        Returns:
            Dict[str, Callable]: 命令名到处理函数的映射
        
        Example:
            @property
            def extra_commands(self) -> Dict[str, Callable]:
                return {
                    'export': self._export_data,
                    'import': self._import_data,
                }
        """
        return {}
    
    def _setup_parser(self):
        """
        设置命令行解析器
        
        配置 argparse 解析器，添加所有基础命令和自定义命令。
        包括:
            - init: 初始化数据库（支持强制重建选项）
            - create-tables: 创建表结构
            - recreate-tables: 重建表结构
            - version: 查看版本
            - migrate: 执行迁移
            - 以及 extra_commands 中的自定义命令
        """
        # 创建主解析器，设置命令描述
        self.parser = argparse.ArgumentParser(description=self.command_name)
        
        # 创建子命令解析器，'dest='command'' 将命令名存储到 args.command 中
        subparsers = self.parser.add_subparsers(dest='command')
        
        # === 配置基础命令 ===
        
        # init 命令：初始化数据库
        init_parser = subparsers.add_parser('init', help='初始化数据库')
        # 添加 --force/-f 选项，用于强制重建数据库
        init_parser.add_argument('--force', '-f', action='store_true', help='强制重建')
        
        # create-tables 命令：仅创建表结构（不删除已有数据）
        subparsers.add_parser('create-tables', help='创建表结构')
        
        # recreate-tables 命令：删除并重建表结构（会丢失数据）
        subparsers.add_parser('recreate-tables', help='重建表结构')
        
        # version 命令：查看数据库版本信息
        subparsers.add_parser('version', help='查看版本')
        
        # migrate 命令：执行数据库迁移操作
        subparsers.add_parser('migrate', help='执行迁移')
        
        # === 配置子类自定义命令 ===
        # 遍历子类提供的额外命令，为每个命令添加解析器
        for cmd_name, handler in self.extra_commands.items():
            subparsers.add_parser(cmd_name, help=f'{cmd_name}命令')
    
    def _get_command_map(self) -> Dict[str, Callable]:
        """
        获取命令映射
        
        将基础命令和子类自定义命令合并成一个完整的命令字典。
        
        Returns:
            Dict[str, Callable]: 命令名称到处理函数的完整映射
        """
        # 基础命令映射表
        base_commands = {
            'init': self._init,                      # 初始化数据库
            'create-tables': self._create_tables,    # 创建表结构
            'recreate-tables': self._recreate_tables, # 重建表结构
            'version': self._version,                # 查看版本
            'migrate': self._migrate,                # 执行迁移
        }
        
        # 合并子类的自定义命令（子类命令会覆盖同名的基类命令）
        base_commands.update(self.extra_commands)
        return base_commands
    
    def execute(self, args: Optional[List[str]] = None) -> int:
        """
        执行命令
        
        解析命令行参数，查找对应的处理函数并执行。
        
        Args:
            args: 命令行参数列表，默认为 None（将使用 sys.argv[1:]）
                 例如: ['init', '--force'] 或 ['create-tables']
        
        Returns:
            int: 退出码
                - 0: 执行成功
                - 1: 执行失败（参数错误、命令不存在或执行异常）
        
        Example:
            # 直接执行
            cmd = MyDBCommand()
            exit_code = cmd.execute(['init', '--force'])
            
            # 或者从命令行参数执行
            exit_code = cmd.execute()  # 使用 sys.argv[1:]
        """
        # 调试输出：打印接收到的参数和系统参数（仅在需要调试时使用）
        print(f"DEBUG: args = {args}", file=sys.stderr)
        print(f"DEBUG: sys.argv = {sys.argv}", file=sys.stderr)
        
        # 解析命令行参数
        # 如果 args 为 None，parse_args 会默认使用 sys.argv[1:]
        args = self.parser.parse_args(args)
        
        # 检查是否提供了子命令
        if not args.command:
            # 没有命令时显示帮助信息
            self.parser.print_help()
            return 1
        
        # 获取命令映射表
        command_map = self._get_command_map()
        
        # 查找对应的处理函数
        handler = command_map.get(args.command)
        
        if handler:
            try:
                # 执行命令处理函数
                success = handler(args)
                # 根据执行结果返回退出码
                return 0 if success else 1
            except Exception as e:
                # 捕获并打印异常信息
                print(f"执行命令失败: {e}")
                return 1
        else:
            # 理论上不应该执行到这里，因为所有命令都已注册
            # 但保留此分支作为安全保护
            self.parser.print_help()
            return 1
    
    def _init(self, args) -> bool:
        """
        初始化数据库命令处理函数
        
        根据是否传入 force 参数决定是强制重建还是普通初始化。
        
        Args:
            args: 解析后的命令行参数对象，包含 force 属性
        
        Returns:
            bool: 操作是否成功
        """
        # 检查是否带有 --force/-f 参数
        if getattr(args, 'force', False):
            # 强制重建数据库（不备份）
            return db_util.reinit(backup=False)
        else:
            # 普通初始化数据库
            return db_util.init()
    
    def _create_tables(self, args) -> bool:
        """
        创建表结构命令处理函数
        
        根据 model_tables 属性中定义的模型列表创建数据库表。
        如果表已存在，通常不会重复创建（具体行为取决于 db_util 实现）。
        
        Args:
            args: 解析后的命令行参数对象（此命令无需额外参数）
        
        Returns:
            bool: 操作是否成功
        """
        return db_util.create_tables(self.model_tables)
    
    def _recreate_tables(self, args) -> bool:
        """
        重建表结构命令处理函数
        
        删除已存在的表并根据 model_tables 重新创建。
        注意：此操作会删除所有已有数据！
        
        Args:
            args: 解析后的命令行参数对象（此命令无需额外参数）
        
        Returns:
            bool: 操作是否成功
        """
        return db_util.recreate_tables(self.model_tables)
    
    def _version(self, args) -> bool:
        """
        查看版本命令处理函数
        
        验证数据库版本信息或连接状态。
        
        Args:
            args: 解析后的命令行参数对象（此命令无需额外参数）
        
        Returns:
            bool: 操作是否成功
        """
        return db_util.verify()
    
    def _migrate(self, args) -> bool:
        """
        执行迁移命令处理函数
        
        执行数据库迁移操作，用于更新数据库结构。
        
        Args:
            args: 解析后的命令行参数对象（此命令无需额外参数）
        
        Returns:
            bool: 操作是否成功
        """
        return db_util.migrate()


def main():
    """
    命令行入口函数（供子类调用）
    
    这个函数作为模块的直接入口点。
    由于 BaseDBCommand 是抽象类不能直接实例化，
    所以这里会提示用户使用具体的数据库命令子类。
    
    使用方式:
        # 在子类模块中调用
        if __name__ == "__main__":
            cmd = MyDBCommand()
            sys.exit(cmd.execute())
    
    注意:
        不要在命令行中直接运行这个文件，而应该运行实现了
        model_tables 属性的具体子类。
    """
    # 检查命令行参数中是否请求了帮助信息
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("请使用具体的数据库命令类，如: DBCMD")
        sys.exit(0)
    else:
        # 如果没有请求帮助，提示用户使用具体的子类
        print("请直接运行具体的数据库命令子类")
        sys.exit(1)


# 模块直接执行时的入口点
if __name__ == "__main__":
    main()