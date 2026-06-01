
# magic_base/protocol/pipeline/cmd/command.py
from typing import Protocol, runtime_checkable, Any, Dict
from ..data_class import Result, CommandConfig


@runtime_checkable
class Command(Protocol):
    """
    命令协议，定义了命令模式的标准接口。
    
    所有具体命令只需实现 execute 和 name 属性即可符合协议。
    可以可选地实现 validate 方法进行前置条件验证，以及 get_metadata 方法提供元数据。
    
    示例:
        # 方式1: 实现完整接口
        class MyCommand:
            @property
            def name(self) -> str:
                return "my.command"
            
            def execute(self, cmd_config: CommandConfig) -> Result:
                # 执行命令逻辑
                return Result.ok({"output": "processed_value"})
            
            def validate(self) -> None:
                # 验证前置条件
                pass
            
            def get_metadata(self) -> Dict[str, Any]:
                return {"description": "我的命令"}
        
        # 方式2: 最小实现（只有必须的）
        class SimpleCommand:
            @property
            def name(self) -> str:
                return "simple.command"
            
            def execute(self, cmd_config: CommandConfig) -> Result:
                return Result.ok()
        
        # 方式3: 使用函数式风格
        def make_command(cmd_name: str):
            class DynamicCommand:
                @property
                def name(self) -> str:
                    return cmd_name
                
                def execute(self, cmd_config: CommandConfig) -> Result:
                    # 动态命令逻辑
                    return Result.ok()
            return DynamicCommand()
    """
    
    @property
    def name(self) -> str:
        """
        命令名称，用于注册命令的只读属性。
        
        Returns:
            定义的命令注册名称，以.分隔的小写字母，建议总等级不超过3级。
        """
        ...
    
    def execute(self, cmd_config: CommandConfig) -> Result:
        """
        执行命令的核心方法。
        
        Args:
            cmd_config: 命令配置对象
            
        Returns:
            Result 对象，包含执行结果、状态信息和输出数据。
        
        Raises:
            实现类可根据需要抛出特定异常。
        """
        ...
    
    def validate(self) -> None:
        """
        验证命令执行的前置条件（可选实现）。
        
        该方法在 execute 之前调用，用于检查命令执行的要求。
        验证失败时应抛出异常。
        
        Raises:
            验证失败时抛出异常（如 ValueError、KeyError 等）。
        
        示例:
            def validate(self) -> None:
                # 验证逻辑
                pass
        """
        ...  # 注意：这里用 ... 而不是 pass，表示这是可选方法
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        返回命令的元数据信息（可选实现）。
        
        Returns:
            包含命令元数据的字典
        
        示例:
            def get_metadata(self) -> Dict[str, Any]:
                return {
                    "name": "my_command",
                    "description": "执行文件分析",
                    "version": "1.0",
                    "requires_llm": False,
                }
        """
        ...  # 可选方法，不强制实现