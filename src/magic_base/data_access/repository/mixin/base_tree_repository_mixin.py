# magic_base/data_access/repository/base_tree_repository_mixin.py
"""
TreeRepositoryMixin - 树结构数据访问 Mixin

职责：
    提供层次表（parent_id / node_ref_id / edge_type / order_no / tree_id）的
    专属数据访问原语。

设计理念：
    - 与 CUDRepositoryMixin / QueryRepositoryMixin 同层，可叠加
    - 只做数据访问，不做业务判断
    - 首期只实现 tree 边，mount 预留
    - 所有方法默认 edge_type='tree'

依赖：
    宿主类（Repository）必须提供：
    - self._table_name : str          # 层次表名
    - self._get_session() : Session   # 会话
    - self.fetch_all / fetch_one      # 原生 SQL 查询（来自 QueryRepositoryMixin）
    - self.create / update / delete   # CUD（来自 CUDRepositoryMixin）
"""

from typing import Dict, List, Optional, Any, Generic, TypeVar
from abc import abstractmethod

T = TypeVar('T')


class TreeRepositoryMixin(Generic[T]):
    """树结构数据访问 Mixin"""

    # ==================== 边查询 ====================

    def find_edge(self, parent_id: int, node_ref_id: int,
                  edge_type: str = 'tree') -> Optional[Dict]:
        """查单条边

        参数:
            parent_id: 父节点 id
            node_ref_id: 子节点 id
            edge_type: 边类型，默认 'tree'

        返回:
            Optional[Dict]: 边记录，未找到返回 None
        """
        return self.find_one({
            'parent_id': parent_id,
            'node_ref_id': node_ref_id,
            'edge_type': edge_type,
        })

    def find_children(self, parent_id: int,
                      edge_type: str = 'tree',
                      order_by: str = 'order_no ASC') -> List[Dict]:
        """查直接子节点（一层）

        参数:
            parent_id: 父节点 id
            edge_type: 边类型，默认 'tree'
            order_by: 排序，默认按 order_no

        返回:
            List[Dict]: 子边列表
        """
        return self.find(
            conditions={'parent_id': parent_id, 'edge_type': edge_type},
            order_by=order_by,
        )

    def find_parents(self, node_ref_id: int,
                     edge_type: str = 'tree') -> List[Dict]:
        """查父节点（一层）

        首期 tree 下 child 唯一，返回 0 或 1 条；
        mount 后续实现时可能多父。

        参数:
            node_ref_id: 子节点 id
            edge_type: 边类型，默认 'tree'

        返回:
            List[Dict]: 父边列表
        """
        return self.find(
            conditions={'node_ref_id': node_ref_id, 'edge_type': edge_type},
        )

    def has_parent(self, node_ref_id: int,
                   edge_type: str = 'tree') -> bool:
        """检查子节点是否已有父（用于唯一归属校验）

        参数:
            node_ref_id: 子节点 id
            edge_type: 边类型，默认 'tree'

        返回:
            bool: True 表示已有父
        """
        return self.find_one({
            'node_ref_id': node_ref_id,
            'edge_type': edge_type,
        }) is not None

    # ==================== 子树查询 ====================

    def find_subtree_by_path(self, tree_id_prefix: str,
                             edge_type: str = 'tree',
                             order_by: str = 'tree_id ASC') -> List[Dict]:
        """按 tree_id 前缀查子树（利用冒号分隔路径）

        参数:
            tree_id_prefix: 路径前缀，如 '1:3'
            edge_type: 边类型，默认 'tree'
            order_by: 排序

        返回:
            List[Dict]: 子树边列表

        注意:
            走 fetch_all 手写 SQL（LIKE 查询），因为 Repository 的 find 只支持等值。
        """
        sql = (
            f"SELECT * FROM {self._table_name} "
            f"WHERE tree_id LIKE :prefix AND edge_type = :edge_type "
            f"ORDER BY {order_by}"
        )
        return self.fetch_all(sql, {
            'prefix': f"{tree_id_prefix}:%",
            'edge_type': edge_type,
        })

    def find_edges_by_parents(self, parent_ids: List[int],
                              edge_type: str = 'tree') -> List[Dict]:
        """批量查多个父的直接子边（用于批量构造树）

        参数:
            parent_ids: 父节点 id 列表
            edge_type: 边类型

        返回:
            List[Dict]: 边列表

        注意:
            走 fetch_all 手写 SQL（IN 查询），find 只支持等值单值。
        """
        if not parent_ids:
            return []
        placeholders = ', '.join(f':p{i}' for i in range(len(parent_ids)))
        sql = (
            f"SELECT * FROM {self._table_name} "
            f"WHERE parent_id IN ({placeholders}) AND edge_type = :edge_type "
            f"ORDER BY parent_id, order_no ASC"
        )
        params = {f'p{i}': pid for i, pid in enumerate(parent_ids)}
        params['edge_type'] = edge_type
        return self.fetch_all(sql, params)

    # ==================== 环检测 / 祖先链 ====================

    def find_ancestor_path(self, node_ref_id: int,
                           edge_type: str = 'tree') -> List[int]:
        """上溯查祖先链（用于环检测）

        参数:
            node_ref_id: 子节点 id
            edge_type: 边类型

        返回:
            List[int]: 祖先 id 列表（从直接父到根）

        注意:
            首期用逐层上溯（深度小，性能可接受）；
            若 tree_id 已维护，可改为 tree_id 前缀解析，O(1)。
        """
        ancestors = []
        current = node_ref_id
        visited = set()  # 防御：万一有环，避免死循环
        while True:
            if current in visited:
                break
            visited.add(current)
            edge = self.find_one({
                'node_ref_id': current,
                'edge_type': edge_type,
            })
            if not edge:
                break
            parent = edge['parent_id']
            ancestors.append(parent)
            current = parent
        return ancestors

    def is_descendant(self, ancestor_id: int, node_ref_id: int,
                      edge_type: str = 'tree') -> bool:
        """检查 node_ref_id 是否是 ancestor_id 的后代（用于环检测）

        参数:
            ancestor_id: 祖先节点 id
            node_ref_id: 待检查节点 id
            edge_type: 边类型

        返回:
            bool: True 表示 node_ref_id 在 ancestor_id 的子树中

        注意:
            若 tree_id 已维护，可改为：
                node.tree_id.startswith(ancestor.tree_id + ':')
            O(1)。
        """
        return ancestor_id in self.find_ancestor_path(node_ref_id, edge_type)

    # ==================== order_no 管理 ====================

    def get_max_order_no(self, parent_id: int,
                         edge_type: str = 'tree') -> Optional[int]:
        """查同级最大 order_no（用于 add_edge 赋新值）

        参数:
            parent_id: 父节点 id
            edge_type: 边类型

        返回:
            Optional[int]: 最大 order_no，无子边时返回 None
        """
        children = self.find_children(parent_id, edge_type)
        orders = [c['order_no'] for c in children if c.get('order_no') is not None]
        return max(orders) if orders else None