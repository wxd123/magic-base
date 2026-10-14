# magic_base/data_access/service/base_tree_service.py
"""
BaseTreeService - 树结构专属 Service 基类

定位：
    BaseService + TreeServiceMixin 的预设组合。
    树业务 Service 直接继承即用。

使用方式：
    class SystemHierarchyDefService(BaseTreeService[SystemHierarchyDefs]):
        def __init__(self):
            super().__init__(SystemHierarchyDefRepository())
            self._node_repo = SystemNodeDefRepository()

等价于：
    class SystemHierarchyDefService(
        BaseService[SystemHierarchyDefs],
        TreeServiceMixin[SystemHierarchyDefs],
    ):
        ...
"""

from typing import TypeVar

from .base_service import BaseService
from .mixin.base_tree_service_mixin import TreeServiceMixin


T = TypeVar('T')


class BaseTreeService(
    BaseService[T],
    TreeServiceMixin[T],
):
    """
    树结构专属 Service 基类

    组合：
        - BaseService：通用 CRUD 透传（含 *_by_key）
        - TreeServiceMixin：树专属业务逻辑

    提供能力：
        - 通用：get_by_key / update_by_key / delete_by_key / find / find_one
                 / exists / count / paginate / create / update / delete
        - 树专属：add_edge / get_children / get_parents / get_subtree
                 / remove_edge / reorder

    子类需在 __init__ 里注入：
        - self._repo      : BaseTreeRepository 实例（super().__init__ 参数）
        - self._node_repo : 节点表 Repository 实例

    注意：
        通常通过子类继承使用，子类需指定泛型类型 T（层次表 ORM 模型）。
    """
    pass