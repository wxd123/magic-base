
# magic_base/protocol/pipeline/data_class/commands.py
from dataclasses import dataclass, field
from typing import  Optional, Dict, Any
from .step import Step
@dataclass
class CommandConfig(Step):
    """命令配置 - 代表一个具体的命令执行"""
    
    command: str                        # 命令名称，如 "java:clean", "java:generate"   
    type: str = "command"               # 步骤类型，固定为 "command"
    id: Optional[str] = None            # 源目录
    name: Optional[str] = None          # 输出目录 
    model: Optional[str] = None         # 可选的模型名称，适用于需要模型支持的命令
    source_dir: Optional[str] = None    # 源目录
    output_dir: Optional[str] = None    # 输出目录
    timeout: Optional[int] = None       # 超时时间（秒）
    params: Dict[str, Any] = field(default_factory=dict)  # 额外参数
    
    def __post_init__(self):
        """初始化后处理"""
        # 如果没有提供 id，自动生成
        if not self.id:
            self.id = self.command
        # 如果没有提供 name，使用 command
        if not self.name:
            self.name = self.command
    
    
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CommandConfig":
        """从字典创建命令配置"""
        # 提取已知字段
        command = data.get("command")
        if not command:
            raise KeyError("命令配置缺少必需字段: command")       
        
        
        # 剩余字段作为额外参数
        params = {k: v for k, v in data.items() 
                 if k not in ["command", "source_dir", "output_dir", "id", "name", "model", "timeout"]}
        
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            command=command,
            source_dir=data.get("source_dir"),
            output_dir=data.get("output_dir"),
            model=data.get("model"),
            timeout=data.get("timeout"),
            params=params
        )