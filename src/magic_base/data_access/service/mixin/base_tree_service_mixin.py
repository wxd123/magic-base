# magic_base/data_access/service/mixin/base_tree_service_mixin.py
"""
TreeServiceMixin - 树结构业务逻辑 Mixin

职责：
    实现树业务的完整逻辑：key→id 转换、唯一归属校验、环检测、
    order_no 分配、子树查询编排。

设计理念：
    - 与 Repository 层的 TreeRepositoryMixin 对应
    - Repository 管数据访问，Mixin 管业务逻辑
    - 首期只实现 tree 边，mount 预留
    - 不级联、不感知节点废弃（业务组装层判断）

依赖（宿主 Service 必须提供）：
    - self._repo      : BaseTreeRepository 实例（层次表）
    - self._node_repo : 节点表 Repository 实例（查节点业务信息）

使用方式：
    class SystemHierarchyDefService(BaseTreeService[SystemHierarchyDefs]):
        def __init__(self):
            super().__init__(SystemHierarchyDefRepository())
            self._node_repo = SystemNodeDefRepository()
"""

from typing import Dict, List, Optional, Any, Generic, TypeVar

T = TypeVar('T')


class TreeServiceMixin(Generic[T]):
    """树结构业务逻辑 Mixin"""

    # 业务 key 字段名，子类可覆写
    _node_key_field: str = 'node_key'

    # 类型标注（IDE / mypy 提示）
    _repo: Any          # 期望 BaseTreeRepository
    _node_repo: Any     # 期望 BaseRepository

    # ==================== 依赖校验 ====================

    def _check_dependencies(self) -> None:
        """校验宿主依赖是否满足

        在入口方法调用一次，保证依赖可用。
        缺失时立即报错，避免运行到一半才 AttributeError。
        """
        if not hasattr(self, '_repo') or self._repo is None:
            raise RuntimeError(
                f"{self.__class__.__name__} 必须注入 _repo（BaseTreeRepository）"
            )
        if not hasattr(self._repo, 'has_parent'):
            raise TypeError(
                f"{self.__class__.__name__} 的 _repo 必须是 BaseTreeRepository，"
                f"缺少 has_parent 方法"
            )
        if not hasattr(self, '_node_repo') or self._node_repo is None:
            raise RuntimeError(
                f"{self.__class__.__name__} 必须注入 _node_repo（节点表 Repository）"
            )
        if not self._node_key_field:
            raise ValueError(
                f"{self.__class__.__name__} 的 _node_key_field 不能为空"
            )

    # ==================== 边操作 ====================

    def add_edge(self, parent_key: str, child_key: str,
                 order_no: Optional[int] = None) -> Dict:
        """加边（首期只做 tree）

        业务规则：
            1. parent_key / child_key 必须存在（转 id）
            2. child 必须唯一归属（不能已有父）
            3. 不能成环（parent 不能是 child 的后代）
            4. order_no 未给则取同级最大 + 1

        参数:
            parent_key: 父节点业务 key
            child_key: 子节点业务 key
            order_no: 同级顺序，可选

        返回:
            Dict: 创建的边记录（Dict）

        异常:
            ValueError: 节点不存在 / child 已有父 / 成环
        """
        self._check_dependencies()

        parent = self._node_repo.find_one({self._node_key_field: parent_key})
        child = self._node_repo.find_one({self._node_key_field: child_key})
        if not parent or not child:
            raise ValueError(f"节点不存在: parent={parent_key}, child={child_key}")

        parent_id, child_id = parent['id'], child['id']

        # child 唯一归属
        if self._repo.has_parent(child_id):
            raise ValueError(f"子节点 {child_key} 已有父，树中 child 必须唯一")

        # 环检测
        if self._repo.is_descendant(child_id, parent_id):
            raise ValueError(f"加边会成环：{parent_key} 是 {child_key} 的后代")

        # order_no
        if order_no is None:
            max_order = self._repo.get_max_order_no(parent_id)
            order_no = (max_order + 1) if max_order is not None else 0

        instance = self._repo.create(
            parent_id=parent_id,
            node_ref_id=child_id,
            edge_type='tree',
            order_no=order_no,
        )
        return instance.to_dict() if hasattr(instance, 'to_dict') else instance

    def get_children(self, parent_key: str) -> List[Dict]:
        """查直接子节点（返回子节点的业务信息）

        参数:
            parent_key: 父节点业务 key

        返回:
            List[Dict]: 子节点业务信息列表（按 order_no 排序）
        """
        self._check_dependencies()

        parent = self._node_repo.find_one({self._node_key_field: parent_key})
        if not parent:
            return []

        edges = self._repo.find_children(parent['id'])
        if not edges:
            return []

        return self._assemble_nodes(edges, id_field='node_ref_id')

    def get_parents(self, child_key: str) -> List[Dict]:
        """查父节点（返回父节点的业务信息）

        首期 tree 下 child 唯一，返回 0 或 1 条。

        参数:
            child_key: 子节点业务 key

        返回:
            List[Dict]: 父节点业务信息列表
        """
        self._check_dependencies()

        child = self._node_repo.find_one({self._node_key_field: child_key})
        if not child:
            return []

        edges = self._repo.find_parents(child['id'])
        if not edges:
            return []

        return self._assemble_nodes(edges, id_field='parent_id')

    def get_subtree(self, root_key: str,
                    strict: bool = False) -> List[Dict]:
        """查子树（所有后代，利用 tree_id 前缀）

        参数:
            root_key: 子树根节点业务 key
            strict: True 时若 tree_id 未维护则抛异常；
                    False（默认）时静默返回空

        返回:
            List[Dict]: 后代节点业务信息列表

        异常:
            ValueError: strict=True 且 tree_id 未维护
        """
        self._check_dependencies()

        root = self._node_repo.find_one({self._node_key_field: root_key})
        if not root:
            return []

        tree_id = root.get('tree_id')
        if not tree_id:
            if strict:
                raise ValueError(
                    f"节点 {root_key} 的 tree_id 未维护，无法查子树"
                )
            return []

        edges = self._repo.find_subtree_by_path(tree_id)
        if not edges:
            return []

        return self._assemble_nodes(edges, id_field='node_ref_id')

    def remove_edge(self, parent_key: str, child_key: str) -> bool:
        """删边（硬删，边表无软删除语义）

        参数:
            parent_key: 父节点业务 key
            child_key: 子节点业务 key

        返回:
            bool: True 表示删除成功
        """
        self._check_dependencies()

        parent = self._node_repo.find_one({self._node_key_field: parent_key})
        child = self._node_repo.find_one({self._node_key_field: child_key})
        if not parent or not child:
            return False

        edge = self._repo.find_edge(parent['id'], child['id'])
        if not edge:
            return False

        return self._repo.delete(edge['id'], soft=False)

    def reorder(self, parent_key: str, child_key: str,
                order_no: int) -> bool:
        """调整同级顺序

        参数:
            parent_key: 父节点业务 key
            child_key: 子节点业务 key
            order_no: 新的顺序号

        返回:
            bool: True 表示调整成功
        """
        self._check_dependencies()

        parent = self._node_repo.find_one({self._node_key_field: parent_key})
        child = self._node_repo.find_one({self._node_key_field: child_key})
        if not parent or not child:
            return False

        edge = self._repo.find_edge(parent['id'], child['id'])
        if not edge:
            return False

        return self._repo.update(edge['id'], order_no=order_no)

    # ==================== 内部辅助 ====================

    def _assemble_nodes(self, edges: List[Dict],
                        id_field: str) -> List[Dict]:
        """按边列表查节点业务信息，组装返回

        参数:
            edges: 边记录列表
            id_field: 边中存放节点 id 的字段（'node_ref_id' 或 'parent_id'）

        返回:
            List[Dict]: 节点业务信息列表，附带 _order_no

        说明:
            逐条查节点表（简化实现）；
            如需优化，可改为批量 IN 查询（需节点表 Repository 支持）。
        """
        result = []
        for edge in edges:
            node_id = edge.get(id_field)
            if node_id is None:
                continue
            node = self._node_repo.get_by_id(node_id)
            if node:
                node['_order_no'] = edge.get('order_no')
                node['_edge_id'] = edge.get('id')
                result.append(node)
        return result