"""
数智岐黄 - 精简知识库API
保留基本的知识库问答功能
"""

import asyncio
import json
from typing import List, Optional
from fastapi import APIRouter, Body
from sse_starlette.sse import EventSourceResponse

from configs import (
    VECTOR_SEARCH_TOP_K, 
    SCORE_THRESHOLD, 
    TEMPERATURE,
    LLM_MODELS
)
from server.utils import BaseResponse, ListResponse
from server.knowledge_base.utils import get_kb_path, list_kbs_from_folder
from server.knowledge_base.kb_service.base import get_kb_details, get_kb_file_details
from server.knowledge_base.kb_service import KBServiceFactory
from server.chat.simple_chat import call_external_llm_api
from server.db.repository.message_repository import add_message_to_db, update_message

router = APIRouter()


@router.get("/list_knowledge_bases", summary="获取知识库列表")
async def list_knowledge_bases():
    """获取所有知识库的列表"""
    return ListResponse(data=list_kbs_from_folder())


@router.get("/knowledge_base_info", summary="获取知识库详细信息")  
async def knowledge_base_info(knowledge_base_name: str):
    """获取指定知识库的详细信息"""
    kb_details = get_kb_details()
    for kb in kb_details:
        if kb["kb_name"] == knowledge_base_name:
            return BaseResponse(data=kb)
    
    return BaseResponse(code=404, msg=f"未找到知识库 {knowledge_base_name}")


@router.post("/knowledge_base_chat", summary="知识库问答")
async def knowledge_base_chat(
    query: str = Body(..., description="用户输入", examples=["什么是人参？"]),
    knowledge_base_name: str = Body(..., description="知识库名称", examples=["tcm_kb"]),
    top_k: int = Body(VECTOR_SEARCH_TOP_K, description="匹配向量数"),
    score_threshold: float = Body(SCORE_THRESHOLD, description="知识库匹配相关度阈值", ge=0, le=2),
    history: List[dict] = Body([], description="历史对话"),
    stream: bool = Body(False, description="流式输出"),
    model_name: str = Body(LLM_MODELS[0], description="LLM 模型名称"),
    temperature: float = Body(TEMPERATURE, description="LLM 采样温度", ge=0.0, le=2.0),
    max_tokens: Optional[int] = Body(None, description="限制LLM生成Token数量"),
    conversation_id: str = Body("", description="对话框ID"),
):
    """
    基于知识库的问答
    """
    
    async def knowledge_base_chat_iterator():
        # 获取知识库服务
        kb = KBServiceFactory.get_service_by_name(knowledge_base_name)
        if not kb:
            yield json.dumps({
                "text": f"错误：未找到知识库 {knowledge_base_name}",
                "message_id": "",
            }, ensure_ascii=False)
            return
        
        # 在知识库中搜索相关文档
        docs = kb.search_docs(query, top_k, score_threshold)
        
        if not docs:
            yield json.dumps({
                "text": "抱歉，在知识库中没有找到相关信息。",
                "message_id": "",
            }, ensure_ascii=False)
            return
        
        # 构建上下文
        context = "\n".join([f"参考资料{i+1}：{doc.page_content}" for i, doc in enumerate(docs)])
        
        # 构建消息列表
        messages = []
        
        # 系统提示词
        system_prompt = f"""你是数智岐黄，一个专业的中西医融合问答助手。请基于以下参考资料回答用户的问题，能够提供中医、西医及两者结合的专业医药建议。

参考资料：
{context}

请注意：
1. 请基于提供的参考资料进行回答
2. 如果参考资料中没有相关信息，请明确说明
3. 回答要专业、准确、有条理
4. 适当引用参考资料的内容
"""
        
        messages.append({"role": "system", "content": system_prompt})
        
        # 添加历史对话
        for msg in history:
            if isinstance(msg, dict) and "role" in msg and "content" in msg:
                messages.append(msg)
        
        # 添加当前用户问题
        messages.append({"role": "user", "content": query})
        
        # 保存用户消息到数据库
        message_id = ""
        if conversation_id:
            message_id = add_message_to_db(
                chat_type="knowledge_base_chat",
                query=query,
                conversation_id=conversation_id
            )
        
        # 调用外部LLM API生成回答
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
                "message_id": message_id,
                "docs": [{"page_content": doc.page_content, "metadata": doc.metadata} for doc in docs] if token == "" else None,
            }, ensure_ascii=False)
        
        # 保存助手回复到数据库
        if conversation_id and message_id:
            update_message(message_id, response_text)
    
    if stream:
        return EventSourceResponse(knowledge_base_chat_iterator(), media_type="text/plain")
    else:
        # 非流式输出
        response_text = ""
        docs_info = None
        async for chunk in knowledge_base_chat_iterator():
            data = json.loads(chunk)
            response_text += data.get("text", "")
            if data.get("docs"):
                docs_info = data["docs"]
        
        return BaseResponse(data={
            "text": response_text,
            "docs": docs_info
        })


@router.get("/list_files", summary="获取知识库文件列表")
async def list_files(knowledge_base_name: str):
    """获取指定知识库的文件列表"""
    kb_file_details = get_kb_file_details(knowledge_base_name)
    return ListResponse(data=kb_file_details)


@router.post("/search_docs", summary="搜索知识库文档")
async def search_docs(
    query: str = Body(..., description="搜索查询"),
    knowledge_base_name: str = Body(..., description="知识库名称"),
    top_k: int = Body(VECTOR_SEARCH_TOP_K, description="返回结果数量"),
    score_threshold: float = Body(SCORE_THRESHOLD, description="相似度阈值")
):
    """在知识库中搜索相关文档"""
    kb = KBServiceFactory.get_service_by_name(knowledge_base_name)
    if not kb:
        return BaseResponse(code=404, msg=f"未找到知识库 {knowledge_base_name}")
    
    docs = kb.search_docs(query, top_k, score_threshold)
    
    return BaseResponse(data=[{
        "page_content": doc.page_content,
        "metadata": doc.metadata,
        "score": getattr(doc, 'score', 0)
    } for doc in docs])
