# magic_base/data_access/service/base_service.py
"""
Service 基类 - 定义业务层接口
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Dict, Any

# 注意：Service 操作的是业务对象（可以是 Dict 或 Model）
T = TypeVar('T')  # 业务对象类型


class BaseService(ABC, Generic[T]):
    """
    Service 基类（抽象接口）
    
    定义业务层的标准操作接口。
    具体业务 Service 继承此类并实现业务逻辑。
    
    与 Repository 的区别：
    - Repository: 数据访问（CUD 返回 ORM 对象，R 返回 Dict）
    - Service: 业务逻辑（可统一返回 Dict 或 DTO）
    """
    
    # ==================== 基础 CRUD 业务方法 ====================
    
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Dict]:
        """
        根据 ID 获取业务对象
        
        可包含：
        - 权限检查
        - 数据转换
        - 关联数据加载
        """
        pass
    
    @abstractmethod
    def get_list(self, filters: Optional[Dict] = None,
                 order_by: Optional[str] = None,
                 page: int = 1,
                 page_size: int = 20) -> Dict:
        """
        获取业务对象列表（分页）
        
        Returns:
            {
                "items": [...],
                "total": 100,
                "page": 1,
                "page_size": 20,
                "pages": 5
            }
        """
        pass
    
    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Dict:
        """
        创建业务对象
        
        可包含：
        - 数据验证
        - 业务规则检查
        - 默认值设置
        - 关联数据处理
        """
        pass
    
    @abstractmethod
    def update(self, id: int, data: Dict[str, Any]) -> Dict:
        """
        更新业务对象
        
        可包含：
        - 存在性检查
        - 数据验证
        - 业务规则检查
        - 更新时间戳
        """
        pass
    
    @abstractmethod
    def delete(self, id: int, soft: bool = True) -> bool:
        """
        删除业务对象
        
        可包含：
        - 权限检查
        - 关联数据检查
        - 软删除/硬删除
        """
        pass
    
    @abstractmethod
    def exists(self, **conditions) -> bool:
        """检查业务对象是否存在"""
        pass
    
    @abstractmethod
    def count(self, filters: Optional[Dict] = None) -> int:
        """统计业务对象数量"""
        pass
    
    # ==================== 批量操作方法 ====================
    
    @abstractmethod
    def batch_create(self, items: List[Dict[str, Any]]) -> List[Dict]:
        """批量创建"""
        pass
    
    @abstractmethod
    def batch_update(self, updates: Dict[int, Dict[str, Any]]) -> int:
        """批量更新"""
        pass
    
    @abstractmethod
    def batch_delete(self, ids: List[int], soft: bool = True) -> int:
        """批量删除"""
        pass
    
    # ==================== 业务方法（子类实现） ====================
    
    @abstractmethod
    def validate(self, data: Dict[str, Any], is_update: bool = False) -> bool:
        """
        验证业务数据
        
        子类应实现具体验证逻辑：
        - 必填字段检查
        - 格式验证
        - 唯一性检查
        - 业务规则验证
        """
        pass