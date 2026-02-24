"""
演化路径时间序列图

"""

import os
import matplotlib.pyplot as plt
import pandas as pd

def plot_evolution_trend(trump_result: dict, multi_result: dict, sym_result: dict, output_dir: str):
    """绘制三条演化路径的趋势图"""
    # 提取演化历史
    trump_history = pd.DataFrame(trump_result["evolution_history"])
    multi_history = pd.DataFrame(multi_result["evolution_history"])
    sym_history = pd.DataFrame(sym_result["evolution_history"])

    # 创建子图
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))

    # 1. 拓扑闭链残差趋势
    ax1 = axes[0, 0]
    ax1.plot(trump_history["step"], trump_history["chain_residual"], label="特朗普路径", color="#ff4444")
    ax1.plot(multi_history["step"], multi_history["chain_residual"], label="旧多边路径", color="#33b5e5")
    ax1.plot(sym_history["step"], sym_history["chain_residual"], label="同源共生路径", color="#00C851")
    ax1.set_title("拓扑闭链残差趋势（越低越稳定）", fontsize=14, fontweight="bold")
    ax1.set_xlabel("演化步数", fontsize=12)
    ax1.set_ylabel("残差", fontsize=12)
    ax1.legend(fontsize=10)
    ax1.grid(alpha=0.3)

    # 2. 共生度趋势
    ax2 = axes[0, 1]
    ax2.plot(trump_history["step"], trump_history["symbiosis_score"], label="特朗普路径", color="#ff4444")
    ax2.plot(multi_history["step"], multi_history["symbiosis_score"], label="旧多边路径", color="#33b5e5")
    ax2.plot(sym_history["step"], sym_history["symbiosis_score"], label="同源共生路径", color="#00C851")
    ax2.set_title("共生度趋势（越高越健康）", fontsize=14, fontweight="bold")
    ax2.set_xlabel("演化步数", fontsize=12)
    ax2.set_ylabel("共生度", fontsize=12)
    ax2.legend(fontsize=10)
    ax2.grid(alpha=0.3)

    # 3. 性能指标趋势
    ax3 = axes[1, 0]
    ax3.plot(trump_history["step"], trump_history["us_performance"], label="特朗普路径", color="#ff4444")
    ax3.plot(multi_history["step"], multi_history["avg_performance"], label="旧多边路径", color="#33b5e5")
    ax3.plot(sym_history["step"], sym_history["avg_performance"], label="同源共生路径", color="#00C851")
    ax3.set_title("性能指标趋势", fontsize=14, fontweight="bold")
    ax3.set_xlabel("演化步数", fontsize=12)
    ax3.set_ylabel("性能指标", fontsize=12)
    ax3.legend(fontsize=10)
    ax3.grid(alpha=0.3)

    # 4. 生存指标趋势
    ax4 = axes[1, 1]
    ax4.plot(trump_history["step"], trump_history["us_survival"], label="特朗普路径", color="#ff4444")
    ax4.plot(sym_history["step"], sym_history["avg_survival"], label="同源共生路径", color="#00C851")
    ax4.set_title("生存指标趋势（特朗普路径 vs 同源共生路径）", fontsize=14, fontweight="bold")
    ax4.set_xlabel("演化步数", fontsize=12)
    ax4.set_ylabel("生存指标", fontsize=12)
    ax4.legend(fontsize=10)
    ax4.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "evolution_trend.png"), dpi=300, bbox_inches="tight")
    plt.close()