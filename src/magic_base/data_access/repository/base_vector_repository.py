# magic_base/data_access/repository/base_vector_repository.py
"""
BaseVectorRepository - 向量结构专属 Repository 基类

定位：
    MagicBaseRepository + VectorRepositoryMixin 的预设组合。
    向量表专属 Repository 直接继承即用。

使用方式：
    class SystemModelMemberVectorRepository(
        BaseVectorRepository[SystemModelMemberVectors]
    ):
        pass

等价于：
    class SystemModelMemberVectorRepository(
        MagicBaseRepository[SystemModelMemberVectors],
        VectorRepositoryMixin[SystemModelMemberVectors],
    ):
        pass
"""

from typing import TypeVar

from .base_repository import MagicBaseRepository
from .mixin.base_vector_repository_mixin import VectorRepositoryMixin


T = TypeVar('T')


class BaseVectorRepository(
    MagicBaseRepository[T],
    VectorRepositoryMixin[T],
):
    """
    向量结构专属 Repository 基类

    组合：
        - MagicBaseRepository：通用 CRUD（CUD + Query）
        - VectorRepositoryMixin：向量专属数据访问

    提供能力：
        - 通用：create / update / delete / find / find_one / count / paginate
        - 向量专属：find_vector / find_vectors_by_owner
                   / list_encodings / delete_vector

    注意：
        通常通过子类继承使用，子类需指定泛型类型 T（向量表 ORM 模型）。
        默认字段名：member_key / vector_encoding_key / vector_encoding_value。
        如需自定义字段名，调用时传 owner_field / encoding_field。
    """
    pass