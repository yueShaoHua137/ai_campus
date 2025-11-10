"""
web_app.py

Streamlit 前端聊天界面：
- 侧边栏显示标题与说明
- 主界面展示对话历史，底部输入问题
- 提交后调用后端 http://localhost:8000/ask 并展示回答与来源

运行：
    streamlit run web_app.py

注意：请先启动 FastAPI 后端（例如：uvicorn main:app --reload）并确保 OPENAI_API_KEY 已设置。
"""
import os
import requests
import streamlit as st


API_URL = os.environ.get("RAG_API_URL", "http://localhost:8000/ask")


def init_state():
    if "history" not in st.session_state:
        st.session_state.history = []  # list of (role, text, optional sources)


def post_question(question: str):
    payload = {"question": question}
    try:
        resp = requests.post(API_URL, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data
    except Exception as e:
        return {"answer": f"调用后端出错：{e}", "source_documents": []}


def render_chat():
    for entry in st.session_state.history:
        role = entry.get("role")
        text = entry.get("text")
        sources = entry.get("sources", [])
        if role == "user":
            st.chat_message("user").write(text)
        else:
            with st.chat_message("assistant"):
                st.write(text)
                if sources:
                    st.markdown("**引用来源：**")
                    for s in sources:
                        src = s.get("source")
                        snippet = s.get("content")
                        # 仅展示前200字符的片段作为引用
                        st.markdown(f"- `{src}`: {snippet[:200].replace('\n', ' ')}...")


def main():
    st.set_page_config(page_title="校园引导智能体", page_icon="🎓")
    init_state()

    # 侧边栏
    st.sidebar.title("校园引导智能体")
    st.sidebar.markdown(
        "一个基于本地知识库的问答机器人。先用 `knowledge_builder.py` 构建知识库，再启动后端（FastAPI）和前端（Streamlit）。"
    )
    st.sidebar.markdown("后端接口: ``http://localhost:8000/ask``（可通过环境变量 RAG_API_URL 覆盖）")

    st.title("🎓 校园引导智能体")

    # 展示历史
    st.subheader("对话")
    render_chat()

    # 底部输入
    question = st.chat_input("请输入你的问题，例如：如何申请奖学金？")
    if question:
        # 添加用户消息
        st.session_state.history.append({"role": "user", "text": question})
        # 调用后端
        with st.spinner("正在查询知识库并生成答案..."):
            result = post_question(question)

        answer = result.get("answer")
        sources = result.get("source_documents", [])

        st.session_state.history.append({"role": "assistant", "text": answer, "sources": sources})

        # 重新渲染（Streamlit 会自动更新页面）
        st.experimental_rerun()


if __name__ == "__main__":
    main()
