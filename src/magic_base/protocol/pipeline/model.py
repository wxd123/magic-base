# magic_tool/pipeline/model.py
import os
from typing import Optional, Dict
import requests

# 全局配置，可通过环境变量覆盖
DEFAULT_BASE_URL = os.environ.get("MODEL_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL", "llama3.2")
DEFAULT_TIMEOUT = int(os.environ.get("MODEL_TIMEOUT", "60"))
DEFAULT_TEMPERATURE = float(os.environ.get("MODEL_TEMPERATURE", "0.7"))
DEFAULT_MAX_TOKENS = int(os.environ.get("MODEL_MAX_TOKENS", "2000"))

# 简单缓存（可选，通过环境变量开启）
CACHE_ENABLED = os.environ.get("MODEL_CACHE", "").lower() == "true"
_cache: Dict[str, str] = {}


def llm_generate(
    prompt: str,
    model: Optional[str] = None,
    system: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    timeout: Optional[int] = None,
    base_url: Optional[str] = None,
    cache: Optional[bool] = None,
) -> str:
    """
    调用本地模型生成文本
    
    Args:
        prompt: 用户提示词
        model: 模型名称，默认使用 DEFAULT_MODEL
        system: 系统提示词（可选，部分后端支持）
        temperature: 温度参数，默认 0.7
        max_tokens: 最大生成 token 数，默认 2000
        timeout: 超时秒数，默认 60
        base_url: API 地址，默认使用 DEFAULT_BASE_URL
        cache: 是否使用缓存，默认由 MODEL_CACHE 环境变量决定
    
    Returns:
        生成的文本字符串，失败时返回错误信息（以 [Error] 开头）
    """
    # 参数合并
    model = model or DEFAULT_MODEL
    temperature = temperature if temperature is not None else DEFAULT_TEMPERATURE
    max_tokens = max_tokens if max_tokens is not None else DEFAULT_MAX_TOKENS
    timeout = timeout or DEFAULT_TIMEOUT
    base_url = base_url or DEFAULT_BASE_URL
    use_cache = cache if cache is not None else CACHE_ENABLED
    
    # 缓存键（包含所有影响结果的参数）
    if use_cache:
        cache_key = f"{model}|{temperature}|{max_tokens}|{prompt}|{system}"
        if cache_key in _cache:
            return _cache[cache_key]
    
    # 构造请求（兼容 Ollama API，也支持 OpenAI 格式）
    url = f"{base_url.rstrip('/')}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        }
    }
    if system:
        payload["system"] = system
    
    try:
        resp = requests.post(url, json=payload, timeout=timeout)
        resp.raise_for_status()
        result = resp.json().get("response", "").strip()
        
        if use_cache:
            _cache[cache_key] = result
        return result
    except requests.exceptions.ConnectionError:
        return "[Error] Cannot connect to model service. Is Ollama running?"
    except requests.exceptions.Timeout:
        return f"[Error] Request timeout after {timeout}s"
    except requests.exceptions.RequestException as e:
        return f"[Error] {str(e)}"
    except Exception as e:
        return f"[Error] Unexpected error: {str(e)}"


# 可选：流式生成（高级用法）
def generate_stream(
    prompt: str,
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    timeout: Optional[int] = None,
    base_url: Optional[str] = None,
):
    """
    流式生成，返回生成器，逐块产出文本
    """
    model = model or DEFAULT_MODEL
    temperature = temperature if temperature is not None else DEFAULT_TEMPERATURE
    max_tokens = max_tokens if max_tokens is not None else DEFAULT_MAX_TOKENS
    timeout = timeout or DEFAULT_TIMEOUT
    base_url = base_url or DEFAULT_BASE_URL
    
    url = f"{base_url.rstrip('/')}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        }
    }
    
    try:
        with requests.post(url, json=payload, stream=True, timeout=timeout) as resp:
            resp.raise_for_status()
            for line in resp.iter_lines():
                if line:
                    import json
                    chunk = json.loads(line)
                    if "response" in chunk:
                        yield chunk["response"]
    except Exception as e:
        yield f"[Error] {str(e)}"