from abc import ABC
from typing import Dict, List, Optional, TypeVar, Generic, Type, Any, get_origin, get_args
from sqlalchemy.orm import Session
from sqlalchemy import inspect, text
from .base_repository_core_mixin import RepositoryCoreMixin


T = TypeVar('T')

class CUDRepositoryMixin(RepositoryCoreMixin[T]):
    """
    CUD 操作 Mixin（Create, Update, Delete）
    
    提供使用 ORM 方式的创建、更新、删除操作。
    继承自 RepositoryCoreMixin，获得核心基础设施。
    
    设计理念:
        CUD 操作（创建、更新、删除）适合使用 ORM 方式，因为：
        - 需要对象关系映射的便利性
        - 需要自动处理关联关系
        - 需要触发 ORM 事件和钩子
        
    包含的功能:
        - 单条记录的创建、更新、删除
        - 批量创建和更新
        - 软删除支持
        - ORM 实例获取
    
    注意:
        本 Mixin 不包含查询操作，查询操作请使用 QueryRepositoryMixin
    
    使用方式:
        class UserRepository(RepositoryCoreMixin[User], CUDRepositoryMixin[User]):
            pass
        
        repo = UserRepository()
        user = repo.create(name="Alice", email="alice@example.com")
        repo.update(user.id, name="Alice Updated")
        repo.delete(user.id, soft=True)
    """
    
    def create(self, **kwargs) -> T:
        """创建记录（ORM）
        
        使用 ORM 方式创建并保存新记录，自动刷新并获取自增 ID。
        
        执行流程:
            1. 根据关键字参数实例化模型对象
            2. 将实例添加到会话
            3. 刷新会话（发送 SQL 到数据库）
            4. 刷新实例（获取数据库生成的值，如自增 ID）
        
        参数:
            **kwargs: 模型字段名和值的键值对，字段名需与模型定义一致
        
        返回:
            T: 创建后的模型实例（包含自增 ID 等数据库生成的值）
        
        示例:
            # 创建用户
            user = repo.create(
                name="Alice", 
                email="alice@example.com",
                age=25
            )
            print(user.id)  # 自动生成的 ID
            print(user.created_at)  # 自动设置的时间戳
        
        注意:
            如果模型定义了默认值或自动字段（如 created_at），
            会在 refresh 后获得这些值。
        """
        with self._get_session() as session:
            instance = self._model_class(**kwargs)
            session.add(instance)
            session.flush()
            session.refresh(instance)  # 刷新获取自增 ID
            return instance
    
    def create_from_model(self, model: T) -> T:
        """从模型对象创建（ORM）
        
        使用已有的模型实例创建记录，适用于模型已经部分填充的情况。
        
        使用场景:
            - 模型已经通过其他方式构建完成
            - 需要批量创建相同的模型实例
            - 模型包含复杂的嵌套关系
        
        参数:
            model: 模型实例对象（可以是新建的或从其他地方获取的）
        
        返回:
            T: 创建后的模型实例（包含自增 ID）
        
        示例:
            # 预先构建模型
            user = User(name="Bob", email="bob@example.com")
            user.age = 30
            
            # 保存到数据库
            repo.create_from_model(user)
            print(user.id)  # 现在有了 ID
        """
        with self._get_session() as session:
            session.add(model)
            session.flush()
            session.refresh(model)
            return model
    
    def update(self, record_id: int, **kwargs) -> bool:
        """更新记录（ORM）
        
        根据 ID 查找记录并更新指定字段。
        
        执行流程:
            1. 根据主键 ID 查询记录
            2. 如果记录存在，更新指定字段的值
            3. 刷新会话使更改生效
        
        参数:
            record_id: 记录的主键 ID
            **kwargs: 要更新的字段名和值，只更新提供的字段
        
        返回:
            bool: True 表示更新成功（记录存在），False 表示记录不存在
        
        示例:
            # 更新单个字段
            repo.update(1, name="New Name")
            
            # 同时更新多个字段
            repo.update(1, name="New Name", age=26, email="new@example.com")
        
        注意:
            不会更新未在 kwargs 中指定的字段，保持原有值不变。
        """
        with self._get_session() as session:
            instance = session.query(self._model_class).get(record_id)
            if not instance:
                return False
            
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            
            session.flush()
            return True
    
    def update_from_model(self, model: T) -> bool:
        """从模型对象更新（ORM）
        
        使用 merge 操作将模型实例的状态同步到数据库。
        
        merge 操作的特点:
            - 如果数据库中存在相同 ID 的记录，则更新
            - 如果不存在，则插入新记录
            - 会返回一个附加到当前会话的实例
        
        参数:
            model: 包含更新数据的模型实例（通常包含 ID 字段）
        
        返回:
            bool: 总是返回 True
        
        示例:
            # 获取 ORM 实例
            user = repo.get_orm_instance(1)
            
            # 修改属性
            user.name = "New Name"
            user.email = "updated@example.com"
            
            # 保存更改
            repo.update_from_model(user)
        
        适用场景:
            - 在会话外修改了模型实例
            - 需要将脱管（detached）实例重新附加到会话
        """
        with self._get_session() as session:
            session.merge(model)
            session.flush()
            return True
    
    def delete(self, record_id: int, soft: bool = True, active_field: str = 'is_active') -> bool:
        """删除记录（ORM）
        
        支持软删除和硬删除两种模式。
        
        软删除（soft=True）:
            - 不实际删除数据，只设置激活状态字段为 False
            - 数据仍然保留在数据库中，可通过修改状态恢复
            - 适合需要数据审计或恢复的场景
            
        硬删除（soft=False）:
            - 从数据库中物理删除记录
            - 数据永久丢失，无法恢复
            - 适合不需要保留历史数据的场景
        
        参数:
            record_id: 记录的主键 ID
            soft: 是否软删除，True 表示软删除（设置 is_active=False），
                  False 表示物理删除（从表中删除）
            active_field: 激活状态字段名，默认为 'is_active'
                           仅软删除模式使用
        
        返回:
            bool: True 表示删除成功（记录存在），False 表示记录不存在
        
        异常:
            ValueError: 当使用软删除但模型缺少指定的 active_field 字段时抛出
        
        示例:
            # 软删除（推荐）
            repo.delete(1, soft=True)
            
            # 硬删除（谨慎使用）
            repo.delete(1, soft=False)
            
            # 自定义激活字段名
            repo.delete(1, soft=True, active_field='enabled')
        """
        with self._get_session() as session:
            instance = session.query(self._model_class).get(record_id)
            if not instance:
                return False
            
            if soft:
                if hasattr(instance, active_field):
                    setattr(instance, active_field, False)
                else:
                    raise ValueError(f"模型缺少 {active_field} 字段")
            else:
                session.delete(instance)
            
            session.flush()
            return True
    
    def batch_create(self, models: List[T]) -> List[T]:
        """批量创建（ORM）
        
        使用 bulk_save_objects 批量插入多个模型实例，性能优于逐个插入。
        
        性能优势:
            - 减少数据库往返次数
            - 使用更高效的批量插入语句
            - 对于大量数据插入，性能提升显著
        
        参数:
            models: 模型实例列表
        
        返回:
            List[T]: 创建后的模型实例列表（与输入相同）
        
        注意:
            批量操作不会触发 ORM 的事件（如 before_insert）和钩子函数。
            如果需要触发事件，请使用循环逐个 create()。
        
        示例:
            users = [
                User(name="User1", email="user1@example.com"),
                User(name="User2", email="user2@example.com"),
                User(name="User3", email="user3@example.com")
            ]
            repo.batch_create(users)
        
        适用场景:
            - 数据迁移
            - 批量导入
            - 测试数据准备
        """
        with self._get_session() as session:
            session.bulk_save_objects(models)
            session.flush()
            session.commit()
            return models
    
    def batch_update(self, updates: Dict[int, Dict[str, Any]]) -> int:
        """批量更新（ORM）
        
        根据 ID 字典批量更新多条记录的不同字段。
        
        参数:
            updates: 更新字典，格式为 {record_id: {field_name: new_value, ...}}
                    每个记录可以更新不同的字段集
        
        返回:
            int: 实际更新的记录数量（不包括不存在的记录）
        
        示例:
            updates = {
                1: {'name': 'Alice Updated', 'age': 31},
                2: {'name': 'Bob Updated'},
                3: {'email': 'charlie@new.com', 'is_active': False}
            }
            count = repo.batch_update(updates)
            print(f"成功更新 {count} 条记录")
        
        性能考虑:
            每条记录单独更新，对于大量记录建议使用原生 SQL 批量更新。
        
        注意:
            不存在的记录会被跳过，不会抛出异常。
        """
        updated = 0
        with self._get_session() as session:
            for record_id, fields in updates.items():
                instance = session.query(self._model_class).get(record_id)
                if instance:
                    for key, value in fields.items():
                        if hasattr(instance, key):
                            setattr(instance, key, value)
                    updated += 1
            session.flush()
        return updated
    
    def get_orm_instance(self, record_id: int) -> Optional[T]:
        """获取 ORM 实例
        
        返回完整的 ORM 模型实例，可用于进一步的 ORM 操作。
        
        与查询方法返回字典不同，此方法返回 ORM 对象，可以：
            - 访问关联关系（relationships）
            - 调用模型的方法
            - 修改后直接 update_from_model
        
        参数:
            record_id: 记录的主键 ID
        
        返回:
            Optional[T]: 模型实例，不存在时返回 None
        
        示例:
            # 获取实例并修改
            user = repo.get_orm_instance(1)
            if user:
                user.last_login = datetime.now()
                repo.update_from_model(user)
            
            # 访问关联关系（假设定义了 relationship）
            user = repo.get_orm_instance(1)
            if user and user.profile:
                print(user.profile.bio)
        
        适用场景:
            - 需要操作关联数据
            - 需要调用模型业务方法
            - 需要 ORM 的懒加载特性
        """
        with self._get_session() as session:
            return session.query(self._model_class).get(record_id)