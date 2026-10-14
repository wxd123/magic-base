# magic_base/data_access/service/mixin/base_vector_service_mixin.py
"""
VectorServiceMixin - 向量结构业务逻辑 Mixin

职责：
    实现向量业务的完整逻辑：upsert 语义（有则更新无则创建）、
    按双 key 查、按归属查、列编码方式、软删除。

设计理念：
    - 与 Repository 层的 VectorRepositoryMixin 对应
    - Repository 管数据访问，Mixin 管业务逻辑
    - 字段名可配置（可选参数，带默认值）
    - upsert 用两步：find → update / create（Repository 无原生 upsert）

依赖（宿主 Service 必须提供）：
    - self._repo : BaseVectorRepository 实例（向量表）

使用方式：
    class SystemModelMemberVectorService(
        BaseVectorService[SystemModelMemberVectors]
    ):
        def __init__(self):
            super().__init__(SystemModelMemberVectorRepository())
"""

from typing import Dict, List, Optional, Any, Generic, TypeVar

T = TypeVar('T')


class VectorServiceMixin(Generic[T]):
    """向量结构业务逻辑 Mixin"""

    # ==================== 写操作（upsert） ====================

    def set_vector(self, owner_key, encoding_key, value,
                   owner_field: str = 'member_key',
                   encoding_field: str = 'vector_encoding_key',
                   value_field: str = 'vector_encoding_value',
                   ) -> Dict:
        """设置向量值（upsert 语义）

        业务规则：
            - 若 (owner_key, encoding_key) 已存在 → 更新 value
            - 若不存在 → 创建新记录

        参数:
            owner_key: 归属 key（如 member_key）
            encoding_key: 编码方式 key（如 vector_encoding_key）
            value: 向量值
            owner_field: 归属字段名，默认 'member_key'
            encoding_field: 编码方式字段名，默认 'vector_encoding_key'
            value_field: 向量值字段名，默认 'vector_encoding_value'

        返回:
            Dict: 设置后的向量记录

        注意:
            Repository 无原生 upsert，这里用两步：
            先 find_vector，存在则 update，否则 create。
            并发场景下唯一约束可兜底（Duplicate 报错）。
        """
        existing = self._repo.find_vector(
            owner_key, encoding_key, owner_field, encoding_field
        )
        if existing:
            self._repo.update(existing['id'], **{value_field: value})
            # update 返回 bool，重新查一次拿最新数据
            return self._repo.find_vector(
                owner_key, encoding_key, owner_field, encoding_field
            )
        else:
            instance = self._repo.create(**{
                owner_field: owner_key,
                encoding_field: encoding_key,
                value_field: value,
            })
            # create 返回 ORM 实例，转 dict
            return instance.to_dict() if hasattr(instance, 'to_dict') else instance

    # ==================== 读操作 ====================

    def get_vector(self, owner_key, encoding_key,
                   owner_field: str = 'member_key',
                   encoding_field: str = 'vector_encoding_key',
                   ) -> Optional[Dict]:
        """按双 key 查单个向量值

        参数:
            owner_key: 归属 key
            encoding_key: 编码方式 key
            owner_field: 归属字段名，默认 'member_key'
            encoding_field: 编码方式字段名，默认 'vector_encoding_key'

        返回:
            Optional[Dict]: 向量记录，未找到返回 None
        """
        return self._repo.find_vector(
            owner_key, encoding_key, owner_field, encoding_field
        )

    def get_vectors(self, owner_key,
                    owner_field: str = 'member_key',
                    ) -> List[Dict]:
        """按归属 key 查全部向量值（不同编码方式）

        参数:
            owner_key: 归属 key
            owner_field: 归属字段名，默认 'member_key'

        返回:
            List[Dict]: 向量记录列表
        """
        return self._repo.find_vectors_by_owner(owner_key, owner_field)

    def list_encodings(self, owner_key,
                       owner_field: str = 'member_key',
                       encoding_field: str = 'vector_encoding_key',
                       ) -> List[str]:
        """列某归属下所有编码方式

        参数:
            owner_key: 归属 key
            owner_field: 归属字段名，默认 'member_key'
            encoding_field: 编码方式字段名，默认 'vector_encoding_key'

        返回:
            List[str]: 编码方式 key 列表（去重）
        """
        return self._repo.list_encodings(owner_key, owner_field, encoding_field)

    # ==================== 删除 ====================

    def deprecate_vector(self, owner_key, encoding_key,
                         owner_field: str = 'member_key',
                         encoding_field: str = 'vector_encoding_key',
                         ) -> bool:
        """废弃向量值（软删除）

        参数:
            owner_key: 归属 key
            encoding_key: 编码方式 key
            owner_field: 归属字段名，默认 'member_key'
            encoding_field: 编码方式字段名，默认 'vector_encoding_key'

        返回:
            bool: True 表示删除成功，False 表示记录不存在
        """
        return self._repo.delete_vector(
            owner_key, encoding_key, owner_field, encoding_field, soft=True
        )