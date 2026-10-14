# magic_base/data_access/util/base_uniqueness_checker.py
"""
BaseUniquenessChecker - 唯一性校验工具类

职责：
    提供"检查记录是否唯一"的通用工具方法。
    纯数据访问层工具，只依赖 Repository 的查询能力。

设计理念：
    - 无状态，所有方法为静态方法
    - 只做数据访问层检查，不做业务规则判断
    - 检查失败时抛 ValueError，也可只检查不抛
    - 与 Repository 解耦：接受任意有 find_one 的 Repository

使用方式：
    from magic_base.data_access.util.base_uniqueness_checker import BaseUniquenessChecker

    # 检查并抛异常
    BaseUniquenessChecker.check(repo, 'node_key', 'admin_system')

    # 只检查，返回 bool
    if BaseUniquenessChecker.exists(repo, 'node_key', 'admin_system'):
        print("已存在")

    # 多字段联合唯一
    BaseUniquenessChecker.check_multi(
        repo,
        {'member_key': 'm1', 'vector_encoding_key': 'enc_A'},
    )

注意：
    本工具与"树结构"无关。
    - 树的 child 唯一归属 → TreeServiceMixin.add_edge 里的 has_parent
    - 业务 key 唯一（node_key / model_key / member_key）→ 本工具
"""

from typing import Dict, Any, Optional


class BaseUniquenessChecker:
    """唯一性校验工具类（无状态，静态方法）"""

    # ==================== 单字段唯一 ====================

    @staticmethod
    def check(repo, key_field: str, key_value: Any,
              message: Optional[str] = None) -> None:
        """检查单字段唯一性，存在则抛 ValueError

        参数:
            repo: Repository 实例（需提供 find_one）
            key_field: 唯一字段名
            key_value: 唯一字段值
            message: 自定义错误信息，为 None 时使用默认信息

        异常:
            ValueError: 记录已存在

        示例:
            BaseUniquenessChecker.check(repo, 'node_key', 'admin_system')
            # 若已存在，抛 ValueError: node_key='admin_system' 已存在
        """
        if repo.find_one({key_field: key_value}) is not None:
            raise ValueError(
                message or f"{key_field}={key_value!r} 已存在"
            )

    # ==================== 多字段联合唯一 ====================

    @staticmethod
    def check_multi(repo, conditions: Dict[str, Any],
                    message: Optional[str] = None) -> None:
        """检查多字段联合唯一性，存在则抛 ValueError

        参数:
            repo: Repository 实例
            conditions: 联合唯一条件，如 {'member_key': 'm1', 'vector_encoding_key': 'enc_A'}
            message: 自定义错误信息

        异常:
            ValueError: 记录已存在

        示例:
            BaseUniquenessChecker.check_multi(
                repo,
                {'member_key': 'm1', 'vector_encoding_key': 'enc_A'},
            )
        """
        if repo.find_one(conditions) is not None:
            raise ValueError(
                message or f"记录已存在: {conditions}"
            )

    # ==================== 只检查，不抛 ====================

    @staticmethod
    def exists(repo, key_field: str, key_value: Any) -> bool:
        """检查单字段是否存在，返回 bool（不抛异常）

        参数:
            repo: Repository 实例
            key_field: 唯一字段名
            key_value: 唯一字段值

        返回:
            bool: True 表示已存在

        示例:
            if BaseUniquenessChecker.exists(repo, 'node_key', 'x'):
                print("已存在")
        """
        return repo.find_one({key_field: key_value}) is not None

    @staticmethod
    def exists_multi(repo, conditions: Dict[str, Any]) -> bool:
        """检查多字段联合是否存在，返回 bool（不抛异常）

        参数:
            repo: Repository 实例
            conditions: 联合唯一条件

        返回:
            bool: True 表示已存在
        """
        return repo.find_one(conditions) is not None

    # ==================== 排除自身（更新场景） ====================

    @staticmethod
    def check_exclude_self(repo, key_field: str, key_value: Any,
                           exclude_id: int,
                           message: Optional[str] = None) -> None:
        """检查单字段唯一性，排除自身记录（更新场景）

        参数:
            repo: Repository 实例
            key_field: 唯一字段名
            key_value: 唯一字段值
            exclude_id: 排除的记录 id（自身）
            message: 自定义错误信息

        异常:
            ValueError: 其他记录已占用该 key

        示例:
            # 更新 id=1 的记录，检查 node_key 是否被别的记录占用
            BaseUniquenessChecker.check_exclude_self(
                repo, 'node_key', 'x', exclude_id=1
            )
        """
        record = repo.find_one({key_field: key_value})
        if record is not None and record.get('id') != exclude_id:
            raise ValueError(
                message or f"{key_field}={key_value!r} 已被其他记录占用"
            )