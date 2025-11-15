# mobile_app.py - 移动端优化版本
import streamlit as st
import time

# 移动端优化配置
st.set_page_config(
    page_title="校园引导",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"  # 移动端默认收起侧边栏
)

# 添加加载状态
with st.spinner('加载中...'):
    time.sleep(0.5)  # 模拟加载

# 简化界面
st.title("🎓 校园助手")

# 移动端友好的大按钮
st.markdown("### 📱 快速问答")

col1, col2 = st.columns(2)
with col1:
    if st.button("📚 图书馆", use_container_width=True):
        st.info("开放时间：8:00-22:00")
with col2:
    if st.button("💰 奖学金", use_container_width=True):
        st.info("申请条件：成绩85分以上")

col3, col4 = st.columns(2)
with col3:
    if st.button("🏠 宿舍", use_container_width=True):
        st.info("关门时间：23:00")
with col4:
    if st.button("🍽️ 食堂", use_container_width=True):
        st.info("开放时间：6:30-20:00")

# 简化聊天
st.markdown("### 💬 问答")
question = st.text_input("输入问题...", placeholder="如图书馆时间？")
if question:
    with st.spinner('思考中...'):
        time.sleep(0.3)
        if "图书馆" in question:
            st.success("图书馆开放时间：周一至周日 8:00-22:00")
        elif "奖学金" in question:
            st.success("奖学金申请需要成绩85分以上，每学期初申请")
        else:
            st.info("请输入关于图书馆、奖学金、宿舍或食堂的问题")