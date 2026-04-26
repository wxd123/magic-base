# magic_base/exceptions/base.py
"""
异常基类
"""


class MagicBaseError(Exception):
    """magic-base 基础异常类"""
    pass


class PlatformNotSupportedError(MagicBaseError):
    """当前平台不支持"""
    pass


class DatabaseError(MagicBaseError):
    """数据库错误"""
    pass


class ConfigurationError(MagicBaseError):
    """配置错误"""
    pass


class DetectionError(MagicBaseError):
    """检测错误"""
    pass


class CryptoError(MagicBaseError):
    """加密错误"""
    pass


class ValidationError(MagicBaseError):
    """验证错误"""
    pass