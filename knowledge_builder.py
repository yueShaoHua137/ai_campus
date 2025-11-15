"""
knowledge_builder.py

构建本地知识库脚本：
- 读取 ./knowledge_source 目录下的所有 .txt 文件
- 使用 RecursiveCharacterTextSplitter 分割（chunk_size=500, chunk_overlap=50）
- 使用 OpenAI 的 embedding 模型（text-embedding-3-small）将文本块编码
- 将向量和文本持久化到 ChromaDB（目录 ./chroma_db）

注意：请事先设置环境变量 OPENAI_API_KEY（在 Windows PowerShell 中：$Env:OPENAI_API_KEY="your_key"）
"""
import os
import glob
from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.vectorstores import Chroma


def build_knowledge_base(
    source_dir: str = "./knowledge_source",
    persist_dir: str = "./chroma_db",
    embedding_model: str = "text-embedding-3-small",
    collection_name: str = "campus",
    chunk_size: int = 500,
    chunk_overlap: int = 50,
):
    """构建知识库并持久化到 ChromaDB。包含重复构建检查。

    如果 persist_dir 存在且非空，则默认跳过构建以避免重复。
    """

    # 检查 OPENAI_API_KEY
    if not os.environ.get("OPENAI_API_KEY"):
        raise EnvironmentError(
            "请先设置环境变量 OPENAI_API_KEY，例如：在 PowerShell 中运行：$Env:OPENAI_API_KEY=\"your_key\""
        )

    # 简单的去重 / 跳过逻辑：如果持久化目录存在且非空，则认为已经构建过
    if os.path.exists(persist_dir) and any(os.scandir(persist_dir)):
        print(f"检测到持久化目录 {persist_dir} 非空，已跳过构建（避免重复）。若要强制重建请删除该目录。")
        return

    # 收集文本文件
    pattern = os.path.join(source_dir, "**", "*.txt")
    files = glob.glob(pattern, recursive=True)
    if not files:
        raise FileNotFoundError(f"在 {source_dir} 中未找到任何 .txt 文件，请确保存在知识源。")

    print(f"找到 {len(files)} 个文本文件，开始构建知识片段...")

    # 读取并切分
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    documents: List[Document] = []
    for fp in files:
        with open(fp, "r", encoding="utf-8") as f:
            text = f.read()
        # 跳过空文件
        if not text.strip():
            continue

        splits = splitter.split_text(text)
        for i, chunk in enumerate(splits):
            metadata = {"source": os.path.relpath(fp, start=source_dir), "chunk": i}
            documents.append(Document(page_content=chunk, metadata=metadata))

    print(f"切分得到 {len(documents)} 个段落，开始生成向量并写入 ChromaDB...")

    # 嵌入器
    embeddings = OpenAIEmbeddings(model=embedding_model)

    # 将 documents 写入 ChromaDB（持久化）
    chroma = Chroma.from_documents(
        documents,
        embeddings,
        persist_directory=persist_dir,
        collection_name=collection_name,
    )
    # 持久化到磁盘
    chroma.persist()

    print("知识库构建完成并持久化到:", persist_dir)


if __name__ == "__main__":
    # 直接运行脚本时构建知识库
    build_knowledge_base()
"""
knowledge_builder.py

构建本地知识库脚本：
- 读取 ./knowledge_source 目录下的所有 .txt 文件
- 使用 RecursiveCharacterTextSplitter 分割（chunk_size=500, chunk_overlap=50）
- 使用 OpenAI 的 embedding 模型（text-embedding-3-small）将文本块编码
- 将向量和文本持久化到 ChromaDB（目录 ./chroma_db）

注意：请事先设置环境变量 OPENAI_API_KEY（在 Windows PowerShell 中：$Env:OPENAI_API_KEY="your_key"）
"""
import os
import glob
from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.vectorstores import Chroma


def build_knowledge_base(
    source_dir: str = "./knowledge_source",
    persist_dir: str = "./chroma_db",
    embedding_model: str = "text-embedding-3-small",
    collection_name: str = "campus",
    chunk_size: int = 500,
    chunk_overlap: int = 50,
):
    """构建知识库并持久化到 ChromaDB。包含重复构建检查。

    如果 persist_dir 存在且非空，则默认跳过构建以避免重复。
    """

    # 检查 OPENAI_API_KEY
    if not os.environ.get("OPENAI_API_KEY"):
        raise EnvironmentError(
            "请先设置环境变量 OPENAI_API_KEY，例如：在 PowerShell 中运行：$Env:OPENAI_API_KEY=\"your_key\""
        )

    # 简单的去重 / 跳过逻辑：如果持久化目录存在且非空，则认为已经构建过
    if os.path.exists(persist_dir) and any(os.scandir(persist_dir)):
        print(f"检测到持久化目录 {persist_dir} 非空，已跳过构建（避免重复）。若要强制重建请删除该目录。")
        return

    # 收集文本文件
    pattern = os.path.join(source_dir, "**", "*.txt")
    files = glob.glob(pattern, recursive=True)
    if not files:
        raise FileNotFoundError(f"在 {source_dir} 中未找到任何 .txt 文件，请确保存在知识源。")

    print(f"找到 {len(files)} 个文本文件，开始构建知识片段...")

    # 读取并切分
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    documents: List[Document] = []
    for fp in files:
        with open(fp, "r", encoding="utf-8") as f:
            text = f.read()
        # 跳过空文件
        if not text.strip():
            continue

        splits = splitter.split_text(text)
        for i, chunk in enumerate(splits):
            metadata = {"source": os.path.relpath(fp, start=source_dir), "chunk": i}
            documents.append(Document(page_content=chunk, metadata=metadata))

    print(f"切分得到 {len(documents)} 个段落，开始生成向量并写入 ChromaDB...")

    # 嵌入器
    embeddings = OpenAIEmbeddings(model=embedding_model)

    # 将 documents 写入 ChromaDB（持久化）
    chroma = Chroma.from_documents(
        documents,
        embeddings,
        persist_directory=persist_dir,
        collection_name=collection_name,
    )
    # 持久化到磁盘
    chroma.persist()

    print("知识库构建完成并持久化到:", persist_dir)


if __name__ == "__main__":
    # 直接运行脚本时构建知识库
    build_knowledge_base()
