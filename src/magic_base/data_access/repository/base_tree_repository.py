# magic_base/data_access/repository/base_tree_repository.py
"""
BaseTreeRepository - 树结构专属 Repository 基类

定位：
    MagicBaseRepository + TreeRepositoryMixin 的预设组合。
    层次表专属 Repository 直接继承即用。

使用方式：
    class SystemHierarchyDefRepository(BaseTreeRepository[SystemHierarchyDefs]):
        pass

等价于：
    class SystemHierarchyDefRepository(
        MagicBaseRepository[SystemHierarchyDefs],
        TreeRepositoryMixin[SystemHierarchyDefs],
    ):
        pass
"""

from typing import TypeVar

from .base_repository import MagicBaseRepository
from .mixin.base_tree_repository_mixin import TreeRepositoryMixin


T = TypeVar('T')


class BaseTreeRepository(
    MagicBaseRepository[T],
    TreeRepositoryMixin[T],
):
    """
    树结构专属 Repository 基类

    组合：
        - MagicBaseRepository：通用 CRUD（CUD + Query）
        - TreeRepositoryMixin：树专属数据访问

    提供能力：
        - 通用：create / update / delete / find / find_one / count / paginate
        - 树专属：find_edge / find_children / find_parents / has_parent
                 / find_subtree_by_path / find_edges_by_parents
                 / find_ancestor_path / is_descendant / get_max_order_no

    注意：
        通常通过子类继承使用，子类需指定泛型类型 T（层次表 ORM 模型）。
    """
    pass