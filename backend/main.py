# 文件: backend/main.py
# 这是你的FastAPI后端服务器，它模拟了LangGraph的多智能体工作流
from fastapi import FastAPI
from pydantic import BaseModel
import time
import random
import re
import numpy as np


# --- 1. 定义数据结构 (Pydantic Models) ---
class QueryRequest(BaseModel):
    """前端发送给后端的请求体"""
    query: str


class ReportResponse(BaseModel):
    """后端返回给前端的响应体"""
    report: str
    data: dict  # 我们用一个灵活的字典来存放图表数据


# --- 2. 创建 FastAPI 应用 ---
app = FastAPI(
    title="Holistica Quant Backend",
    description="为微众银行大赛模拟的AI量化分析后端 [cite: 326, 331, 332]",
    version="1.0.0"
)


# --- 3. 模拟的报告生成函数 (来自 app.py) ---
def _generate_fake_report(stock_name: str) -> str:
    """
    辅助函数：根据《Structure调研.pdf》中的Prompt模板，生成一份假的专业报告
    [cite: 774-809]
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
    # 在真实的后端中，这里会返回一个 pandas DataFrame.to_dict('records')
    # 为了简化，我们只返回一个简单的字典
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

    # --- 模拟 LangGraph 多智能体工作流  ---

    # 1. 模拟 Plan Team
    print("[后端] Plan Team 正在制定计划...")
    time.sleep(0.5)

    # 2. 模拟 Data Team
    print("[后端] Data Team 正在抓取数据...")
    #
    # ‼️‼️‼️
    # ‼️ TODO: 这里是你的后端团队 (Maxen, Jess) 需要替换的地方
    # ‼️ 把这里的模拟代码，换成对 AkShare 或 TuShare 的真实API调用 [cite: 770-774]
    # ‼️
    time.sleep(1.5)  # 模拟网络延迟

    # 3. 模拟 Strategy Team
    print("[后端] Strategy Team 正在生成报告...")
    time.sleep(1.0)  # 模拟AI思考

    # --- 模拟结束 ---

    # 检查查询内容并生成响应
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
    return {"message": "Holistica Quant 后端服务器正在运行。请访问 /docs 查看 API 文档。"}

# --- 5. 运行服务器的命令 (在终端中运行) ---
# uvicorn main:app --reload