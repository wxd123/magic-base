# magic_base/crypto/cert.py
"""
证书验证基类
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class CertValidatorBase(ABC):
    """证书验证器基类"""
    
    @abstractmethod
    def verify_signature(self, data: bytes, signature: bytes, cert_path: str) -> bool:
        """验证签名"""
        pass
    
    @abstractmethod
    def get_cert_info(self, cert_path: str) -> Dict[str, Any]:
        """获取证书信息"""
        pass
    
    @abstractmethod
    def verify_chain(self, cert_path: str, ca_bundle_path: str) -> bool:
        """验证证书链"""
        pass