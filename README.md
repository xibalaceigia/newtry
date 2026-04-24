# 智扫通 · 智能客服（本地运行说明）

**技术栈概览**：Streamlit 界面 + 阿里云通义（DashScope）聊天与向量嵌入 + Chroma 向量库 + LangChain Agent。

**面试官 / 快速演示**：需 **Python 3.11 左右**、**联网**、以及您自备的 **`DASHSCOPE_API_KEY`**（勿写入代码、勿提交到仓库）。

---

## 一、最快跑起来（建议直接照做）

1. 解压/克隆代码，终端 **`cd` 到项目根目录**（与 `utils/`、`agent/` 同级）。

2. **建环境**（二选一，推荐 conda）  
   - **conda**：`conda create -n zst python=3.11 -y` → `conda activate zst`  
   - **无 conda**：`python -m venv .venv` → Windows：`.\.venv\Scripts\Activate.ps1` /  Mac/Linux：`source .venv/bin/activate`

3. **装依赖**：若有 `requirements.txt` 则 `pip install -r requirements.txt`；没有则向代码提供者索取清单后再装。

4. **设 Key 与路径**（**同一终端**、**在项目根**执行；PowerShell 示例）：

```powershell
$env:DASHSCOPE_API_KEY = "你的Key"
$env:PYTHONPATH = (Get-Location).Path
```

用 **VS Code / Cursor 打开项目文件夹** 时，集成终端里 `PYTHONPATH` 可能已配好（见 `.vscode/settings.json`）；**若报「找不到 agent/utils」再执行上面第二行。**

5. **启动**：

```bash
streamlit run utils/app.py
```

浏览器打开 **`http://localhost:8501`** 即可。结束：`Ctrl + C`。

**bash / zsh 简要对照**：`export DASHSCOPE_API_KEY="你的Key"`，`export PYTHONPATH="$(pwd)"`。

---

## 二、API Key 从哪来

| 变量 | 作用 |
|------|------|
| `DASHSCOPE_API_KEY` | 阿里云 [DashScope / 通义](https://help.aliyun.com/zh/model-studio/developer-reference/use-qwen-by-calling-api) 控制台申请 |

---

## 三、项目里你会看到的（扫一眼结构）

- **配置**：`config/*.yml`（如 `rag.yml` 中模型名）
- **向量数据**：`chroma_db/`（随仓库带上即可；环境差异大时可能需重建）
- **日志**：`logs/`

---

## 四、跑不通时优先看这里

| 现象 | 处理 |
|------|------|
| `No module named agent` 等 | 项目根下执行，或设好 `PYTHONPATH`（见第一节第 4 步） |
| 401 / 鉴权相关 | 检查 `DASHSCOPE_API_KEY` 与额度 |
| 依赖报错 | 对齐 **Python 3.11** 与 `requirements.txt`（若有）版本 |

若仍无法运行，请把 **Python 版本、系统、完整报错、启动命令** 发给维护者。
