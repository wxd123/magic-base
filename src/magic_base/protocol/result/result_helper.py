"""
统一结果信封模块

提供标准化的操作结果封装，用于 Agent 调用、工具执行、工作流步骤的返回值。
支持成功、失败、部分成功、流式输出、异步等待等多种状态。

设计目标：
- 统一：所有组件返回相同格式
- 可追踪：包含 request_id 支持全链路追踪
- 可观测：包含耗时、状态码等元数据
- 易扩展：支持流式输出、批量结果

使用示例：
    # 成功结果
    result = Result.success(
        output={"errors": [], "score": 100},
        request_id="req_123",
        agent_name="quality_agent"
    )
    
    # 失败结果
    result = Result.error(
        code=ErrorCode.AGENT_TIMEOUT,
        message="执行超时",
        request_id="req_123"
    )
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Optional, List, Dict
from enum import StrEnum


class ResultStatus(StrEnum):
    """
    结果状态枚举
    
    定义操作执行后的状态类型，用于区分不同的执行结果。
    """
    SUCCESS = "success"
    """执行成功，output 字段包含有效数据"""
    
    ERROR = "error"
    """执行失败，error 字段包含错误详情"""
    
    PARTIAL = "partial"
    """部分成功，用于批量操作，items 字段包含各子项结果"""
    
    STREAMING = "streaming"
    """流式输出中，非最终结果块，stream_id 标识会话"""
    
    PENDING = "pending"
    """异步任务等待中，output.poll_url 用于轮询结果"""


class ErrorCode(StrEnum):
    """
    错误码枚举
    
    标准化错误类型，便于客户端根据错误码进行差异化处理（如重试、提示、降级）。
    """
    # 客户端错误（4xx）
    BAD_REQUEST = "BAD_REQUEST"
    """请求参数错误"""
    
    UNAUTHORIZED = "UNAUTHORIZED"
    """未认证，需要提供有效的认证凭证"""
    
    FORBIDDEN = "FORBIDDEN"
    """无权限，认证通过但无权访问该资源"""
    
    NOT_FOUND = "NOT_FOUND"
    """资源不存在"""
    
    # Agent 错误
    AGENT_TIMEOUT = "AGENT_TIMEOUT"
    """Agent 执行超时，可重试"""
    
    AGENT_UNAVAILABLE = "AGENT_UNAVAILABLE"
    """Agent 服务不可用，可重试"""
    
    AGENT_INTERNAL_ERROR = "AGENT_INTERNAL_ERROR"
    """Agent 内部错误，不可重试"""
    
    # 网关错误
    GATEWAY_TIMEOUT = "GATEWAY_TIMEOUT"
    """网关调用超时"""
    
    GATEWAY_RATE_LIMITED = "GATEWAY_RATE_LIMITED"
    """请求被限流"""
    
    # 沙箱错误
    SANDBOX_ERROR = "SANDBOX_ERROR"
    """沙箱执行错误"""
    
    SANDBOX_RESOURCE_EXCEEDED = "SANDBOX_RESOURCE_EXCEEDED"
    """沙箱资源超限（CPU/内存/时间）"""
    
    # 工作流错误
    WORKFLOW_INVALID = "WORKFLOW_INVALID"
    """工作流定义无效"""
    
    WORKFLOW_STEP_FAILED = "WORKFLOW_STEP_FAILED"
    """工作流步骤执行失败"""


@dataclass
class ErrorDetail:
    """
    错误详情数据结构
    
    封装错误信息，便于客户端解析和展示。
    
    Attributes:
        code: 错误码，用于程序化处理
        message: 人类可读的错误描述
        details: 可选的额外错误详情（如字段验证失败的具体信息）
    """
    code: ErrorCode
    """错误码，用于程序化处理"""
    
    message: str
    """人类可读的错误描述"""
    
    details: Optional[Dict[str, Any]] = None
    """可选的额外错误详情（如字段验证失败的具体信息）"""
