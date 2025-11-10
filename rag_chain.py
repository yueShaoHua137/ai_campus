"""
rag_chain.py

封装 RAG 流程：
- 从持久化的 ChromaDB 加载向量库
- 检索最相关的 3 个文本块
- 将检索到的上下文填入提示模板并调用 gpt-3.5-turbo 生成答案

注意：请事先设置环境变量 OPENAI_API_KEY
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
        # 检查 API Key
        if not os.environ.get("OPENAI_API_KEY"):
            raise EnvironmentError(
                "请先设置环境变量 OPENAI_API_KEY，例如：在 PowerShell 中运行：$Env:OPENAI_API_KEY=\"your_key\""
            )

        # 嵌入器和向量数据库
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.db = Chroma(persist_directory=persist_dir, embedding_function=self.embeddings, collection_name=collection_name)

        # 检索器：返回最相关的 k=3
        self.retriever = self.db.as_retriever(search_kwargs={"k": 3})

        # LLM
        self.llm = ChatOpenAI(model_name=llm_model, temperature=0)

        # Prompt 模板（严格根据上下文回答），使用三引号避免转义繁琐
        template = '''你是一个专业的校园信息助手。请严格根据以下提供的上下文信息来回答问题。如果上下文信息中没有答案，请直接说“根据现有信息，我无法回答这个问题”，不要编造答案。

上下文：
{context}

问题：
{question}

请用中文回答：'''

        self.prompt = PromptTemplate(input_variables=["context", "question"], template=template)
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def ask(self, question: str) -> Dict[str, Any]:
        """对外接口：给定问题，返回答案和引用的源文档列表。"""
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
"""
rag_chain.py

封装 RAG 流程：
- 从持久化的 ChromaDB 加载向量库
- 检索最相关的 3 个文本块
- 将检索到的上下文填入提示模板并调用 gpt-3.5-turbo 生成答案

注意：请事先设置环境变量 OPENAI_API_KEY
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
        # 检查 API Key
        if not os.environ.get("OPENAI_API_KEY"):
            raise EnvironmentError(
                "请先设置环境变量 OPENAI_API_KEY，例如：在 PowerShell 中运行：$Env:OPENAI_API_KEY=\"your_key\""
            )

        # 嵌入器和向量数据库
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.db = Chroma(persist_directory=persist_dir, embedding_function=self.embeddings, collection_name=collection_name)

        # 检索器：返回最相关的 k=3
        self.retriever = self.db.as_retriever(search_kwargs={"k": 3})

        # LLM
        self.llm = ChatOpenAI(model_name=llm_model, temperature=0)

        # Prompt 模板（严格根据上下文回答），使用三引号避免转义繁琐
        template = (
            "你是一个专业的校园信息助手。请严格根据以下提供的上下文信息来回答问题。如果上下文信息中没有答案，请直接说\"根据现有信息，我无法回答这个问题\"，不要编造答案。\n\n"
            "上下文：\n{context}\n\n问题：\n{question}\n\n请用中文回答："
        )

        self.prompt = PromptTemplate(input_variables=["context", "question"], template=template)
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def ask(self, question: str) -> Dict[str, Any]:
        """对外接口：给定问题，返回答案和引用的源文档列表。"""
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
"""
rag_chain.py

封装 RAG 流程：
- 从持久化的 ChromaDB 加载向量库
- 检索最相关的 3 个文本块
- 将检索到的上下文填入提示模板并调用 gpt-3.5-turbo 生成答案

注意：请事先设置环境变量 OPENAI_API_KEY
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
        # 检查 API Key
        if not os.environ.get("OPENAI_API_KEY"):
            raise EnvironmentError(
                "请先设置环境变量 OPENAI_API_KEY，例如：在 PowerShell 中运行：$Env:OPENAI_API_KEY=\"your_key\""
            )

        # 嵌入器和向量数据库
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        # 从持久化目录加载 Chroma（embedding_function 或 embeddings 参数取决于 langchain/chromadb 版本）
        self.db = Chroma(persist_directory=persist_dir, embedding_function=self.embeddings, collection_name=collection_name)

        # 检索器：返回最相关的 k=3
        self.retriever = self.db.as_retriever(search_kwargs={"k": 3})

        # LLM
        self.llm = ChatOpenAI(model_name=llm_model, temperature=0)

        # Prompt 模板（严格根据上下文回答）
        template = (
            "你是一个专业的校园信息助手。请严格根据以下提供的上下文信息来回答问题。如果上下文信息中没有答案，请直接说\\\"根据现有信息，我无法回答这个问题\\\"，不要编造答案。\n\n"
            "上下文：\n{context}\n\n问题：\n{question}\n\n请用中文回答："
        )
        self.prompt = PromptTemplate(input_variables=["context", "question"], template=template)

        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def ask(self, question: str) -> Dict[str, Any]:
        """对外接口：给定问题，返回答案和引用的源文档列表。

        返回结构：{"answer": str, "source_documents": [ {"source": str, "content": str}, ... ]}
        """
        # 先检索相关文档
        docs = self.retriever.get_relevant_documents(question)

        if not docs:
            return {"answer": "根据现有信息，我无法回答这个问题", "source_documents": []}

        # 构建 context：包含来源文件名与片段内容，便于模型直接引用
        parts = []
        for d in docs:
            src = d.metadata.get("source") if isinstance(d.metadata, dict) else None
            parts.append(f"来源: {src}\n{d.page_content}")
        context = "\n\n---\n\n".join(parts)

        # 调用 LLMChain 生成答案
        answer = self.chain.run({"context": context, "question": question})

        # 构造源文档输出（只返回必要字段）
        source_documents = []
        for d in docs:
            source_documents.append({
                "source": d.metadata.get("source") if isinstance(d.metadata, dict) else None,
                "content": d.page_content,
            })

        return {"answer": answer, "source_documents": source_documents}


# 便捷工厂函数（可直接导入使用）
def get_rag_chain(persist_dir: str = "./chroma_db") -> RAGChain:
    return RAGChain(persist_dir=persist_dir)
"""
rag_chain.py

封装 RAG 流程：
- 从持久化的 ChromaDB 加载向量库
- 检索最相关的 3 个文本块
- 将检索到的上下文填入提示模板并调用 gpt-3.5-turbo 生成答案

注意：请事先设置环境变量 OPENAI_API_KEY
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
        # 检查 API Key
        if not os.environ.get("OPENAI_API_KEY"):
            raise EnvironmentError(
                "请先设置环境变量 OPENAI_API_KEY，例如：在 PowerShell 中运行：$Env:OPENAI_API_KEY=\"your_key\""
            )

        # 嵌入器和向量数据库
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        # 从持久化目录加载 Chroma（embedding_function 或 embeddings 参数取决于 langchain/chromadb 版本）
        self.db = Chroma(persist_directory=persist_dir, embedding_function=self.embeddings, collection_name=collection_name)

        # 检索器：返回最相关的 k=3
        self.retriever = self.db.as_retriever(search_kwargs={"k": 3})

        # LLM
        self.llm = ChatOpenAI(model_name=llm_model, temperature=0)

        # Prompt 模板（严格根据上下文回答）
        template = (
            "你是一个专业的校园信息助手。请严格根据以下提供的上下文信息来回答问题。如果上下文信息中没有答案，请直接说\\"根据现有信息，我无法回答这个问题\\"，不要编造答案。\n\n"
            "上下文：\n{context}\n\n问题：\n{question}\n\n请用中文回答："
        )
        self.prompt = PromptTemplate(input_variables=["context", "question"], template=template)

        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def ask(self, question: str) -> Dict[str, Any]:
        """对外接口：给定问题，返回答案和引用的源文档列表。

        返回结构：{"answer": str, "source_documents": [ {"source": str, "content": str}, ... ]}
        """
        # 先检索相关文档
        docs = self.retriever.get_relevant_documents(question)

        if not docs:
            return {"answer": "根据现有信息，我无法回答这个问题", "source_documents": []}

        # 构建 context：包含来源文件名与片段内容，便于模型直接引用
        parts = []
        for d in docs:
            src = d.metadata.get("source") if isinstance(d.metadata, dict) else None
            parts.append(f"来源: {src}\n{d.page_content}")
        context = "\n\n---\n\n".join(parts)

        # 调用 LLMChain 生成答案
        answer = self.chain.run({"context": context, "question": question})

        # 构造源文档输出（只返回必要字段）
        source_documents = []
        for d in docs:
            source_documents.append({
                "source": d.metadata.get("source") if isinstance(d.metadata, dict) else None,
                "content": d.page_content,
            })

        return {"answer": answer, "source_documents": source_documents}


# 便捷工厂函数（可直接导入使用）
def get_rag_chain(persist_dir: str = "./chroma_db") -> RAGChain:
    return RAGChain(persist_dir=persist_dir)
"""
rag_chain.py

封装 RAG 流程：
- 从持久化的 ChromaDB 加载向量库
- 检索最相关的 3 个文本块
- 将检索到的上下文填入提示模板并调用 gpt-3.5-turbo 生成答案

注意：请事先设置环境变量 OPENAI_API_KEY
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
        # 检查 API Key
        if not os.environ.get("OPENAI_API_KEY"):
            raise EnvironmentError(
                "请先设置环境变量 OPENAI_API_KEY，例如：在 PowerShell 中运行：$Env:OPENAI_API_KEY=\"your_key\""
            )

        # 嵌入器和向量数据库
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        # 从持久化目录加载 Chroma（embedding_function 或 embeddings 参数取决于 langchain/chromadb 版本）
        self.db = Chroma(persist_directory=persist_dir, embedding_function=self.embeddings, collection_name=collection_name)

        # 检索器：返回最相关的 k=3
        self.retriever = self.db.as_retriever(search_kwargs={"k": 3})

        # LLM
        self.llm = ChatOpenAI(model_name=llm_model, temperature=0)

        # Prompt 模板（严格根据上下文回答）
        template = (
            "你是一个专业的校园信息助手。请严格根据以下提供的上下文信息来回答问题。如果上下文信息中没有答案，请直接说\\"根据现有信息，我无法回答这个问题\\"，不要编造答案。\n\n"
            "上下文：\n{context}\n\n问题：\n{question}\n\n请用中文回答："
        )
        self.prompt = PromptTemplate(input_variables=["context", "question"], template=template)

        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def ask(self, question: str) -> Dict[str, Any]:
        """对外接口：给定问题，返回答案和引用的源文档列表。

        返回结构：{"answer": str, "source_documents": [ {"source": str, "content": str}, ... ]}
        """
        # 先检索相关文档
        docs = self.retriever.get_relevant_documents(question)

        if not docs:
            return {"answer": "根据现有信息，我无法回答这个问题", "source_documents": []}

        # 构建 context：包含来源文件名与片段内容，便于模型直接引用
        parts = []
        for d in docs:
            src = d.metadata.get("source") if isinstance(d.metadata, dict) else None
            parts.append(f"来源: {src}\n{d.page_content}")
        context = "\n\n---\n\n".join(parts)

        # 调用 LLMChain 生成答案
        answer = self.chain.run({"context": context, "question": question})

        # 构造源文档输出（只返回必要字段）
        source_documents = []
        for d in docs:
            source_documents.append({
                "source": d.metadata.get("source") if isinstance(d.metadata, dict) else None,
                "content": d.page_content,
            })

        return {"answer": answer, "source_documents": source_documents}


# 便捷工厂函数（可直接导入使用）
def get_rag_chain(persist_dir: str = "./chroma_db") -> RAGChain:
    return RAGChain(persist_dir=persist_dir)
