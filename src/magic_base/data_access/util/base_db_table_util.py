#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# magic_base/data_access/util/db_table_util.py

from typing import List, Type, Optional
from pathlib import Path
from sqlalchemy import create_engine, Engine, text
import sqlite3

from magic_base import MagicBaseEntity
from magic_base.context.application_context import ApplicationContext
from magic_base.constants.tables import SCHEMA_VERSION_TABLE


class DBModelUtil:
    """数据库迁移管理"""
    
    VERSION: int = 5
    
    @staticmethod
    def _get_engine() -> Engine:
        """获取 SQLAlchemy engine
        
        Returns:
            Engine: SQLAlchemy 数据库引擎实例
        """
        # 优先使用 db_manager 的 engine
        db_manager = ApplicationContext.get_db_manager()
        if db_manager.engine:
            return db_manager.engine    

        # 无法获取 engine，抛出明确异常
        raise RuntimeError(
            "无法获取数据库引擎。请确保:\n"
            "1. ApplicationContext 已正确初始化\n"
            "2. db_manager 已正确配置\n"
            "3. 数据库连接已建立"
        )    
        
    @staticmethod
    def create_tables_entities(models: List[Type[MagicBaseEntity]] = None, check_first: bool = True) -> None:
        """
        通过实体类列表创建对应的表（静态方法版本）
        
        Args:
            models: 模型类列表，如 [User, Order]
                    如果为 None，则创建所有实体对应的表
            check_first: 是否先检查表是否存在（默认 True）
        """
        
        engine: Engine = DBModelUtil._get_engine()
                
        if not models:
            # 获取所有 MagicBaseEntity 的子类
            models = MagicBaseEntity.__subclasses__()
            if not models:
                print("❌ 没有找到任何实体类")
                return
        
        # 显示信息
        print(f"\n📋 准备创建以下 {len(models)} 个实体对应的表:")
        for entity in models:
            exists = engine.dialect.has_table(engine.connect(), entity.__table__.name) if check_first else False
            status = "✅ 已存在" if exists else "⏳ 待创建"
            print(f"   📊 {entity.__name__:20} -> {entity.__table__.name:20} [{status}]")
        
        # 创建表
        created: List[str] = []
        skipped: List[str] = []
        failed: List[tuple[str, str]] = []
        
        with engine.begin() as conn:
            for model in models:
                try:
                    table_name = model.__table__.name
                    
                    # 检查表是否已存在
                    if check_first and engine.dialect.has_table(conn, table_name):
                        skipped.append(model.__name__)
                        print(f"⏭️  {model.__name__} 表已存在，跳过")
                        continue
                    
                    # 创建表
                    model.__table__.create(conn, checkfirst=check_first)
                    created.append(model.__name__)
                    print(f"✅ {model.__name__} 表已创建")
                    
                except Exception as e:
                    failed.append((model.__name__, str(e)))
                    print(f"❌ {model.__name__} 创建失败: {e}")
        
        # 总结
        print(f"\n📊 创建完成: 成功 {len(created)} 个，跳过 {len(skipped)} 个，失败 {len(failed)} 个")
        
        if failed:
            print("\n失败详情:")
            for name, error in failed:
                print(f"   ❌ {name}: {error}")
    
    @staticmethod
    def create_tables(check_first: bool = True) -> None:
        """
        创建所有表（便捷方法）
        
        Args:
            check_first: 是否先检查表是否存在
        """
        DBModelUtil.create_tables_entities(None, check_first)
    
    @staticmethod
    def drop_tables() -> None:
        """删除所有表（谨慎使用）"""
        confirm = input("⚠️  确认删除所有表？这将丢失所有数据！(yes/no): ")
        if confirm.lower() != 'yes':
            print("操作已取消")
            return
        
        engine: Engine = DBModelUtil._get_engine()
        MagicBaseEntity.metadata.drop_all(engine)
        print("✅ 所有表已删除")
    
    @staticmethod
    def get_current_version() -> int:
        """获取当前数据库版本
        
        Returns:
            int: 当前数据库版本号，如果表不存在则返回 0
        """
        engine: Engine = DBModelUtil._get_engine()
        with engine.connect() as conn:
            try:
                result = conn.execute(text(
                    f"SELECT version FROM {SCHEMA_VERSION_TABLE} ORDER BY version DESC LIMIT 1"
                )).fetchone()
                return result[0] if result else 0
            except Exception:
                # 表不存在
                return 0
    
    @staticmethod
    def drop_tables_entities(models: List[Type[MagicBaseEntity]] = None) -> None:
        """
        通过实体类列表删除对应的表
        
        Args:
            models: 模型类列表，如 [User, Order]
                    如果为 None，则删除所有实体对应的表
        """
        engine: Engine = DBModelUtil._get_engine()
    
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
        deleted: List[str] = []
        failed: List[tuple[str, str]] = []
        
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
    def update_version(version: int) -> None:
        """更新数据库版本
        
        Args:
            version: 要更新的版本号
        """
        engine: Engine = DBModelUtil._get_engine()
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
    def run() -> None:
        """执行迁移"""
        print(f"🚀 开始数据库迁移...")
        
        # 创建表
        DBModelUtil.create_tables()
        
        # 版本管理
        current_version: int = DBModelUtil.get_current_version()
        
        if current_version < DBModelUtil.VERSION:
            DBModelUtil.update_version(DBModelUtil.VERSION)
            print(f"✅ 数据库已从版本 {current_version} 迁移到版本 {DBModelUtil.VERSION}")
            
            # 可以在这里添加版本间的数据迁移
            DBModelUtil._run_version_DBModelUtils(current_version)
        else:
            print(f"✅ 数据库当前已是版本 {current_version} (最新)")
        
        print("🎉 数据库迁移完成！")
    
    @staticmethod
    def _run_version_DBModelUtils(from_version: int) -> None:
        """
        执行版本间的数据迁移
        
        Args:
            from_version: 起始版本
        
        # 示例：v1 -> v2 的数据迁移
        if from_version < 2:
            DBModelUtil._migrate_to_v2()
        
        # v2 -> v3 的数据迁移
        if from_version < 3:
            DBModelUtil._migrate_to_v3()
        
        # 继续添加更多版本迁移...
        """
        pass
    
    @staticmethod
    def _migrate_to_v2() -> None:
        """迁移到版本 2 的数据变更"""
        print("  📦 执行 v1 -> v2 数据迁移...")
        # 添加具体的数据迁移逻辑
        # 例如：添加新字段默认值、数据转换等
    
    @staticmethod
    def _migrate_to_v3() -> None:
        """迁移到版本 3 的数据变更"""
        print("  📦 执行 v2 -> v3 数据迁移...")
        # 添加具体的数据迁移逻辑

class DBSqlUtil:
    """数据库初始化工具"""
    
    @staticmethod
    def init_from_sql(sql_file: Path, db_path: Path, force: bool = False) -> None:
        """从 SQL 文件初始化数据库
        
        Args:
            sql_file: SQL 脚本文件路径
            db_path: 数据库文件路径
            force: 是否强制重建（删除现有数据库）
        """
        if force and db_path.exists():
            db_path.unlink()
            print(f"✅ 已删除现有数据库: {db_path}")
        
        # 确保目录存在
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 连接数据库
        conn: sqlite3.Connection = sqlite3.connect(db_path)
        cursor: sqlite3.Cursor = conn.cursor()
        
        # 读取并执行 SQL 脚本
        sql_content: str = sql_file.read_text(encoding='utf-8')
        
        # 分割并执行语句
        for statement in DBSqlUtil._split_sql(sql_content):
            if statement.strip():
                try:
                    cursor.execute(statement)
                except sqlite3.Error as e:
                    print(f"❌ SQL 执行失败: {e}")
                    print(f"   失败的 SQL: {statement[:200]}")
                    conn.rollback()
                    raise
        
        conn.commit()
        conn.close()
        print(f"✅ 数据库初始化完成: {db_path}")
    
    @staticmethod
    def _split_sql(sql_content: str) -> List[str]:
        """分割 SQL 语句
        
        Args:
            sql_content: SQL 脚本内容
            
        Returns:
            List[str]: SQL 语句列表
        """
        statements: List[str] = []
        current: List[str] = []
        
        for line in sql_content.split('\n'):
            line = line.strip()
            if not line or line.startswith('--'):
                continue
            
            current.append(line)
            
            if line.endswith(';'):
                statements.append(' '.join(current))
                current = []
        
        return statements
    
    @staticmethod
    def get_current_version(db_path: Path) -> Optional[str]:
        """获取当前数据库版本
        
        Args:
            db_path: 数据库文件路径
            
        Returns:
            Optional[str]: 版本号字符串，如果数据库不存在或无法获取则返回 None
        """
        if not db_path.exists():
            return None
        
        try:
            conn: sqlite3.Connection = sqlite3.connect(db_path)
            cursor: sqlite3.Cursor = conn.cursor()
            cursor.execute("SELECT value FROM configs WHERE key = 'db_version'")
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else None
        except:
            return None

# 全局实例
db_model_util: DBModelUtil = DBModelUtil()