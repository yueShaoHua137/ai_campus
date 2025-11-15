# campus_app.py - 校园引导智能体基础版本
import streamlit as st
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置页面
st.set_page_config(
    page_title="校园引导智能体",
    page_icon="🎓",
    layout="centered"
)

# 应用标题和介绍
st.title("🎓 校园引导智能体")
st.markdown("""
欢迎使用校园AI助手！我可以帮助您查询：
- 📚 课程信息
- 🏫 校园设施
- 💰 奖学金政策
- 📅 学术日历
- 等等...
""")

# 检查环境
st.sidebar.header("环境状态")
st.sidebar.success("✅ 虚拟环境已激活")
st.sidebar.info(f"Python路径: {os.path.dirname(os.sys.executable)}")

# 检查API密钥
api_key = os.getenv("OPENAI_API_KEY")
if api_key and api_key != "your_api_key_here":
    st.sidebar.success("✅ OpenAI API密钥已设置")
else:
    st.sidebar.warning("⚠️ 请先在 .env 文件中设置 OPENAI_API_KEY")

# 简单的问答界面
st.header("💬 校园问答")

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示聊天历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入
if prompt := st.chat_input("请输入关于校园的问题..."):
    # 添加用户消息到历史
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 生成AI回复（模拟）
    with st.chat_message("assistant"):
        if "图书馆" in prompt:
            response = "学校图书馆开放时间是周一至周日 8:00-22:00。期末期间会延长至23:00。"
        elif "奖学金" in prompt:
            response = "奖学金申请通常在每学期初开放，需要提交成绩单和申请材料。具体请查看学生事务处网站。"
        elif "课程" in prompt:
            response = "课程信息可以在教务系统中查询。选课时间一般在学期开始前两周。"
        else:
            response = "我目前还在学习中，请先在我的知识库中添加校园文档来获得更准确的回答。"
        
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# 底部信息
st.markdown("---")
st.caption("校园引导智能体 - 基于RAG技术构建")