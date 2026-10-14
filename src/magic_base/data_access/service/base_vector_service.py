# magic_base/data_access/service/base_vector_service.py
"""
BaseVectorService - 向量结构专属 Service 基类

定位：
    BaseService + VectorServiceMixin 的预设组合。
    向量业务 Service 直接继承即用。

使用方式：
    class SystemModelMemberVectorService(
        BaseVectorService[SystemModelMemberVectors]
    ):
        def __init__(self):
            super().__init__(SystemModelMemberVectorRepository())

等价于：
    class SystemModelMemberVectorService(
        BaseService[SystemModelMemberVectors],
        VectorServiceMixin[SystemModelMemberVectors],
    ):
        ...
"""

from typing import TypeVar

from .base_service import BaseService
from .mixin.base_vector_service_mixin import VectorServiceMixin


T = TypeVar('T')


class BaseVectorService(
    BaseService[T],
    VectorServiceMixin[T],
):
    """
    向量结构专属 Service 基类

    组合：
        - BaseService：通用 CRUD 透传（含 *_by_key）
        - VectorServiceMixin：向量专属业务逻辑

    提供能力：
        - 通用：get_by_key / update_by_key / delete_by_key / find / find_one
                 / exists / count / paginate / create / update / delete
        - 向量专属：set_vector / get_vector / get_vectors
                   / list_encodings / deprecate_vector

    子类需在 __init__ 里注入：
        - self._repo : BaseVectorRepository 实例（super().__init__ 参数）

    注意：
        通常通过子类继承使用，子类需指定泛型类型 T（向量表 ORM 模型）。
        默认字段名：member_key / vector_encoding_key / vector_encoding_value。
        如需自定义字段名，调用时传 owner_field / encoding_field / value_field。
    """
    pass