"""
main.py

FastAPI 后端，暴露 /ask POST 接口：接收 {"question": "..."}，返回 {"answer": "...", "source_documents": [...]}

使用 rag_chain.RAGChain 来处理请求。

运行示例（在项目根目录下）：
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload

注意：请先确保已经通过 knowledge_builder.py 构建好 ./chroma_db，且设置 OPENAI_API_KEY
"""
import os
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from rag_chain_clean import get_rag_chain


class AskRequest(BaseModel):
    question: str


app = FastAPI(title="校园引导智能体 API")

# 在启动时加载 RAGChain 实例（全局复用）
try:
    rag = get_rag_chain(persist_dir="./chroma_db")
except Exception as e:
    # 记录异常但允许服务启动；在调用 /ask 时会返回错误提示
    rag = None
    load_error = str(e)
else:
    load_error = None


@app.post("/ask")
async def ask(req: AskRequest) -> Dict[str, Any]:
    """接收用户问题并返回答案与引用源文档。"""
    if load_error:
        raise HTTPException(status_code=500, detail=f"RAG 加载失败：{load_error}")

    if rag is None:
        raise HTTPException(status_code=500, detail="RAG 尚未初始化")

    # 基本输入校验
    question = req.question or ""
    if not question.strip():
        raise HTTPException(status_code=400, detail="问题不能为空")

    try:
        res = rag.ask(question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"内部错误：{e}")

    # 返回 answer 与 source_documents
    return {"answer": res.get("answer"), "source_documents": res.get("source_documents", [])}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
