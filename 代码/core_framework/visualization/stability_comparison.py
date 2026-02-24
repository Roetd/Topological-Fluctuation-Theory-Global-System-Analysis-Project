"""
稳定性与最优性对比可视化

"""

import os
import matplotlib.pyplot as plt
import pandas as pd

def plot_optimality_comparison(optimality_df: pd.DataFrame, output_dir: str):
    """绘制三条路径的综合最优性对比图"""
    fig, ax = plt.subplots(figsize=(12, 7))

    x = range(len(optimality_df))
    width = 0.25

    metrics = ["长期稳定性评分", "抗风险能力评分", "文明演化潜力评分"]
    colors = ["#ff4444", "#ffbb33", "#00C851"]

    for i, metric in enumerate(metrics):
        ax.bar([xi + width*i for xi in x], optimality_df[metric], width=width, label=metric, color=colors[i])

    ax.set_title("三条演化路径综合能力对比", fontsize=16, fontweight="bold")
    ax.set_ylabel("评分（0-100）", fontsize=12)
    ax.set_xticks([xi + width for xi in x])
    ax.set_xticklabels(optimality_df["路径名称"], fontsize=10, rotation=15)
    ax.set_ylim(0, 100)
    ax.legend(fontsize=12)
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "optimality_comparison.png"), dpi=300, bbox_inches="tight")
    plt.close()