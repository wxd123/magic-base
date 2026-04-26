# magic_base/data_access/repository/base_repository.py
"""
仓储基类 - 定义统一 CRUD 操作接口

设计原则：
- 查询（R）：返回 Dict，使用原生 SQL，性能优先
- 写操作（CUD）：返回 ORM 对象，使用 ORM，便利优先
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Dict, Any

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """仓储基类（抽象接口）"""
    
    # ==================== 查询方法（返回 Dict） ====================
    
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Dict]:
        """根据 ID 获取单条记录"""
        pass
    
    @abstractmethod
    def find_one(self, conditions: Dict[str, Any]) -> Optional[Dict]:
        """根据条件获取单条记录"""
        pass
    
    @abstractmethod
    def find(self, conditions: Optional[Dict] = None,
             order_by: Optional[str] = None,
             limit: Optional[int] = None,
             offset: Optional[int] = None) -> List[Dict]:
        """根据条件查询记录列表"""
        pass
    
    @abstractmethod
    def get_all(self, filters: Optional[Dict] = None,
                order_by: Optional[str] = None,
                limit: Optional[int] = None) -> List[Dict]:
        """获取所有记录（简化版，无 offset）"""
        pass
    
    @abstractmethod
    def exists(self, **conditions) -> bool:
        """检查记录是否存在"""
        pass
    
    @abstractmethod
    def count(self, filters: Optional[Dict] = None) -> int:
        """统计记录数量"""
        pass
    
    @abstractmethod
    def paginate(self, page: int = 1, per_page: int = 20,
                 filters: Optional[Dict] = None,
                 order_by: str = "id DESC") -> Dict:
        """
        分页查询
        
        Returns:
            {
                "items": [...],
                "total": 100,
                "page": 1,
                "per_page": 20,
                "pages": 5,
                "has_next": True,
                "has_prev": False
            }
        """
        pass
    
    # ==================== 创建方法（返回 ORM 对象） ====================
    
    @abstractmethod
    def create(self, **kwargs) -> T:
        """创建记录（从参数）"""
        pass
    
    @abstractmethod
    def create_from_model(self, model: T) -> T:
        """创建记录（从模型对象）"""
        pass
    
    @abstractmethod
    def batch_create(self, models: List[T]) -> List[T]:
        """批量创建（从模型对象列表）"""
        pass
    
    # ==================== 更新方法（返回 bool） ====================
    
    @abstractmethod
    def update(self, id: int, **kwargs) -> bool:
        """更新记录（从参数）"""
        pass
    
    @abstractmethod
    def update_from_model(self, model: T) -> bool:
        """更新记录（从模型对象）"""
        pass
    
    @abstractmethod
    def batch_update(self, updates: Dict[int, Dict[str, Any]]) -> int:
        """
        批量更新
        
        Args:
            updates: {id: {field: value, ...}, ...}
        
        Returns:
            成功更新的记录数
        """
        pass
    
    # ==================== 删除方法（返回 bool） ====================
    
    @abstractmethod
    def delete(self, id: int, soft: bool = True) -> bool:
        """删除单条记录"""
        pass
    
    @abstractmethod
    def batch_delete(self, ids: List[int], soft: bool = True) -> int:
        """批量删除，返回成功删除的数量"""
        pass
    
    # ==================== 辅助方法 ====================
    
    @abstractmethod
    def get_orm_instance(self, id: int) -> Optional[T]:
        """获取 ORM 实例（用于复杂操作）"""
        pass