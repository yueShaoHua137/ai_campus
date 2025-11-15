# 🎓 校园引导智能体

基于 RAG 的校园信息问答系统，帮助学生快速获取校园相关信息。

## 快速开始

1. 克隆仓库
2. 创建并激活虚拟环境：
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
3. 复制 `.env.example` 为 `.env` 并填写密钥
4. 构建知识库（将 `knowledge_source/*.txt` 放好后）：
```powershell
python build_knowledge.py
```
5. 启动后端（FastAPI）：
```powershell
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
6. 启动前端（Streamlit）：
```powershell
streamlit run campus_app.py
```

## 文件说明
- `knowledge_source/`：本地存放的知识文档（.txt）
- `build_knowledge.py`：构建向量数据库脚本
- `main.py`：FastAPI 后端接口
- `web_app.py`：Streamlit 前端
# ai_campus
原创创意，使用AI辅助编程，实现校园引导智能体项目。
