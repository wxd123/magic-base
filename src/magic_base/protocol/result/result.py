"""
统一结果信封模块

提供标准化的操作结果封装，用于 Agent 调用、工具执行、工作流步骤的返回值。
支持泛型，可以携带不同类型的业务数据。

设计目标：
- 统一：所有组件返回相同格式
- 可追踪：包含 request_id 支持全链路追踪
- 类型安全：通过泛型支持 IDE 类型推断
- 轻量：只做数据传输，不包含业务逻辑

使用示例：
    # 返回患者数据
    result = Result.success(
        request_id="req_123",
        output=PatientData(id="456", name="张三")
    )
    
    # 返回错误
    result = Result.error(
        request_id="req_123",
        error_code="AGENT_TIMEOUT",
        error_message="执行超时"
    )
    
    # 检查结果
    if result.is_success:
        patient = result.output  # 类型: PatientData
    else:
        print(f"错误: {result.error_message}")
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional, Dict, Generic, TypeVar
from enum import Enum
from typing import TypeVar, Any

class ResultStatus(str, Enum):
    """
    结果状态枚举
    
    定义操作执行后的状态类型，用于区分不同的执行结果。
    """
    SUCCESS = "success"
    """执行成功，output 字段包含有效数据"""
    
    ERROR = "error"
    """执行失败，error_code 和 error_message 包含错误信息"""
    
    PENDING = "pending"
    """异步任务等待中，需要通过轮询获取最终结果"""


# 泛型类型变量
# 改为（Python 3.10 兼容）


# 不设置 default，直接用 Any 作为默认
T = TypeVar('T')
"""输出数据的类型，默认为 Any，不指定泛型时兼容任意类型"""


@dataclass
class Result(Generic[T]):
    """
    统一结果信封 - 泛型版本
    
    所有 Agent、Command、Pipeline 统一使用此结构返回结果。
    通过泛型 T 携带不同类型的业务数据，支持 IDE 类型推断。
    
    设计原则：
        - 只做数据传输，不封装业务逻辑
        - 成功时 output 有效，失败时 error_code/error_message 有效
        - 不混用成功和失败字段（要么有 output，要么有 error_code）
    
    Attributes:
        status: 执行状态，决定 success/error/pending
        request_id: 全链路请求ID，用于追踪和日志关联
        output: 成功时的输出数据，类型由泛型 T 决定
        error_code: 失败时的错误码，用于程序化处理
        error_message: 失败时的错误描述，用于日志和展示
        timestamp: 结果生成时间戳，用于时序追踪
        metadata: 额外元数据，如耗时、重试次数、Agent版本等
    
    Example:
        >>> # 成功结果
        >>> result = Result.success(
        ...     request_id="req_123",
        ...     output={"patient_id": "456", "score": 95}
        ... )
        >>> result.is_success
        True
        >>> result.output["patient_id"]
        '456'
        
        >>> # 失败结果
        >>> result = Result.error(
        ...     request_id="req_123",
        ...     error_code="AGENT_TIMEOUT",
        ...     error_message="Agent execution exceeded 30s limit"
        ... )
        >>> result.is_error
        True
        >>> result.error_code
        'AGENT_TIMEOUT'
        
        >>> # 泛型使用
        >>> def get_patient(id: str) -> Result[PatientData]:
        ...     patient = PatientData(id=id, name="张三")
        ...     return Result.success(request_id="req_123", output=patient)
        >>> result = get_patient("456")
        >>> if result.is_success:
        ...     patient = result.output  # IDE 知道类型是 PatientData
        ...     print(patient.name)
    """
    status: ResultStatus
    """执行状态"""
    
    request_id: str
    """全链路请求ID，用于追踪和日志关联"""
    
    output: Optional[T] = None
    """成功时的输出数据，类型由泛型 T 决定"""
    
    error_code: Optional[str] = None
    """失败时的错误码，用于程序化处理"""
    
    error_message: Optional[str] = None
    """失败时的错误描述，用于日志和展示"""
    
    timestamp: datetime = field(default_factory=datetime.now)
    """结果生成时间戳"""
    
    metadata: Optional[Dict[str, Any]] = None
    """
    额外元数据
    
    可包含：
    - duration_ms: 执行耗时（毫秒）
    - retry_count: 重试次数
    - agent_version: Agent版本号
    - sandbox_used: 是否使用沙箱
    等自定义字段
    """
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典
        
        递归处理 output 对象，如果对象有 to_dict 方法则调用。
        确保结果可以被 JSON 序列化。
        
        Returns:
            Dict[str, Any]: 字典格式的结果对象
            
        Example:
            >>> result = Result.success(
            ...     request_id="req_123",
            ...     output={"key": "value"},
            ...     metadata={"duration_ms": 150}
            ... )
            >>> result.to_dict()
            {
                "status": "success",
                "request_id": "req_123",
                "timestamp": "2025-01-01T00:00:00",
                "output": {"key": "value"},
                "metadata": {"duration_ms": 150}
            }
        """
        result = {
            "status": self.status.value,
            "request_id": self.request_id,
            "timestamp": self.timestamp.isoformat()
        }
        
        # 添加输出数据
        if self.output is not None:
            # 如果 output 有 to_dict 方法，调用它
            if hasattr(self.output, 'to_dict'):
                result["output"] = self.output.to_dict()
            else:
                result["output"] = self.output
        
        # 添加错误信息
        if self.error_code is not None:
            result["error_code"] = self.error_code
            result["error_message"] = self.error_message
        
        # 添加元数据
        if self.metadata is not None:
            result["metadata"] = self.metadata
        
        return result
    
    def to_json(self) -> str:
        """
        转换为JSON字符串
        
        自动处理 datetime 等非标准类型。
        
        Returns:
            str: JSON格式的字符串
            
        Example:
            >>> result = Result.success(request_id="req_123", output="ok")
            >>> result.to_json()
            '{"status": "success", "request_id": "req_123", "timestamp": "2025-01-01T00:00:00", "output": "ok"}'
        """
        import json
        return json.dumps(self.to_dict(), default=str, ensure_ascii=False)
    
    @property
    def is_success(self) -> bool:
        """
        是否成功
        
        Returns:
            bool: True 表示执行成功，False 表示非成功状态
        """
        return self.status == ResultStatus.SUCCESS
    
    @property
    def is_error(self) -> bool:
        """
        是否失败
        
        Returns:
            bool: True 表示执行失败，False 表示非失败状态
        """
        return self.status == ResultStatus.ERROR
    
    @classmethod
    def success(cls, request_id: str, output: T, **kwargs) -> 'Result[T]':
        """
        创建成功结果
        
        Args:
            request_id: 全链路请求ID（必填）
            output: 成功时的输出数据，类型为 T
            **kwargs: 其他字段（metadata 等）
            
        Returns:
            Result[T]: 状态为 SUCCESS 的 Result 实例
            
        Example:
            >>> result = Result.success(
            ...     request_id="req_123",
            ...     output={"patient_id": "456"},
            ...     metadata={"duration_ms": 150}
            ... )
        """
        return cls(
            status=ResultStatus.SUCCESS,
            request_id=request_id,
            output=output,
            **kwargs
        )
    
    @classmethod
    def error(cls, request_id: str, error_code: str, error_message: str, **kwargs) -> 'Result[Any]':
        """
        创建失败结果
        
        Args:
            request_id: 全链路请求ID（必填）
            error_code: 错误码，用于程序化处理
            error_message: 错误描述，用于日志和展示
            **kwargs: 其他字段（metadata 等）
            
        Returns:
            Result[Any]: 状态为 ERROR 的 Result 实例（泛型为 Any）
            
        Example:
            >>> result = Result.error(
            ...     request_id="req_123",
            ...     error_code="AGENT_TIMEOUT",
            ...     error_message="执行超时",
            ...     metadata={"timeout_seconds": 30}
            ... )
        """
        return cls(
            status=ResultStatus.ERROR,
            request_id=request_id,
            error_code=error_code,
            error_message=error_message,
            **kwargs
        )