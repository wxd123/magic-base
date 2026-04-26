# magic_base/crypto/crypto.py
"""
加密基类
"""

from abc import ABC, abstractmethod


class CryptoBase(ABC):
    """加密工具基类"""
    
    @abstractmethod
    def encrypt(self, data: bytes, key: bytes) -> bytes:
        """加密数据"""
        pass
    
    @abstractmethod
    def decrypt(self, data: bytes, key: bytes) -> bytes:
        """解密数据"""
        pass
    
    @abstractmethod
    def hash(self, data: bytes) -> str:
        """计算哈希值"""
        pass
    
    @abstractmethod
    def generate_key(self) -> bytes:
        """生成密钥"""
        pass