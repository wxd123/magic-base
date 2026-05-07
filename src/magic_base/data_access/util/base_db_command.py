#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# magic_base/data_access/util/base_db_command.py

import sys
import argparse
from abc import ABC, abstractmethod
from typing import List, Type, Dict, Callable, Optional
from magic_base.data_access.util.base_db_util import db_util



class BaseDBCommand(ABC):
    """数据库命令基类"""
    
    def __init__(self):
        """初始化基类"""
        self.parser = None
        self._setup_parser()
    
    @property
    @abstractmethod
    def model_tables(self) -> List[Type]:
        """子类必须提供模型列表"""
        pass
    
    @property
    def command_name(self) -> str:
        """命令名称，可用于帮助信息"""
        return "数据库管理工具"
    
    @property
    def extra_commands(self) -> Dict[str, Callable]:
        """额外命令映射，子类可重写添加自定义命令"""
        return {}
    
    def _setup_parser(self):
        """设置命令行解析器"""
        self.parser = argparse.ArgumentParser(description=self.command_name)
        subparsers = self.parser.add_subparsers(dest='command')
        
        # 基础命令
        init_parser = subparsers.add_parser('init', help='初始化数据库')
        init_parser.add_argument('--force', '-f', action='store_true', help='强制重建')
        
        subparsers.add_parser('create-tables', help='创建表结构')
        subparsers.add_parser('recreate-tables', help='重建表结构')
        subparsers.add_parser('version', help='查看版本')
        subparsers.add_parser('migrate', help='执行迁移')
        
        # 子类自定义命令
        for cmd_name, handler in self.extra_commands.items():
            subparsers.add_parser(cmd_name, help=f'{cmd_name}命令')
    
    def _get_command_map(self) -> Dict[str, Callable]:
        """获取命令映射"""
        base_commands = {
            'init': self._init,
            'create-tables': self._create_tables,
            'recreate-tables': self._recreate_tables,
            'version': self._version,
            'migrate': self._migrate,
        }
        # 合并子类的自定义命令
        base_commands.update(self.extra_commands)
        return base_commands
    
    def execute(self, args: Optional[List[str]] = None) -> int:
        """执行命令
        
        Args:
            args: 命令行参数列表，默认使用sys.argv[1:]
            
        Returns:
            退出码，0表示成功，非0表示失败
        """

        print(f"DEBUG: args = {args}", file=sys.stderr)
        print(f"DEBUG: sys.argv = {sys.argv}", file=sys.stderr)
        args = self.parser.parse_args(args)
        
        if not args.command:
            self.parser.print_help()
            return 1
        
        command_map = self._get_command_map()
        handler = command_map.get(args.command)
        
        if handler:
            try:
                success = handler(args)
                return 0 if success else 1
            except Exception as e:
                print(f"执行命令失败: {e}")
                return 1
        else:
            self.parser.print_help()
            return 1
    
    def _init(self, args) -> bool:
        """初始化数据库"""
        if getattr(args, 'force', False):
            return db_util.reinit(backup=False)
        else:
            return db_util.init()
    
    def _create_tables(self, args) -> bool:
        """创建表结构"""
        return db_util.create_tables(self.model_tables)
    
    def _recreate_tables(self, args) -> bool:
        """重建表结构"""
        return db_util.recreate_tables(self.model_tables)
    
    def _version(self, args) -> bool:
        """查看版本"""
        return db_util.verify()
    
    def _migrate(self, args) -> bool:
        """执行迁移"""
        return db_util.migrate()



def main():
    """命令行入口（供子类调用）"""
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("请使用具体的数据库命令类，如: DBCMD")
        sys.exit(0)
    else:
        print("请直接运行具体的数据库命令子类")
        sys.exit(1)


if __name__ == "__main__":
    main()
