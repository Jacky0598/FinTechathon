# 文件: backend/main.py (已添加 CORS 修复)
from fastapi import FastAPI
from pydantic import BaseModel
import time
import random
import re
import numpy as np  # <-- 确保 numpy 已经导入

# -----------------------------------------------
# ‼️‼️ 第 1 步：导入 CORS 中间件 ‼️‼️
# -----------------------------------------------
from fastapi.middleware.cors import CORSMiddleware


# -----------------------------------------------


# --- 1. 定义数据结构 (Pydantic Models) ---
class QueryRequest(BaseModel):
    """前端发送给后端的请求体"""
    query: str


class ReportResponse(BaseModel):
    """后端返回给前端的响应体"""
    report: str
    data: dict


# --- 2. 创建 FastAPI 应用 ---
app = FastAPI(
    title="Holistica Quant Backend",
    description="为微众银行大赛模拟的AI量化分析后端",
    version="1.0.0"
)

# -----------------------------------------------
# ‼️‼️ 第 2 步：配置 CORS ‼️‼️
# -----------------------------------------------
# 允许的前端来源列表
origins = [
    "http://localhost:8501",  # 1. 你的本地前端 (开发时用)
    "http://localhost",
    "https_origin_renderer", # 这一行是 Render 平台预览时需要的
    "https://fintechathon-e5uy9jdzvqq6kosfoqxywp.streamlit.app"  # 2. ‼️ 你的公开前端网址
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许上面列表中的来源访问
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法 (GET, POST 等)
    allow_headers=["*"],  # 允许所有 HTTP 标头
)


# -----------------------------------------------


# --- 3. 模拟的报告生成函数 (来自 app.py) ---
def _generate_fake_report(stock_name: str) -> str:
    """
    辅助函数：根据《Structure调研.pdf》中的Prompt模板，生成一份假的专业报告
    """
    rsi = round(random.uniform(30, 70), 2)
    macd = round(random.uniform(-0.5, 0.5), 2)
    roe = round(random.uniform(5, 25), 2)
    pe = round(random.uniform(10, 50), 2)

    report = f"""
    ## {stock_name} 综合分析报告 (由FastAPI后端生成)

    ---

    ## 一、技术面分析
    1.  **K线技术形态**: 近90日K线图显示，{stock_name} 处于震荡上行趋势。
    2.  **技术指标信号**:
        * **RSI**: 当前RSI为 {rsi}，处于中性区间。
        * **MACD**: MACD值为 {macd}，快慢线接近金叉。

    ## 二、基本面分析
    1.  **盈利能力**: 最新财报显示，ROE (净资产收益率) 为 {roe}%。
    2.  **财务健康度**: 资产负债率为 {round(random.uniform(20, 60), 2)}%，现金流充裕。

    ## 三、综合评估
    1.  **核心结论**: 综合技术面与基本面，{stock_name} 短期看涨，长期基本面稳固。
    2.  **数据局限性**: 本报告为模拟数据，请接入真实数据源 (如 AkShare)。
    """
    return report


def _generate_fake_chart_data() -> dict:
    """辅助函数：为任意股票生成假的图表数据"""
    prices = (np.random.rand(90).cumsum() + 100).tolist()
    return {"price_history": prices}


# --- 4. API 路由 (Endpoint) ---
@app.post("/analyze", response_model=ReportResponse)
async def analyze_query(request: QueryRequest):
    """
    这是前端调用的核心API。
    它接收一个自然语言查询，然后返回一份结构化的分析报告。
    """

    query = request.query
    print(f"[后端] 收到了前端的请求: {query}")

    # --- 模拟 LangGraph 多智能体工作流 ---
    print("[后端] Plan Team 正在制定计划...")
    time.sleep(0.5)
    print("[后端] Data Team 正在抓取数据...")
    time.sleep(1.5)
    print("[后端] Strategy Team 正在生成报告...")
    time.sleep(1.0)
    # --- 模拟结束 ---

    match = re.search(r"分析一下(.*)", query)

    if match:
        stock_name = match.group(1).strip()
        report_content = _generate_fake_report(stock_name)
        chart_data = _generate_fake_chart_data()
    else:
        report_content = "后端收到了请求，但无法解析。请输入 '分析一下 [股票名称]'。"
        chart_data = {}

    print("[后端] 分析完成，正在将结果返回给前端。")

    return ReportResponse(report=report_content, data=chart_data)


@app.get("/")
def read_root():
    return {"message": "Holistica Quant 后端服务器正在运行 (已启用CORS)。请访问 /docs 查看 API 文档。"}