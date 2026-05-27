# magic-base/magic_base/i18n/languages/zh.py
from typing import Dict
from ..provider import MessageProvider

class ChineseMessages(MessageProvider):
    """中文通用消息"""
    
    @property
    def messages(self) -> Dict[str, str]:
        return {
            # 通用消息（各项目共享）
            "file_not_found": "文件不存在: {path}",
            "directory_not_found": "目录不存在: {path}",
            "permission_denied": "权限不足: {path}",
            # ... 更多通用消息
        }