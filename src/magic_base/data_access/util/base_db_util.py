#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# magic_base/data_access/util/db_util.py


import shutil
from pathlib import Path
from typing import List, Optional, Callable, Type
from datetime import datetime

from magic_base.data_access.model.base_model import MagicBaseModel
from magic_base.data_access.util.base_db_table_util import DBModelUtil
from magic_base.context.application_context import ApplicationContext



class DBUtil:
    """
    数据库工具类，封装所有数据库操作
    
    提供以下公共方法：
    - init(): 初始化数据库（如果不存在则创建）
    - reinit(): 重新初始化数据库（删除现有数据库后重建）
    - create_tables(): 创建所有表结构
    - recreate_tables(): 删除并重建所有表结构
    """

    _application_context: ApplicationContext = None
    
    def __init__(self,  backup_callback: Optional[Callable] = None):
        """
        初始化 DBUtil 实例
        
        Args:
            backup_callback: 可选的自定义备份回调函数，接收 db_path 参数
        """
        self._backup_callback = backup_callback
        
        self.appContext = ApplicationContext

        self._db_config = self.appContext.db_config
        self._db_manager = self.appContext.db_manager
    
    
    
    @property
    def db_config(self):
        """获取数据库配置"""
        if self._db_config is None:
            self._db_config = self._application_context.db_config
        return self._db_config
    
    @property
    def db_manager(self):
        """获取数据库管理器"""
        if self._db_manager is None:
            self._db_manager = self._application_context.get_db_manager()
        return self._db_manager
    
    def close_connections(self) -> None:
        """关闭所有数据库连接"""
        try:
            if self._db_manager:
                self._db_manager.engine.dispose()
            print("✅ 数据库连接已关闭")
        except Exception as e:
            print(f"⚠️ 关闭连接时出现警告: {e}")
    
    def _backup_database(self, db_path: Path) -> bool:
        """
        备份数据库文件
        
        Args:
            db_path: 数据库文件路径
        
        Returns:
            bool: 是否成功备份
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = db_path.parent / f"{db_path.stem}_backup_{timestamp}{db_path.suffix}"
            shutil.copy2(db_path, backup_path)
            print(f"📦 已备份到: {backup_path}")
            return True
        except Exception as e:
            print(f"⚠️ 备份失败: {e}")
            return False
    
    def _delete_database_file(self, db_path: Path, backup: bool = True) -> bool:
        """
        删除数据库文件
        
        Args:
            db_path: 数据库文件路径
            backup: 是否备份
        
        Returns:
            bool: 是否成功
        """
        if not db_path.exists():
            return True
        
        # 备份旧数据库
        if backup:
            if self._backup_callback:
                if not self._backup_callback(db_path):
                    response = input("是否继续删除旧数据库？(y/N): ")
                    if response.lower() != 'y':
                        print("操作已取消")
                        return False
            else:
                if not self._backup_database(db_path):
                    response = input("是否继续删除旧数据库？(y/N): ")
                    if response.lower() != 'y':
                        print("操作已取消")
                        return False
        
        # 删除文件
        try:
            db_path.unlink()
            print(f"🗑️ 已删除旧数据库: {db_path}")
            return True
        except PermissionError:
            print(f"❌ 权限不足，无法删除: {db_path}")
            print("   请检查文件权限或以 sudo 运行")
            return False
        except Exception as e:
            print(f"❌ 删除数据库失败: {e}")
            return False
    
    def _ensure_directory(self, db_path: Path) -> bool:
        """
        确保数据库目录存在
        
        Args:
            db_path: 数据库文件路径
        
        Returns:
            bool: 是否成功
        """
        try:
            db_path.parent.mkdir(parents=True, exist_ok=True)
            print(f"✅ 数据库目录已就绪: {db_path.parent}")
            return True
        except Exception as e:
            print(f"❌ 目录准备失败: {e}")
            return False
    
    def create_tables(self, models: Optional[List[Type[MagicBaseModel]]] = None) -> bool:
        """创建表结构"""
        print("\n" + "=" * 60)
        print("创建数据库表结构")
        print("=" * 60)
        
        try:
            if models:
                DBModelUtil.create_tables_entities(models)
            else:
                DBModelUtil.create_tables()
            return True
        except Exception as e:
            print(f"❌ 表结构创建失败: {e}")
            return False
        
    def drop_tables(self, models: Optional[List[Type[MagicBaseModel]]] = None) -> bool:
        """删除表结构"""
        print("\n" + "=" * 60)
        print("删除数据库表结构")
        print("=" * 60)
        
        try:
            if models:
                DBModelUtil.drop_tables_entities(models)
            else:
                DBModelUtil.drop_tables()
            return True
        except Exception as e:
            print(f"❌ 表结构删除失败: {e}")
            return False
    
    def recreate_tables(self, models: Optional[List[Type[MagicBaseModel]]] = None, backup: bool = True) -> bool:
        """
        删除并重建所有表结构
        
        Args:
            backup: 是否备份数据（默认 True）
        
        Returns:
            bool: 是否成功重建
        """
        print("\n" + "=" * 60)
        print("重建数据库表结构")
        print("=" * 60)
        
        try:            
            self.drop_tables(models)
            self.create_tables(models)            
            return True
        
        except Exception as e:
            print(f"❌ 重建表结构失败: {e}")
            return False
    
    def init(self) -> bool:
        """
        初始化数据库（如果不存在则创建）
        
        Returns:
            bool: 是否成功初始化
        """
        print("=" * 60)
        print("开始初始化数据库")
        print("=" * 60)
        
        db_path = Path(self.db_config.get_db_path())
        print(f"\n数据库路径: {db_path}")
        
        # 检查数据库是否已存在
        if db_path.exists():
            print(f"\n✅ 数据库已存在: {db_path}")
            # 验证数据库完整性
            return self.verify()
        
        # 确保数据库目录存在
        if not self._ensure_directory(db_path):
            return False
        
        # 创建表结构
        return self.create_tables()
    
    def reinit(self, backup: bool = True) -> bool:
        """
        重新初始化数据库（删除现有数据库后重建）
        
        Args:
            backup: 是否备份旧数据库（默认 True）
        
        Returns:
            bool: 是否成功重新初始化
        """
        print("=" * 60)
        print("重新初始化数据库")
        print("=" * 60)
        
        db_path = Path(self.db_config.get_db_path())
        
        # 检查数据库是否存在
        if db_path.exists():
            print(f"\n找到现有数据库: {db_path}")
            
            # 关闭所有数据库连接
            print("\n关闭数据库连接...")
            self.close_connections()
            
            # 删除数据库文件
            print("\n删除数据库文件...")
            if not self._delete_database_file(db_path, backup):
                return False
        else:
            print(f"\n数据库不存在，将创建新数据库")
        
        # 重新初始化
        print("\n")
        success = self.init()
        
        if success:
            print("\n✅ 数据库重新初始化完成！")
        else:
            print("\n❌ 数据库重新初始化失败！")
        
        return success
    
    def verify(self) -> bool:
        """
        验证数据库完整性
        
        Returns:
            bool: 数据库是否有效
        """
        print("\n" + "=" * 60)
        print("验证数据库")
        print("=" * 60)
        
        db_path = Path(self.db_config.get_db_path())
        
        if db_path.exists():
            file_size = db_path.stat().st_size
            print(f"\n✅ 数据库文件存在")
            print(f"   路径: {db_path}")
            print(f"   大小: {file_size} bytes")
            
            # TODO: 添加更多的验证逻辑
            # 例如检查表是否存在
            
            print("\n✅ 数据库验证通过！")
            return True
        else:
            print(f"\n⚠️ 数据库文件不存在: {db_path}")
            return False


# 全局 DBUtil 实例
db_util:DBUtil = DBUtil()








