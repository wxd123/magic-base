"""
统一请求信封模块

提供标准化的请求封装，用于 Agent 调用、工具执行、工作流步骤的输入。
支持泛型，可以携带不同类型的业务数据。

设计目标：
- 统一：所有组件使用相同的请求格式
- 可追踪：包含 request_id 支持全链路追踪
- 类型安全：通过泛型支持 IDE 类型推断
- 灵活：支持同步、异步、流式三种请求方式

使用示例：
    # 同步请求
    request = Request[QualityInput].create(
        request_id="req_123",
        input=QualityInput(document_id="doc_456")
    )
    
    # 异步请求
    request = Request.async_request(
        request_id="req_123",
        input=QualityInput(document_id="doc_456")
    )
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional, Dict, Generic, TypeVar
from enum import Enum


class RequestMethod(str, Enum):
    """
    请求方法枚举
    
    定义请求的执行方式，用于区分不同类型的调用。
    """
    SYNC = "sync"
    """同步请求：调用方等待结果返回"""
    
    ASYNC = "async"
    """异步请求：立即返回任务ID，后续轮询获取结果"""
    
    STREAM = "stream"
    """流式请求：结果分块返回，用于大模型输出等场景"""


I = TypeVar('I')
"""输入数据的类型，默认为 Any，不指定泛型时兼容任意类型"""


@dataclass
class Request(Generic[I]):
    """
    统一请求信封 - 泛型版本
    
    所有 Agent、Command、Pipeline 统一使用此结构接收输入。
    通过泛型 I 携带不同类型的业务数据，支持 IDE 类型推断。
    
    设计原则：
        - 只做数据传输，不封装业务逻辑
        - request_id 是必填字段，用于全链路追踪
        - input 字段承载具体的业务参数
    
    Attributes:
        request_id: 请求ID，全链路追踪标识
        method: 请求方法，决定执行方式（同步/异步/流式）
        input: 输入数据，类型由泛型 I 决定
        timestamp: 请求时间戳，用于时序追踪
        metadata: 额外元数据，如超时时间、重试次数、调用方信息等
    
    Example:
        >>> # 定义输入数据类型
        >>> @dataclass
        ... class QualityInput:
        ...     document_id: str
        ...     document_text: str
        
        >>> # 创建泛型请求
        >>> request = Request[QualityInput].create(
        ...     request_id="req_123",
        ...     input=QualityInput(
        ...         document_id="doc_456",
        ...         document_text="患者因...入院"
        ...     ),
        ...     metadata={"timeout": 30}
        ... )
        >>> request.request_id
        'req_123'
        >>> request.input.document_id
        'doc_456'
        
        >>> # 简单请求（不指定泛型）
        >>> request = Request.create(
        ...     request_id="req_123",
        ...     input={"patient_id": "789"}
        ... )
        
        >>> # 异步请求
        >>> request = Request.async_request(
        ...     request_id="req_123",
        ...     input=QualityInput(document_id="doc_456", document_text="...")
        ... )
        >>> request.method
        <RequestMethod.ASYNC: 'async'>
    """
    request_id: str
    """请求ID，全链路追踪标识，所有日志和审计应包含此字段"""
    
    method: RequestMethod = RequestMethod.SYNC
    """
    请求方法：同步/异步/流式
    
    - SYNC: 调用方阻塞等待结果
    - ASYNC: 立即返回任务ID，调用方轮询获取结果
    - STREAM: 结果分块返回，适用于长文本生成等场景
    """
    
    input: Optional[I] = None
    """输入数据，类型由泛型 I 决定，承载具体的业务参数"""
    
    timestamp: datetime = field(default_factory=datetime.now)
    """请求时间戳，用于时序追踪和性能分析"""
    
    metadata: Optional[Dict[str, Any]] = None
    """
    额外元数据
    
    可包含：
    - timeout: 超时时间（秒）
    - max_retries: 最大重试次数
    - caller: 调用方标识
    - priority: 优先级
    - tenant_id: 租户ID
    等自定义字段
    """
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典
        
        递归处理 input 对象，如果对象有 to_dict 方法则调用。
        确保请求可以被 JSON 序列化，用于日志记录和跨服务传递。
        
        Returns:
            Dict[str, Any]: 字典格式的请求对象
            
        Example:
            >>> request = Request.create(
            ...     request_id="req_123",
            ...     input={"patient_id": "789"},
            ...     metadata={"timeout": 30}
            ... )
            >>> request.to_dict()
            {
                "request_id": "req_123",
                "method": "sync",
                "timestamp": "2025-01-01T00:00:00",
                "input": {"patient_id": "789"},
                "metadata": {"timeout": 30}
            }
        """
        result = {
            "request_id": self.request_id,
            "method": self.method.value,
            "timestamp": self.timestamp.isoformat()
        }
        
        # 添加输入数据
        if self.input is not None:
            # 如果 input 有 to_dict 方法，调用它
            if hasattr(self.input, 'to_dict'):
                result["input"] = self.input.to_dict()
            else:
                result["input"] = self.input
        
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
            >>> request = Request.create(request_id="req_123", input={"key": "value"})
            >>> request.to_json()
            '{"request_id": "req_123", "method": "sync", "timestamp": "2025-01-01T00:00:00", "input": {"key": "value"}}'
        """
        import json
        return json.dumps(self.to_dict(), default=str, ensure_ascii=False)
    
    @classmethod
    def create(cls, request_id: str, input: I, **kwargs) -> 'Request[I]':
        """
        创建请求（同步，默认方式）
        
        Args:
            request_id: 请求ID，全链路追踪标识（必填）
            input: 输入数据，类型为 I
            **kwargs: 其他字段（method、metadata 等）
            
        Returns:
            Request[I]: 请求实例
            
        Example:
            >>> request = Request.create(
            ...     request_id="req_123",
            ...     input={"patient_id": "789"},
            ...     metadata={"timeout": 30}
            ... )
        """
        return cls(
            request_id=request_id,
            input=input,
            **kwargs
        )
    
    @classmethod
    def async_request(cls, request_id: str, input: I, **kwargs) -> 'Request[I]':
        """
        创建异步请求
        
        适用于长时间执行的任务，调用方通过轮询获取结果。
        
        Args:
            request_id: 请求ID，全链路追踪标识（必填）
            input: 输入数据，类型为 I
            **kwargs: 其他字段（metadata 等）
            
        Returns:
            Request[I]: 方法为 ASYNC 的请求实例
            
        Example:
            >>> request = Request.async_request(
            ...     request_id="req_123",
            ...     input=LongRunningTaskInput(data="..."),
            ...     metadata={"callback_url": "https://.../callback"}
            ... )
        """
        return cls(
            request_id=request_id,
            method=RequestMethod.ASYNC,
            input=input,
            **kwargs
        )