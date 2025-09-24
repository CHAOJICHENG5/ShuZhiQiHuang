"""
数智岐黄 - 精简API服务器
只包含对话和知识库问答功能，使用外部VLLM API
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from configs import VERSION
from configs.model_config import NLTK_DATA_PATH
from configs.server_config import OPEN_CROSS_DOMAIN
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from server.utils import BaseResponse, ListResponse, MakeFastAPIOffline
import nltk

# 设置NLTK数据路径
nltk.data.path = [NLTK_DATA_PATH] + nltk.data.path


async def document():
    """重定向到API文档"""
    return RedirectResponse(url="/docs")


def create_simple_app():
    """创建精简的FastAPI应用"""
    app = FastAPI(
        title="数智岐黄 API Server",
        version=VERSION,
        description="数智岐黄中西医融合智能问答系统API"
    )
    
    MakeFastAPIOffline(app)
    
    # 添加CORS中间件
    if OPEN_CROSS_DOMAIN:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    # 添加路由
    app.get("/", response_model=BaseResponse, summary="文档")(document)
    
    # 导入并注册路由
    mount_app_routes(app)
    
    return app


def mount_app_routes(app: FastAPI):
    """挂载应用路由"""
    from server.chat.simple_chat import router as chat_router
    from server.knowledge_base.simple_kb_api import router as kb_router
    from server.embeddings_api import embed_texts_endpoint
    
    # 对话相关路由
    app.include_router(chat_router, prefix="/chat", tags=["对话"])
    
    # 知识库相关路由  
    app.include_router(kb_router, prefix="/knowledge_base", tags=["知识库"])
    
    # 嵌入向量接口
    app.post("/other/embed_texts", tags=["其他"])(embed_texts_endpoint)


if __name__ == "__main__":
    import uvicorn
    from configs import API_SERVER
    
    app = create_simple_app()
    uvicorn.run(
        app,
        host=API_SERVER["host"],
        port=API_SERVER["port"]
    )
