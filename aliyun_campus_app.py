# aliyun_campus_app.py - 使用阿里云模型的校园引导智能体
import streamlit as st
import os
import dashscope
from dotenv import load_dotenv
import json

# 加载环境变量
load_dotenv()

# 设置页面
st.set_page_config(
    page_title="校园引导智能体 - 阿里云版",
    page_icon="🎓",
    layout="centered"
)

# 应用标题和介绍
st.title("🎓 校园引导智能体 - 阿里云版")
st.markdown("""
欢迎使用校园AI助手！基于阿里云通义千问模型，安全可靠。
我可以帮助您查询：
- 📚 课程信息
- 🏫 校园设施  
- 💰 奖学金政策
- 📅 学术日历
- 🎯 竞赛通知
- 等等...
""")

# 侧边栏 - 系统状态
st.sidebar.header("系统状态")

# 检查阿里云API密钥
aliyun_api_key = os.getenv("ALIYUN_API_KEY")
if aliyun_api_key and aliyun_api_key != "your_aliyun_api_key_here":
    st.sidebar.success("✅ 阿里云API密钥已设置")
    dashscope.api_key = aliyun_api_key
else:
    st.sidebar.error("❌ 请设置阿里云API密钥")

# 校园知识库
CAMPUS_KNOWLEDGE = {
    "library": {
        "keywords": ["图书馆", "借书", "还书", "阅览室", "自习"],
        "answer": "图书馆开放时间：周一至周日 8:00-22:00\n位置：校园东区主楼\n服务：借书、还书、电子资源、自习室"
    },
    "scholarship": {
        "keywords": ["奖学金", "助学金", "资助", "学费", "奖金"],
        "answer": "奖学金申请条件：\n- 成绩平均分85分以上\n- 无违纪记录\n- 每学期初申请\n申请地点：学生事务处"
    },
    "dormitory": {
        "keywords": ["宿舍", "寝室", "住宿", "宿管", "宿舍楼"],
        "answer": "宿舍信息：\n- 关门时间：23:00（周末24:00）\n- 报修：联系宿管阿姨\n- 水电费：每月初缴纳"
    },
    "canteen": {
        "keywords": ["食堂", "餐厅", "吃饭", "餐饮", "饭菜"],
        "answer": "食堂信息：\n- 开放时间：6:30-20:00\n- 位置：第一食堂（东区）、第二食堂（西区）\n- 支付方式：校园卡、微信、支付宝"
    },
    "course": {
        "keywords": ["课程", "选课", "上课", "教务", "专业课"],
        "answer": "课程相关：\n- 选课时间：学期开始前两周\n- 查询系统：教务在线\n- 联系方式：各学院教务办公室"
    }
}

def get_aliyun_answer(question):
    """使用阿里云通义千问模型获取答案"""
    try:
        from dashscope import Generation
        
        # 构建系统提示词
        system_prompt = """你是一个专业的校园信息助手。请根据用户的提问提供准确、有用的校园信息。
        如果问题涉及具体校园设施、政策或服务，请给出详细说明。"""
        
        # 调用阿里云模型
        response = Generation.call(
            model='qwen-turbo',  # 可以使用 qwen-plus 或 qwen-max 获得更好效果
            system=system_prompt,
            prompt=question,
            top_p=0.8,
            result_format='message'
        )
        
        if response.status_code == 200:
            return response.output.choices[0].message.content
        else:
            return f"模型调用失败: {response.message}"
            
    except Exception as e:
        return f"阿里云服务异常: {str(e)}"

def rule_based_answer(question):
    """基于规则的备用回答系统"""
    question_lower = question.lower()
    
    # 匹配关键词
    for category, info in CAMPUS_KNOWLEDGE.items():
        for keyword in info["keywords"]:
            if keyword in question_lower:
                return info["answer"]
    
    return None

# 主聊天界面
st.header("💬 校园问答")

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "你好！我是校园引导助手，基于阿里云通义千问模型，请问有什么可以帮助您的？"}
    ]

# 显示聊天历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入
if prompt := st.chat_input("请输入关于校园的问题..."):
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 生成AI回复
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                # 首先尝试规则匹配
                rule_answer = rule_based_answer(prompt)
                
                if rule_answer:
                    # 如果有规则匹配，直接使用规则答案
                    response = rule_answer
                elif aliyun_api_key and aliyun_api_key != "your_aliyun_api_key_here":
                    # 否则使用阿里云模型
                    response = get_aliyun_answer(prompt)
                else:
                    # 如果没有API密钥，使用备用回答
                    response = "我主要能回答关于图书馆、奖学金、食堂、宿舍、课程等方面的问题。请问您想了解哪方面的具体信息？"
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                error_msg = f"❌ 回答生成失败: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

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

# 模型选择
st.sidebar.markdown("### 模型设置")
model_option = st.sidebar.selectbox(
    "选择模型",
    ["qwen-turbo", "qwen-plus", "qwen-max"],
    index=0,
    help="qwen-turbo: 快速响应\nqwen-plus: 平衡性能\nqwen-max: 最佳效果"
)

# 使用说明
with st.sidebar.expander("💡 使用说明"):
    st.markdown("""
    1. 在 `.env` 文件中设置阿里云API密钥
    2. 快速问答按钮可立即获取常见问题答案
    3. 其他问题将使用阿里云AI模型回答
    4. 支持中英文问答
    """)

st.markdown("---")
st.caption("校园引导智能体 - 基于阿里云通义千问模型")