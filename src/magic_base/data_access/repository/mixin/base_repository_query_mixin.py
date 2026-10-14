# magic_base/data_access/repository/base_repository_query_mixin.py

from typing import Dict, List, Optional, TypeVar, Generic, Type, Any, get_origin, get_args
from .base_repository_core_mixin import RepositoryCoreMixin
from sqlalchemy import inspect, text

T = TypeVar('T')



class QueryRepositoryMixin(RepositoryCoreMixin[T]):
    """
    查询操作 Mixin（Query）
    
    提供使用原生 SQL 方式的查询操作，包括基础查询、动态查询、分页等。
    继承自 RepositoryCoreMixin，获得核心基础设施。
    
    设计理念:
        查询操作（Read）适合使用原生 SQL 方式，因为：
        - 可以精确控制查询语句，优化性能
        - 支持复杂的 JOIN、子查询、聚合函数
        - 避免 ORM 的性能开销
        - 返回字典格式，便于序列化和数据传输
    
    包含的功能:
        - 原生 SQL 执行（fetch_one/fetch_all）
        - 基础查询（get_by_id/get_all）
        - 动态条件查询（find/find_one）
        - 存在性检查（exists）
        - 计数统计（count）
        - 分页查询（paginate）
    
    注意:
        本 Mixin 不包含 CUD 操作（创建、更新、删除），
        CUD 操作请使用 CUDRepositoryMixin
    
    使用方式:
        class UserRepository(RepositoryCoreMixin[User], QueryRepositoryMixin[User]):
            pass
        
        repo = UserRepository()
        
        # 基础查询
        user = repo.get_by_id(1)
        users = repo.get_all(filters={'is_active': True}, limit=10)
        
        # 动态查询
        admins = repo.find(conditions={'role': 'admin', 'is_active': True})
        
        # 分页
        page = repo.paginate(page=2, per_page=20, conditions={'is_active': True})
    """
    
    def fetch_one(self, sql: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict]:
        """查询单条记录（原生 SQL）
        
        执行 SQL 查询并返回第一条记录，以字典形式呈现。
        
        执行流程:
            1. 执行原始 SQL 语句
            2. 获取第一条结果行
            3. 将行数据转换为字典（列名 -> 值）
            4. 如果没有结果返回 None
        
        参数:
            sql: SQL 查询语句，支持命名占位符 :param_name
            params: 参数字典，用于 SQL 占位符 :param_name
        
        返回:
            Optional[Dict]: 记录字典，键为列名，值为对应的值；未找到时返回 None
        
        示例:
            # 简单查询
            user = repo.fetch_one("SELECT * FROM users WHERE id = 1")
            
            # 参数化查询（防止 SQL 注入）
            user = repo.fetch_one(
                "SELECT * FROM users WHERE id = :id AND is_active = :active",
                {'id': 1, 'active': True}
            )
        
        注意:
            即使 SQL 返回多行，也只返回第一行。如需多行，使用 fetch_all。
            建议始终使用参数化查询，避免 SQL 注入风险。
        """
        with self._get_session() as session:
            result = session.execute(text(sql), params or {})
            row = result.first()
            if row:
                return dict(row._mapping)
            return None
    
    def fetch_all(self, sql: str, params: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """查询多条记录（原生 SQL）
        
        执行 SQL 查询并返回所有记录，每条记录以字典形式呈现。
        
        执行流程:
            1. 执行原始 SQL 语句
            2. 获取所有结果行
            3. 将每行数据转换为字典（列名 -> 值）
            4. 返回字典列表
        
        参数:
            sql: SQL 查询语句，支持命名占位符 :param_name
            params: 参数字典，用于 SQL 占位符 :param_name
        
        返回:
            List[Dict]: 记录字典列表，未找到时返回空列表 []
        
        示例:
            # 查询所有激活用户
            users = repo.fetch_all(
                "SELECT * FROM users WHERE is_active = :active",
                {'active': True}
            )
            
            # 复杂 JOIN 查询
            results = repo.fetch_all("
                SELECT u.*, p.bio 
                FROM users u
                LEFT JOIN profiles p ON u.id = p.user_id
                WHERE u.created_at > :since
            ", {'since': '2024-01-01'})
        
        性能考虑:
            对于可能返回大量数据的查询，建议添加 LIMIT 限制，
            或者使用分页查询减少单次返回的数据量。
        """
        with self._get_session() as session:
            result = session.execute(text(sql), params or {})
            rows = result.fetchall()
            return [dict(row._mapping) for row in rows]
    
    def get_by_id(self, record_id: int) -> Optional[Dict]:
        """根据 ID 查询（SQL）
        
        使用原生 SQL 根据主键 ID 查询单条记录。
        这是最常用的查询方法之一。
        
        参数:
            record_id: 记录的主键 ID（通常为自增整数 ID）
        
        返回:
            Optional[Dict]: 记录字典，键为列名，值为对应的值；未找到时返回 None
        
        示例:
            # 查询 ID 为 1 的用户
            user = repo.get_by_id(1)
            if user:
                print(f"用户名: {user['name']}")
            else:
                print("用户不存在")
        
        注意:
            此方法假设主键字段名为 "id"。
            如果表使用其他主键名，请使用 fetch_one 自定义查询。
        """
        return self.fetch_one(
            f"SELECT * FROM {self._table_name} WHERE id = :id",
            {'id': record_id}
        )
    
    def get_all(self, filters: Optional[Dict[str, Any]] = None,
                order_by: Optional[str] = None,
                limit: Optional[int] = None) -> List[Dict]:
        """查询所有记录（SQL）
        
        支持过滤条件、排序和限制返回数量，是基础的列表查询方法。
        
        参数:
            filters: 过滤条件字典，格式为 {field_name: value}
                    所有条件使用 AND 连接，且为等值匹配
            order_by: 排序字段，格式如 "id DESC" 或 "created_at ASC"
            limit: 返回记录数量限制
        
        返回:
            List[Dict]: 记录字典列表
        
        示例:
            # 查询所有用户
            all_users = repo.get_all()
            
            # 带过滤条件
            active_users = repo.get_all(
                filters={'is_active': True, 'role': 'user'}
            )
            
            # 带排序和限制
            recent_users = repo.get_all(
                filters={'is_active': True},
                order_by='created_at DESC',
                limit=10
            )
        
        注意:
            过滤条件仅支持等值（=）匹配。如需范围查询（>、<、LIKE 等），
            请使用 find 方法或自定义 fetch_all。
        """
        sql = f"SELECT * FROM {self._table_name} WHERE 1=1"
        params = {}
        
        if filters:
            for key, value in filters.items():
                if value is not None:
                    sql += f" AND {key} = :{key}"
                    params[key] = value
        
        if order_by:
            sql += f" ORDER BY {order_by}"
        if limit:
            sql += " LIMIT :limit"
            params['limit'] = limit
        
        return self.fetch_all(sql, params)
    
    def find(self, conditions: Optional[Dict[str, Any]] = None,
             order_by: Optional[str] = None,
             limit: Optional[int] = None,
             offset: Optional[int] = None) -> List[Dict]:
        """动态查询（SQL）
        
        灵活的查询方法，支持等值条件、排序、分页，比 get_all 更灵活。
        
        参数:
            conditions: 查询条件字典，格式为 {field_name: value}
                       所有条件使用 AND 连接，且为等值匹配
            order_by: 排序字段，如 "created_at DESC" 或 "name ASC"
            limit: 返回记录数量限制
            offset: 偏移量，用于分页（配合 limit 使用）
        
        返回:
            List[Dict]: 记录字典列表
        
        示例:
            # 基础查询
            users = repo.find(conditions={'is_active': True})
            
            # 分页查询
            page_users = repo.find(
                conditions={'is_active': True},
                order_by='id DESC',
                limit=20,
                offset=40
            )
            
            # 无条件的查询（相当于 get_all）
            all_users = repo.find()
        
        适用场景:
            - 需要分页的列表查询
            - 简单的多条件等值查询
            - 需要排序和限制的查询
        
        注意:
            仅支持等值匹配，复杂查询请使用 fetch_all 方法。
        """
        where_parts = []
        params = {}
        
        if conditions:
            for key, value in conditions.items():
                if value is not None:
                    where_parts.append(f"{key} = :{key}")
                    params[key] = value
        
        where_clause = " AND ".join(where_parts) if where_parts else "1=1"
        sql = f"SELECT * FROM {self._table_name} WHERE {where_clause}"
        
        if order_by:
            sql += f" ORDER BY {order_by}"
        if limit:
            sql += " LIMIT :limit"
            params['limit'] = limit
        if offset:
            sql += " OFFSET :offset"
            params['offset'] = offset
        
        return self.fetch_all(sql, params)
    
    def find_one(self, conditions: Dict[str, Any]) -> Optional[Dict]:
        """查询单条记录（SQL）
        
        根据条件查询第一条匹配的记录，常用于唯一性检查或获取单个结果。
        
        参数:
            conditions: 查询条件字典，格式为 {field_name: value}
                       所有条件使用 AND 连接
        
        返回:
            Optional[Dict]: 记录字典，未找到时返回 None
        
        示例:
            # 根据邮箱查找用户
            user = repo.find_one({'email': 'alice@example.com'})
            
            # 根据用户名和状态查找
            user = repo.find_one({
                'username': 'alice',
                'is_active': True
            })
            
            # 检查记录是否存在
            if repo.find_one({'email': email}):
                raise ValueError("邮箱已被注册")
        
        注意:
            如果多个记录匹配条件，只返回第一个。
            建议在条件中包含唯一索引字段，确保结果唯一。
        """
        results = self.find(conditions, limit=1)
        return results[0] if results else None
    
    def exists(self, **conditions) -> bool:
        """检查是否存在（SQL）
        
        检查是否存在满足条件的记录，常用于唯一性验证和存在性检查。
        
        参数:
            **conditions: 条件字段和值的键值对，支持多个条件
        
        返回:
            bool: True 表示至少存在一条满足条件的记录，False 表示不存在
        
        示例:
            # 检查邮箱是否已存在
            if repo.exists(email='alice@example.com'):
                print("用户已存在")
            
            # 检查用户是否激活
            if repo.exists(id=1, is_active=True):
                print("用户已激活")
            
            # 验证唯一性
            def register_user(email, username):
                if repo.exists(email=email):
                    raise ValueError("邮箱已被注册")
                if repo.exists(username=username):
                    raise ValueError("用户名已被占用")
                # 注册逻辑...
        
        性能考虑:
            此方法在查到第一条匹配记录后就会停止，比 count() > 0 更高效。
        """
        result = self.find_one(conditions)
        return result is not None
    
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """统计数量（SQL）
        
        统计满足条件的记录总数，常用于数据概览和分页计算。
        
        参数:
            filters: 过滤条件字典，格式为 {field_name: value}
                    所有条件使用 AND 连接
        
        返回:
            int: 记录总数，如果无匹配记录返回 0
        
        示例:
            # 统计所有用户
            total_users = repo.count()
            
            # 统计激活用户数
            active_count = repo.count({'is_active': True})
            
            # 统计 admin 角色数量
            admin_count = repo.count({'role': 'admin', 'is_active': True})
            
            # 用于分页计算
            total = repo.count(conditions)
            pages = (total + per_page - 1) // per_page
        
        注意:
            如果 filters 为 None 或空字典，统计所有记录。
            对于大表，COUNT(*) 操作可能较慢，请谨慎使用。
        """
        sql = f"SELECT COUNT(*) as total FROM {self._table_name} WHERE 1=1"
        params = {}
        
        if filters:
            for key, value in filters.items():
                if value is not None:
                    sql += f" AND {key} = :{key}"
                    params[key] = value
        
        result = self.fetch_one(sql, params)
        return result['total'] if result else 0
    
    def paginate(self, page: int = 1, per_page: int = 20,
                 conditions: Optional[Dict[str, Any]] = None,
                 order_by: str = "id DESC") -> Dict[str, Any]:
        """分页查询（SQL）
        
        实现标准的分页查询，返回包含数据和分页信息的字典。
        这是 Web 应用中最常用的查询方法之一。
        
        参数:
            page: 当前页码，从 1 开始（第 1 页为首页）
            per_page: 每页记录数，默认 20 条
            conditions: 查询条件字典，格式为 {field_name: value}
            order_by: 排序字段，默认为 "id DESC"（最新的在前）
        
        返回:
            Dict[str, Any]: 分页结果字典，包含以下键：
                - items: 当前页的记录列表（List[Dict]）
                - total: 总记录数（int）
                - page: 当前页码（int）
                - per_page: 每页记录数（int）
                - pages: 总页数（int）
                - has_next: 是否有下一页（bool）
                - has_prev: 是否有上一页（bool）
        
        示例:
            # 基础分页
            result = repo.paginate(page=2, per_page=10)
            for user in result['items']:
                print(user['name'])
            
            # 带条件的分页
            result = repo.paginate(
                page=1,
                per_page=20,
                conditions={'is_active': True},
                order_by='created_at DESC'
            )
            
            # 渲染分页导航
            print(f"第 {result['page']} 页，共 {result['pages']} 页")
            if result['has_prev']:
                print("上一页")
            if result['has_next']:
                print("下一页")
        
        分页计算:
            offset = (page - 1) * per_page
            LIMIT per_page OFFSET offset
        
        注意:
            page 参数小于 1 时会被视为 1。
            per_page 建议根据实际需求设置，避免单次返回过多数据。
        """
        offset = (page - 1) * per_page
        
        items = self.find(
            conditions=conditions,
            order_by=order_by,
            limit=per_page,
            offset=offset
        )
        
        total = self.count(conditions)
        
        return {
            'items': items,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page if total else 0,
            'has_next': page * per_page < total,
            'has_prev': page > 1
        }