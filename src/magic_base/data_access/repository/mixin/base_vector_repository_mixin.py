# magic_base/data_access/repository/mixin/base_vector_repository_mixin.py
"""
VectorRepositoryMixin - 向量结构数据访问 Mixin

职责：
    提供向量表（owner_key / encoding_key / vector_value 三元组）的
    专属数据访问原语。

设计理念：
    - 与 CUDRepositoryMixin / QueryRepositoryMixin / TreeRepositoryMixin 同层，可叠加
    - 只做数据访问，不做业务判断
    - 字段名可配置（可选参数，带默认值）
    - 默认字段名：member_key / vector_encoding_key / vector_encoding_value

依赖（宿主类必须提供）：
    - self._table_name : str          # 向量表名
    - self._get_session() : Session   # 会话
    - self.fetch_all / fetch_one      # 原生 SQL 查询（来自 QueryRepositoryMixin）
    - self.find_one / find            # 条件查询（来自 QueryRepositoryMixin）
    - self.create / update / delete   # CUD（来自 CUDRepositoryMixin）
"""

from typing import Dict, List, Optional, Any, Generic, TypeVar

T = TypeVar('T')


class VectorRepositoryMixin(Generic[T]):
    """向量结构数据访问 Mixin"""

    # ==================== 单条查询 ====================

    def find_vector(self, owner_key, encoding_key,
                    owner_field: str = 'member_key',
                    encoding_field: str = 'vector_encoding_key',
                    ) -> Optional[Dict]:
        """按双 key 查单条向量值

        参数:
            owner_key: 归属 key（如 member_key）
            encoding_key: 编码方式 key（如 vector_encoding_key）
            owner_field: 归属字段名，默认 'member_key'
            encoding_field: 编码方式字段名，默认 'vector_encoding_key'

        返回:
            Optional[Dict]: 向量记录，未找到返回 None
        """
        return self.find_one({
            owner_field: owner_key,
            encoding_field: encoding_key,
        })

    # ==================== 批量查询 ====================

    def find_vectors_by_owner(self, owner_key,
                              owner_field: str = 'member_key',
                              order_by: Optional[str] = None,
                              ) -> List[Dict]:
        """按归属 key 查全部向量值（不同编码方式）

        参数:
            owner_key: 归属 key
            owner_field: 归属字段名，默认 'member_key'
            order_by: 排序，可选

        返回:
            List[Dict]: 向量记录列表
        """
        return self.find(
            conditions={owner_field: owner_key},
            order_by=order_by,
        )

    # ==================== 编码方式列表（distinct） ====================

    def list_encodings(self, owner_key,
                       owner_field: str = 'member_key',
                       encoding_field: str = 'vector_encoding_key',
                       ) -> List[str]:
        """列某归属下所有编码方式（distinct）

        参数:
            owner_key: 归属 key
            owner_field: 归属字段名，默认 'member_key'
            encoding_field: 编码方式字段名，默认 'vector_encoding_key'

        返回:
            List[str]: 编码方式 key 列表（去重）

        注意:
            走 fetch_all 手写 SQL（DISTINCT 查询），
            因为 Repository 的 find 只支持等值，不支持 DISTINCT。
        """
        sql = (
            f"SELECT DISTINCT {encoding_field} AS enc "
            f"FROM {self._table_name} "
            f"WHERE {owner_field} = :owner_key"
        )
        rows = self.fetch_all(sql, {'owner_key': owner_key})
        return [r['enc'] for r in rows if r.get('enc') is not None]

    # ==================== 删除 ====================

    def delete_vector(self, owner_key, encoding_key,
                      owner_field: str = 'member_key',
                      encoding_field: str = 'vector_encoding_key',
                      soft: bool = True,
                      ) -> bool:
        """按双 key 删除向量值

        参数:
            owner_key: 归属 key
            encoding_key: 编码方式 key
            owner_field: 归属字段名，默认 'member_key'
            encoding_field: 编码方式字段名，默认 'vector_encoding_key'
            soft: 是否软删除，默认 True

        返回:
            bool: True 表示删除成功，False 表示记录不存在
        """
        record = self.find_vector(owner_key, encoding_key,
                                  owner_field, encoding_field)
        if not record:
            return False
        return self.delete(record['id'], soft=soft)