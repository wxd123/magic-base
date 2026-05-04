#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# magicm_api/database/migrations.py

from typing import List, Type

from sqlalchemy import create_engine, text

from magic_base import MagicBaseModel
from magic_base.context.application_context import ApplicationContext
from magic_base.constants.tables import SCHEMA_VERSION_TABLE


class DBUtil:
    """数据库迁移管理"""
    
    VERSION = 5
    
    @staticmethod
    def _get_engine():
        """获取 SQLAlchemy engine"""
        # 优先使用 db_manager 的 engine
        db_manager = ApplicationContext.get_db_manager()
        if hasattr(db_manager, 'engine') and db_manager.engine:
            return db_manager.engine
        
        # 兼容处理
        db_path = getattr(db_manager, 'db_path', 'magicm.db')
        return create_engine(f"sqlite:///{db_path}")
    
    
    
    @staticmethod
    def drop_tables():
        """删除所有表（谨慎使用）"""
        confirm = input("⚠️  确认删除所有表？这将丢失所有数据！(yes/no): ")
        if confirm.lower() != 'yes':
            print("操作已取消")
            return
        db_manager = ApplicationContext.get_db_manager()
        engine = db_manager.engine
        MagicBaseModel.metadata.drop_all(engine)
        print("✅ 所有表已删除")
    
    @staticmethod
    def get_current_version() -> int:
        """获取当前数据库版本"""
        db_manager = ApplicationContext.get_db_manager()
        engine = db_manager.engine
        with engine.connect() as conn:
            try:
                result = conn.execute(text(
                    f"SELECT version FROM {SCHEMA_VERSION_TABLE} ORDER BY version DESC LIMIT 1"
                )).fetchone()
                return result[0] if result else 0
            except Exception:
                # 表不存在
                return 0
    
    def drop_tables_entities(self, models: List[Type[MagicBaseModel]] = None):
        """
        通过实体类列表删除对应的表
        
        Args:
            models: 模型类列表，如 [User, Order]
                    如果为 None，则删除所有实体对应的表
        """
        db_manager = ApplicationContext.get_db_manager()
        engine = db_manager.engine
                
        
    
        if not models:
            print("❌ 没有找到要删除的实体")
            return
        
        # 显示信息
        print(f"\n⚠️  准备删除以下 {len(models)} 个实体对应的表:")
        for entity in models:
            print(f"   📊 {entity.__name__} -> {entity.__table__.name}")
        
        # 确认
        confirm = input("\n确认删除？数据将无法恢复！(yes/no): ")
        if confirm.lower() != 'yes':
            print("操作已取消")
            return
        
        # 简单的循环删除
        deleted = []
        failed = []
        
        with engine.begin() as conn:
            for model in models:
                try:
                    model.__table__.drop(conn)
                    deleted.append(model.__name__)
                    print(f"✅ {model.__name__} 表已删除")
                except Exception as e:
                    failed.append((model.__name__, str(e)))
                    print(f"❌ {model.__name__} 删除失败: {e}")
        
        # 总结
        print(f"\n📊 删除完成: 成功 {len(deleted)} 个，失败 {len(failed)} 个")

    @staticmethod
    def update_version(version: int):
        """更新数据库版本"""
        db_manager = ApplicationContext.get_db_manager()
        engine = db_manager.engine
        with engine.connect() as conn:
            # 先尝试更新，如果不存在则插入
            result = conn.execute(text(
                f"UPDATE {SCHEMA_VERSION_TABLE} SET version = :version"
            ), {"version": version})
            
            if result.rowcount == 0:
                conn.execute(text(
                    f"INSERT INTO {SCHEMA_VERSION_TABLE} (version) VALUES (:version)"
                ), {"version": version})
            
            conn.commit()
    
    @staticmethod
    def run():
        """执行迁移"""
        print(f"🚀 开始数据库迁移...")
        
        # 创建表
        Migration.create_tables()
        
        # 版本管理
        current_version = Migration.get_current_version()
        
        if current_version < Migration.VERSION:
            Migration.update_version(Migration.VERSION)
            print(f"✅ 数据库已从版本 {current_version} 迁移到版本 {Migration.VERSION}")
            
            # 可以在这里添加版本间的数据迁移
            Migration._run_version_migrations(current_version)
        else:
            print(f"✅ 数据库当前已是版本 {current_version} (最新)")
        
        print("🎉 数据库迁移完成！")
    
    @staticmethod
    def _run_version_migrations(from_version: int):
        """
        执行版本间的数据迁移
        
        Args:
            from_version: 起始版本
        
        # 示例：v1 -> v2 的数据迁移
        if from_version < 2:
            Migration._migrate_to_v2()
        
        # v2 -> v3 的数据迁移
        if from_version < 3:
            Migration._migrate_to_v3()
        
        # 继续添加更多版本迁移...
        """
    @staticmethod
    def _migrate_to_v2():
        """迁移到版本 2 的数据变更"""
        print("  📦 执行 v1 -> v2 数据迁移...")
        # 添加具体的数据迁移逻辑
        # 例如：添加新字段默认值、数据转换等
    
    @staticmethod
    def _migrate_to_v3():
        """迁移到版本 3 的数据变更"""
        print("  📦 执行 v2 -> v3 数据迁移...")
        # 添加具体的数据迁移逻辑


# 全局实例
db_util = DBUtil()