"""
数智岐黄 - 精简对话模块
使用外部VLLM API进行对话
"""

import asyncio
from typing import List, Optional, AsyncIterable
from fastapi import APIRouter, Body
from sse_starlette.sse import EventSourceResponse
import httpx
import json

from configs import LLM_MODELS, TEMPERATURE
from configs.llm_api_config import VLLM_API_CONFIG, MODEL_MAPPING
from server.utils import wrap_done, BaseResponse
from server.db.repository.message_repository import add_message_to_db

router = APIRouter()


class SimpleAsyncIteratorCallbackHandler:
    """简单的异步迭代器回调处理器"""
    
    def __init__(self):
        self.queue = asyncio.Queue()
        self.done = asyncio.Event()
    
    async def aiter(self):
        """异步迭代器"""
        while not self.done.is_set() or not self.queue.empty():
            try:
                token = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                yield token
            except asyncio.TimeoutError:
                continue
    
    def on_llm_new_token(self, token: str, **kwargs):
        """处理新token"""
        asyncio.create_task(self.queue.put(token))
    
    def on_llm_end(self, response, **kwargs):
        """LLM结束时调用"""
        self.done.set()


async def call_external_llm_api(
    messages: List[dict],
    model_name: str = LLM_MODELS[0],
    temperature: float = TEMPERATURE,
    max_tokens: Optional[int] = None,
    stream: bool = True
) -> AsyncIterable[str]:
    """
    调用外部VLLM API
    """
    # 构建API URL
    api_url = VLLM_API_CONFIG["base_url"] + VLLM_API_CONFIG["chat_endpoint"]
    
    # 模型名称映射
    actual_model_name = MODEL_MAPPING.get(model_name, model_name)
    
    # 构建请求payload
    payload = {
        "model": actual_model_name,
        "messages": messages,
        "temperature": temperature,
        "stream": stream,
        **VLLM_API_CONFIG["default_params"]
    }
    
    # 覆盖默认参数
    payload["temperature"] = temperature
    payload["stream"] = stream
    if max_tokens:
        payload["max_tokens"] = max_tokens
    
    try:
        async with httpx.AsyncClient(timeout=VLLM_API_CONFIG["timeout"]) as client:
            async with client.stream(
                "POST",
                api_url,
                json=payload,
                headers=VLLM_API_CONFIG["headers"]
            ) as response:
                if response.status_code != 200:
                    yield f"Error: API调用失败，状态码: {response.status_code}"
                    return
                
                if stream:
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data = line[6:]
                            if data.strip() == "[DONE]":
                                break
                            try:
                                json_data = json.loads(data)
                                if "choices" in json_data and json_data["choices"]:
                                    delta = json_data["choices"][0].get("delta", {})
                                    if "content" in delta:
                                        yield delta["content"]
                            except json.JSONDecodeError:
                                continue
                else:
                    result = await response.json()
                    if "choices" in result and result["choices"]:
                        content = result["choices"][0]["message"]["content"]
                        yield content
    
    except Exception as e:
        yield f"Error: 调用外部API时出错: {str(e)}"


@router.post("/chat", summary="对话接口")
async def chat(
    query: str = Body(..., description="用户输入", examples=["你好"]),
    conversation_id: str = Body("", description="对话框ID"),
    history: List[dict] = Body([], description="历史对话"),
    stream: bool = Body(False, description="流式输出"),
    model_name: str = Body(LLM_MODELS[0], description="LLM 模型名称"),
    temperature: float = Body(TEMPERATURE, description="LLM 采样温度", ge=0.0, le=2.0),
    max_tokens: Optional[int] = Body(None, description="限制LLM生成Token数量"),
):
    """
    与LLM模型对话
    """
    async def chat_iterator() -> AsyncIterable[str]:
        # 构建消息列表
        messages = []
        
        # 添加系统消息
        messages.append({
            "role": "system",
            "content": "你是数智岐黄，一个专业的中西医融合问答助手。请用专业、准确的语言回答用户关于中医、西医及两者结合的医药问题。"
        })
        
        # 添加历史对话
        for msg in history:
            if isinstance(msg, dict) and "role" in msg and "content" in msg:
                messages.append(msg)
        
        # 添加当前用户输入
        messages.append({"role": "user", "content": query})
        
        # 保存用户消息到数据库
        if conversation_id:
            message_id = add_message_to_db(
                chat_type="llm_chat",
                query=query,
                conversation_id=conversation_id
            )
        
        # 调用外部LLM API
        response_text = ""
        async for token in call_external_llm_api(
            messages=messages,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        ):
            response_text += token
            yield json.dumps({
                "text": token,
                "message_id": message_id if conversation_id else "",
            }, ensure_ascii=False)
        
        # 保存助手回复到数据库
        if conversation_id and message_id:
            from server.db.repository.message_repository import update_message
            update_message(message_id, response_text)
    
    if stream:
        return EventSourceResponse(chat_iterator(), media_type="text/plain")
    else:
        # 非流式输出
        response_text = ""
        async for chunk in chat_iterator():
            data = json.loads(chunk)
            response_text += data.get("text", "")
        
        return BaseResponse(data={"text": response_text})


@router.get("/models", summary="获取可用模型列表")
async def list_models():
    """获取可用的模型列表"""
    return BaseResponse(data=LLM_MODELS)


# 为了兼容现有的前端调用
@router.post("/chat/chat", summary="对话接口(兼容)")
async def chat_chat(*args, **kwargs):
    """兼容原有的chat接口"""
    return await chat(*args, **kwargs)
