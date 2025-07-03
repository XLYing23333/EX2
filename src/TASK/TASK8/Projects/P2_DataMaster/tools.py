from langchain.tools import Tool
import matplotlib.pyplot as plt
import pandas as pd
import os
from typing import Any

def make_col_plot(file_path: str) -> str:
    """
    读取CSV或Excel文件，对所有数值型列进行折线图绘制，全部画在一张图中，并保存本地，返回图片路径。
    支持 .csv, .xlsx, .xls 格式。
    """
    if not os.path.exists(file_path):
        return f"文件不存在: {file_path}"

    # 读取文件
    ext = os.path.splitext(file_path)[-1].lower()
    try:
        if ext == ".csv":
            df = pd.read_csv(file_path)
        elif ext in [".xlsx", ".xls"]:
            df = pd.read_excel(file_path)
        else:
            return "只支持CSV和Excel文件"
    except Exception as e:
        return f"文件读取失败: {e}"

    # 只取数值列
    num_df = df.select_dtypes(include=["number"])
    if num_df.empty:
        return "文件中不包含数值型列，无法绘图"

    plt.figure(figsize=(10, 6))
    for col in num_df.columns:
        plt.plot(num_df.index, num_df[col], label=col)
    plt.title("Column Plot")
    plt.xlabel("Row Index")
    plt.ylabel("Value")
    plt.legend()
    plt.tight_layout()

    img_path = file_path + "_plot.png"
    plt.savefig(img_path)
    plt.show()
    plt.close()
    return f"已生成可视化图片: {img_path}"



make_col_plot_tool = Tool(
    name="make_col_plot",
    func=make_col_plot,
    description="对CSV或Excel文件所有数值型列画折线图并保存。输入参数是文件路径字符串"
)