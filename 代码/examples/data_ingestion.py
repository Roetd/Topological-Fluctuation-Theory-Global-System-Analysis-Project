"""
统一原始数据引入脚本

基于36D拓扑波动理论的数据引入和处理
"""

import os
import sys
import json
import yaml
import pandas as pd
import numpy as np

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core_framework.tft_core import (
    data_normalization, topological_similarity,
    homology_group_approximation, topological_invariant_calculator,
    CORE_CONCEPTS, DIMENSION_CATEGORIES
)
from core_framework.system_modeling.global_system import GlobalSystem
from core_framework.system_modeling.sovereign_node import SovereignNode

class DataIngestion:
    """
    数据引入类
    
    基于36D拓扑波动理论的数据引入和处理
    """
    
    def __init__(self, config=None):
        """
        初始化数据引入器
        
        参数:
            config: 配置字典
        """
        self.config = config or {
            "data_dir": "../data/input",
            "output_dir": "../data/processed",
            "normalization_range": [0, 1],
            "missing_value_strategy": "mean"
        }
        self.global_system = GlobalSystem()
        self.processed_data = {}
    
    def load_structured_index(self, index_path):
        """
        加载结构化索引
        
        参数:
            index_path: 结构化索引文件路径
        
        返回:
            dict: 加载的结构化索引
        """
        with open(index_path, 'r', encoding='utf-8') as f:
            if index_path.endswith('.md'):
                # 简单解析markdown文件
                content = f.read()
                # 这里可以添加更复杂的markdown解析逻辑
                return {"content": content}
            elif index_path.endswith('.json'):
                return json.load(f)
            elif index_path.endswith('.yaml') or index_path.endswith('.yml'):
                return yaml.safe_load(f)
            else:
                raise ValueError(f"不支持的文件格式: {index_path}")
    
    def process_csv_data(self, csv_path):
        """
        处理CSV数据
        
        参数:
            csv_path: CSV文件路径
        
        返回:
            pd.DataFrame: 处理后的数据
        """
        # 读取CSV文件
        df = pd.read_csv(csv_path)
        
        # 处理缺失值
        if self.config["missing_value_strategy"] == "mean":
            df = df.fillna(df.mean())
        elif self.config["missing_value_strategy"] == "median":
            df = df.fillna(df.median())
        elif self.config["missing_value_strategy"] == "zero":
            df = df.fillna(0)
        
        # 归一化数值列
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            df[col] = data_normalization(
                df[col].values,
                self.config["normalization_range"][0],
                self.config["normalization_range"][1]
            )
        
        return df
    
    def create_nodes_from_data(self, df):
        """
        从数据创建节点
        
        参数:
            df: 处理后的数据
        """
        for _, row in df.iterrows():
            # 确保必要的列存在
            node_id = row.get("node_id", f"node_{len(self.global_system.nodes.values())}")
            node_name = row.get("node_name", f"Node {len(self.global_system.nodes.values())}")
            
            # 获取节点指标
            survival_metric = row.get("survival_metric", 0.5)
            security_metric = row.get("security_metric", 0.5)
            linear_metric = row.get("linear_metric", 0.5)
            performance_metric = row.get("performance_metric", 0.5)
            
            # 获取权重
            hard_power_weight = row.get("hard_power_weight", 0.5)
            soft_power_weight = row.get("soft_power_weight", 0.5)
            
            # 创建节点
            node = SovereignNode(
                node_id=node_id,
                node_name=node_name,
                survival_metric=survival_metric,
                security_metric=security_metric,
                linear_metric=linear_metric,
                performance_metric=performance_metric,
                hard_power_weight=hard_power_weight,
                soft_power_weight=soft_power_weight
            )
            
            # 添加节点到全球系统
            self.global_system.add_node(node)
    
    def compute_topological_properties(self):
        """
        计算拓扑属性
        
        返回:
            dict: 拓扑属性
        """
        if not self.global_system.nodes.values():
            return {}
        
        # 获取全球邻接矩阵
        adjacency_matrix = self.global_system.global_adjacency
        
        # 计算拓扑不变量
        invariants = topological_invariant_calculator(adjacency_matrix)
        
        # 计算同调群近似
        homology = homology_group_approximation(adjacency_matrix)
        
        # 计算系统指标
        system_metrics = self.global_system.get_system_metrics()
        
        # 检查系统稳定性
        is_stable, stability_metrics = self.global_system.check_system_stability()
        
        return {
            "topological_invariants": invariants,
            "homology": homology,
            "system_metrics": system_metrics,
            "stability": {
                "is_stable": is_stable,
                "metrics": stability_metrics
            }
        }
    
    def save_processed_data(self):
        """
        保存处理后的数据
        """
        # 确保输出目录存在
        os.makedirs(self.config["output_dir"], exist_ok=True)
        
        # 保存拓扑属性
        topology_path = os.path.join(self.config["output_dir"], "topological_properties.json")
        with open(topology_path, 'w', encoding='utf-8') as f:
            json.dump(self.processed_data.get("topological_properties", {}), f, ensure_ascii=False, indent=2)
        
        # 保存系统状态
        system_state_path = os.path.join(self.config["output_dir"], "system_state.yaml")
        self.global_system.save_system_state(system_state_path)
        
        # 保存节点数据
        nodes_data = []
        for node_id, node in self.global_system.nodes.values().items():
            nodes_data.append({
                "node_id": node_id,
                "node_name": node.node_name,
                "metrics": node.metrics,
                "state": node.state,
                "action_rhythm": node.action_rhythm
            })
        
        nodes_path = os.path.join(self.config["output_dir"], "nodes.json")
        with open(nodes_path, 'w', encoding='utf-8') as f:
            json.dump(nodes_data, f, ensure_ascii=False, indent=2)
    
    def run_ingestion_pipeline(self, data_paths):
        """
        运行数据引入 pipeline
        
        参数:
            data_paths: 数据文件路径列表
        """
        for data_path in data_paths:
            if not os.path.exists(data_path):
                print(f"文件不存在: {data_path}")
                continue
            
            print(f"处理文件: {data_path}")
            
            if data_path.endswith('.csv'):
                # 处理CSV数据
                df = self.process_csv_data(data_path)
                self.create_nodes_from_data(df)
                self.processed_data["csv_data"] = df.to_dict(orient="records")
            elif data_path.endswith('.md') or data_path.endswith('.json') or data_path.endswith('.yaml') or data_path.endswith('.yml'):
                # 处理结构化索引
                index_data = self.load_structured_index(data_path)
                self.processed_data["structured_index"] = index_data
        
        # 计算拓扑属性
        topological_properties = self.compute_topological_properties()
        self.processed_data["topological_properties"] = topological_properties
        
        # 保存处理后的数据
        self.save_processed_data()
        
        print("数据引入完成!")
        return self.processed_data

def main():
    """
    主函数
    """
    # 创建数据引入器
    ingestion = DataIngestion()
    
    # 定义数据路径
    data_paths = [
        "../data/input/default_nodes.csv",
        "../../原始资料/结构化索引/36D拓扑波动理论结构化索引.md"
    ]
    
    # 运行数据引入 pipeline
    result = ingestion.run_ingestion_pipeline(data_paths)
    
    # 打印结果摘要
    print("\n数据引入结果摘要:")
    print(f"处理的节点数: {len(ingestion.global_system.nodes.values())}")
    print(f"系统稳定性: {result['topological_properties']['stability']['is_stable']}")
    print(f"拓扑不变量: {result['topological_properties']['topological_invariants']['rank']}")

if __name__ == "__main__":
    main()
