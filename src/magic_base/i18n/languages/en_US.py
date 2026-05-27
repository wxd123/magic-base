# magic-base/magic_base/i18n/languages/en.py
from typing import Dict
from ..provider import MessageProvider

class EnglishMessages(MessageProvider):
    """English common messages"""
    
    @property
    def messages(self) -> Dict[str, str]:
        return {
            # Common messages (shared across projects)
            "file_not_found": "File not found: {path}",
            "directory_not_found": "Directory not found: {path}",
            "permission_denied": "Permission denied: {path}",
            # ... more common messages
        }