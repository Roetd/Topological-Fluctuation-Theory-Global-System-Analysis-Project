"""
全球系统类

基于36D拓扑波动理论的全球系统实现
"""

import numpy as np
import pandas as pd
import yaml
import os
from .sovereign_node import SovereignNode
from core_framework.tft_core.operators import topological_chain_check
from core_framework.tft_core.axioms import check_system_stability

class GlobalSystem:
    """
    全球系统类

    基于36D拓扑波动理论的全球系统实现，用于管理和分析全球系统中的主权节点
    """

    def __init__(self):
        """
        初始化全球系统
        """
        self.nodes: dict[str, SovereignNode] = {}
        self.global_adjacency: np.ndarray = np.array([])
        self.time_step: int = 0
        self.config: dict = {}
        self.evolution_history = []

    def add_node(self, node: SovereignNode):
        """
        添加主权节点

        参数:
            node: 主权节点
        """
        self.nodes[node.node_id] = node
        self._update_global_adjacency()

    def load_nodes_from_csv(self, csv_path: str):
        """
        从CSV文件批量加载节点

        参数:
            csv_path: CSV文件路径
        """
        df = pd.read_csv(csv_path)
        for _, row in df.iterrows():
            node = SovereignNode(
                node_id=row["node_id"],
                node_name=row["node_name"],
                survival_metric=row["survival_metric"],
                security_metric=row["security_metric"],
                linear_metric=row["linear_metric"],
                performance_metric=row["performance_metric"],
                hard_power_weight=row["hard_power_weight"],
                soft_power_weight=row["soft_power_weight"]
            )
            self.add_node(node)

    def load_config(self, config_path: str):
        """
        从YAML文件加载配置

        参数:
            config_path: 配置文件路径

        返回:
            dict: 配置字典
        """
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        return self.config

    def _update_global_adjacency(self):
        """
        更新全球系统邻接矩阵
        """
        node_count = len(self.nodes)
        if node_count == 0:
            self.global_adjacency = np.array([])
            return

        # 初始化邻接矩阵
        self.global_adjacency = np.eye(node_count)

        # 计算节点间的连接权重
        node_list = list(self.nodes.values())
        for i in range(node_count):
            for j in range(node_count):
                if i != j:
                    # 基于节点实力计算连接权重
                    node_i = node_list[i]
                    node_j = node_list[j]
                    
                    # 计算硬实力和软实力的加权和
                    hard_power_factor = node_i.hard_power_weight * node_j.hard_power_weight
                    soft_power_factor = node_i.soft_power_weight * node_j.soft_power_weight
                    
                    # 计算连接权重
                    weight = 0.6 * hard_power_factor + 0.4 * soft_power_factor
                    
                    # 基于节点状态调整权重
                    if node_i.state == "stable" and node_j.state == "stable":
                        weight *= 1.2
                    elif node_i.state == "unstable" or node_j.state == "unstable":
                        weight *= 0.8
                    
                    self.global_adjacency[i, j] = weight

    def get_global_psi(self) -> np.ndarray:
        """
        获取全球系统的总拓扑波动场Ψ

        返回:
            np.ndarray: 全球系统的总拓扑波动场
        """
        if not self.nodes:
            return np.array([])
        return np.concatenate([node.get_psi() for node in self.nodes.values()])

    def check_global_topological_chain(self) -> tuple[bool, float]:
        """
        校验全球系统拓扑闭链公理

        返回:
            tuple[bool, float]: (是否满足闭链公理, 二阶边界算子的模长)
        """
        if not self.nodes:
            return True, 0.0
        
        psi = self.get_global_psi()
        return topological_chain_check(psi, self.global_adjacency)

    def step_evolution(self, adjacency_update: np.ndarray = None):
        """
        系统演化单步推进

        参数:
            adjacency_update: 邻接矩阵更新
        """
        self.time_step += 1

        if adjacency_update is not None:
            self.global_adjacency = adjacency_update
        else:
            self._update_global_adjacency()

        # 节点演化
        for node in self.nodes.values():
            node.evolve(self.time_step)

        # 节点间交互
        node_list = list(self.nodes.values())
        for i in range(len(node_list)):
            for j in range(i+1, len(node_list)):
                interaction_strength = self.global_adjacency[i, j]
                node_list[i].interact(node_list[j], interaction_strength)
                node_list[j].interact(node_list[i], interaction_strength)

        # 记录演化历史
        self.evolution_history.append({
            "time_step": self.time_step,
            "node_count": len(self.nodes),
            "global_psi": self.get_global_psi().tolist(),
            "adjacency_matrix": self.global_adjacency.tolist(),
            "system_metrics": self.get_system_metrics()
        })

    def get_system_metrics(self) -> dict[str, float]:
        """
        获取系统指标

        返回:
            dict[str, float]: 系统指标字典
        """
        if not self.nodes:
            return {}

        # 计算系统平均指标
        metrics = {
            "survival": 0.0,
            "security": 0.0,
            "linear": 0.0,
            "performance": 0.0
        }

        for node in self.nodes.values():
            for metric_name, value in node.metrics.items():
                metrics[metric_name] += value

        # 计算平均值
        node_count = len(self.nodes)
        for metric_name in metrics:
            metrics[metric_name] /= node_count

        return metrics

    def check_system_stability(self) -> tuple[bool, dict[str, float]]:
        """
        检查系统稳定性

        返回:
            tuple[bool, dict[str, float]]: (是否稳定, 稳定性指标)
        """
        system_metrics = self.get_system_metrics()
        return check_system_stability(system_metrics)

    def get_node_by_id(self, node_id: str) -> SovereignNode:
        """
        通过ID获取节点

        参数:
            node_id: 节点ID

        返回:
            SovereignNode: 主权节点
        """
        return self.nodes.get(node_id)

    def get_node_by_name(self, node_name: str) -> SovereignNode:
        """
        通过名称获取节点

        参数:
            node_name: 节点名称

        返回:
            SovereignNode: 主权节点
        """
        for node in self.nodes.values():
            if node.node_name == node_name:
                return node
        return None

    def remove_node(self, node_id: str):
        """
        移除节点

        参数:
            node_id: 节点ID
        """
        if node_id in self.nodes:
            del self.nodes[node_id]
            self._update_global_adjacency()

    def save_system_state(self, output_path: str):
        """
        保存系统状态

        参数:
            output_path: 输出路径
        """
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # 系统状态
        system_state = {
            "time_step": self.time_step,
            "nodes": {},
            "system_metrics": self.get_system_metrics(),
            "evolution_history_length": len(self.evolution_history)
        }

        # 保存节点状态
        for node_id, node in self.nodes.items():
            system_state["nodes"][node_id] = node.get_state()

        # 保存到文件
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(system_state, f, default_flow_style=False, allow_unicode=True)

    def load_system_state(self, input_path: str):
        """
        加载系统状态

        参数:
            input_path: 输入路径
        """
        # 从文件加载
        with open(input_path, 'r', encoding='utf-8') as f:
            system_state = yaml.safe_load(f)

        # 恢复时间步
        self.time_step = system_state.get("time_step", 0)

        # 恢复节点
        self.nodes = {}
        for node_id, node_state in system_state.get("nodes", {}).items():
            node = SovereignNode(
                node_id=node_id,
                node_name=node_state["node_name"],
                survival_metric=node_state["metrics"]["survival"],
                security_metric=node_state["metrics"]["security"],
                linear_metric=node_state["metrics"]["linear"],
                performance_metric=node_state["metrics"]["performance"],
                hard_power_weight=node_state.get("hard_power_weight", 0.5),
                soft_power_weight=node_state.get("soft_power_weight", 0.5)
            )
            node.state = node_state.get("state", "stable")
            node.action_rhythm = node_state.get("action_rhythm", 1.0)
            self.nodes[node_id] = node

        # 更新全球邻接矩阵
        self._update_global_adjacency()

    def __str__(self) -> str:
        """
        系统字符串表示

        返回:
            str: 系统字符串表示
        """
        return f"GlobalSystem(time_step={self.time_step}, node_count={len(self.nodes)})"

    def get_average_power(self) -> float:
        """
        获取系统平均实力
        
        返回:
            float: 系统平均实力
        """
        if not self.nodes:
            return 0.0
        total_power = sum(node.calculate_power() for node in self.nodes.values())
        return total_power / len(self.nodes)

    def get_average_power(self) -> float:
        """
        获取系统平均实力
        
        返回:
            float: 系统平均实力
        """
        if not self.nodes:
            return 0.0
        total_power = sum(node.calculate_power() for node in self.nodes.values())
        return total_power / len(self.nodes)

    def get_average_power(self) -> float:
        """
        获取系统平均实力
        
        返回:
            float: 系统平均实力
        """
        if not self.nodes:
            return 0.0
        total_power = sum(node.calculate_power() for node in self.nodes.values())
        return total_power / len(self.nodes)

    def get_average_power(self) -> float:
        """
        获取系统平均实力
        
        返回:
            float: 系统平均实力
        """
        if not self.nodes:
            return 0.0
        total_power = sum(node.calculate_power() for node in self.nodes.values())
        return total_power / len(self.nodes)

    def get_average_power(self) -> float:
        """
        获取系统平均实力
        
        返回:
            float: 系统平均实力
        """
        if not self.nodes:
            return 0.0
        total_power = sum(node.calculate_power() for node in self.nodes.values())
        return total_power / len(self.nodes)

    def get_average_power(self) -> float:
        """
        获取系统平均实力
        
        返回:
            float: 系统平均实力
        """
        if not self.nodes:
            return 0.0
        total_power = sum(node.calculate_power() for node in self.nodes.values())
        return total_power / len(self.nodes)

    def get_average_power(self) -> float:
        """
        获取系统平均实力
        
        返回:
            float: 系统平均实力
        """
        if not self.nodes:
            return 0.0
        total_power = sum(node.calculate_power() for node in self.nodes.values())
        return total_power / len(self.nodes)

    def __repr__(self) -> str:
        """
        系统表示

        返回:
            str: 系统表示
        """
        return self.__str__()
