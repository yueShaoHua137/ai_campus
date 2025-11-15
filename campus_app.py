"""
Minimal Streamlit front-end for campus agent (main entry for Streamlit deployment).
"""
import os
import requests
import streamlit as st

API_URL = os.environ.get("RAG_API_URL", "http://127.0.0.1:8000/ask")

st.set_page_config(page_title="校园引导智能体", page_icon="🎓")
st.title("🎓 校园引导智能体")

if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.header("关于")
    st.write("基于本地知识库的校园问答示例。")

q = st.text_input("请输入问题：", "如何申请奖学金？")
if st.button("提问") and q.strip():
    st.session_state.history.append({"role": "user", "text": q})
    try:
        resp = requests.post(API_URL, json={"question": q}, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        answer = data.get("answer")
        sources = data.get("source_documents", [])
    except Exception as e:
        answer = f"后端调用出错：{e}"
        sources = []

    st.session_state.history.append({"role": "assistant", "text": answer, "sources": sources})

for msg in st.session_state.history:
    if msg["role"] == "user":
        st.markdown(f"**用户：** {msg['text']}")
    else:
        st.markdown(f"**助手：** {msg['text']}")
        if msg.get("sources"):
            st.markdown("**引用来源：**")
            for s in msg.get("sources"):
                st.markdown(f"- `{s.get('source')}`: {s.get('content')[:200].replace('\n',' ')}...")
# rule_based_app.py - 基于规则的校园引导系统
import streamlit as st
import re

# 设置页面
st.set_page_config(
    page_title="校园引导智能体",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 校园引导智能体 (规则版)")
st.markdown("基于规则引擎的校园问答系统")

# 校园知识库
CAMPUS_KNOWLEDGE = {
    "library": {
        "keywords": ["图书馆", "借书", "还书", "阅览室"],
        "answer": "图书馆开放时间：周一至周日 8:00-22:00\n位置：校园东区主楼\n服务：借书、还书、电子资源、自习"
    },
    "scholarship": {
        "keywords": ["奖学金", "助学金", "资助", "学费"],
        "answer": "奖学金申请条件：\n- 成绩平均分85分以上\n- 无违纪记录\n- 每学期初申请\n申请地点：学生事务处"
    },
    "dormitory": {
        "keywords": ["宿舍", "寝室", "住宿", "宿管"],
        "answer": "宿舍信息：\n- 关门时间：23:00（周末24:00）\n- 报修：联系宿管阿姨\n- 水电费：每月初缴纳"
    },
    "canteen": {
        "keywords": ["食堂", "餐厅", "吃饭", "餐饮"],
        "answer": "食堂信息：\n- 开放时间：6:30-20:00\n- 位置：第一食堂（东区）、第二食堂（西区）\n- 支付方式：校园卡、微信、支付宝"
    },
    "course": {
        "keywords": ["课程", "选课", "上课", "教务"],
        "answer": "课程相关：\n- 选课时间：学期开始前两周\n- 查询系统：教务在线\n- 联系方式：各学院教务办公室"
    }
}

def rule_based_answer(question):
    """基于规则的问答系统"""
    question_lower = question.lower()
    
    # 匹配关键词
    for category, info in CAMPUS_KNOWLEDGE.items():
        for keyword in info["keywords"]:
            if keyword in question_lower:
                return info["answer"]
    
    # 如果没有匹配，提供通用回答
    return f"""您好！我主要能帮助您了解以下校园信息：
    
📚 图书馆相关：开放时间、借还书规则
💰 奖学金相关：申请条件、流程
🏠 宿舍相关：住宿规定、报修
🍽️ 食堂相关：开放时间、位置
📖 课程相关：选课、教务信息

请问您想了解哪方面的具体信息？"""

# 聊天界面
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "你好！我是校园引导助手，请问有什么可以帮助您的？"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("请输入关于校园的问题..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = rule_based_answer(prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# 快速问答按钮
st.markdown("### 🎯 快速问答")
cols = st.columns(3)
with cols[0]:
    if st.button("📚 图书馆时间"):
        st.session_state.messages.append({"role": "user", "content": "图书馆开放时间"})
        st.session_state.messages.append({"role": "assistant", "content": CAMPUS_KNOWLEDGE["library"]["answer"]})
        st.rerun()
with cols[1]:
    if st.button("💰 奖学金申请"):
        st.session_state.messages.append({"role": "user", "content": "奖学金申请"})
        st.session_state.messages.append({"role": "assistant", "content": CAMPUS_KNOWLEDGE["scholarship"]["answer"]})
        st.rerun()
with cols[2]:
    if st.button("🏠 宿舍信息"):
        st.session_state.messages.append({"role": "user", "content": "宿舍信息"})
        st.session_state.messages.append({"role": "assistant", "content": CAMPUS_KNOWLEDGE["dormitory"]["answer"]})
        st.rerun()

st.markdown("---")
st.caption("校园引导智能体 - 基于规则引擎")