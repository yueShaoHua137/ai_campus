"""
rag_chain_clean.py

修正版的 RAGChain 实现，内容与原 rag_chain.py 功能相同，但写入为独立文件以避免原文件冲突。
"""
import os
from typing import Dict, Any

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma


class RAGChain:
    def __init__(
        self,
        persist_dir: str = "./chroma_db",
        embedding_model: str = "text-embedding-3-small",
        llm_model: str = "gpt-3.5-turbo",
        collection_name: str = "campus",
    ):
        if not os.environ.get("OPENAI_API_KEY"):
            raise EnvironmentError(
                "请先设置环境变量 OPENAI_API_KEY，例如：在 PowerShell 中运行：$Env:OPENAI_API_KEY=\"your_key\""
            )

        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.db = Chroma(persist_directory=persist_dir, embedding_function=self.embeddings, collection_name=collection_name)
        self.retriever = self.db.as_retriever(search_kwargs={"k": 3})
        self.llm = ChatOpenAI(model_name=llm_model, temperature=0)

        template = '''你是一个专业的校园信息助手。请严格根据以下提供的上下文信息来回答问题。如果上下文信息中没有答案，请直接说“根据现有信息，我无法回答这个问题”，不要编造答案。

上下文：
{context}

问题：
{question}

请用中文回答：'''

        self.prompt = PromptTemplate(input_variables=["context", "question"], template=template)
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def ask(self, question: str) -> Dict[str, Any]:
        docs = self.retriever.get_relevant_documents(question)
        if not docs:
            return {"answer": "根据现有信息，我无法回答这个问题", "source_documents": []}

        parts = []
        for d in docs:
            src = d.metadata.get("source") if isinstance(d.metadata, dict) else None
            parts.append(f"来源: {src}\n{d.page_content}")
        context = "\n\n---\n\n".join(parts)

        answer = self.chain.run({"context": context, "question": question})

        source_documents = [{
            "source": d.metadata.get("source") if isinstance(d.metadata, dict) else None,
            "content": d.page_content,
        } for d in docs]

        return {"answer": answer, "source_documents": source_documents}


def get_rag_chain(persist_dir: str = "./chroma_db") -> RAGChain:
    return RAGChain(persist_dir=persist_dir)
