"""
主权节点类

基于36D拓扑波动理论的主权节点实现
"""

import numpy as np
from core_framework.tft_core.constants import CONSTRAINT_PRIORITY

class SovereignNode:
    """
    主权节点类

    基于36D拓扑波动理论的主权节点实现，用于表示全球系统中的国家或地区
    """

    def __init__(
        self,
        node_id: str,
        node_name: str,
        survival_metric: float,  # 生存界稳定度 0-1
        security_metric: float,  # 安全界稳定度 0-1
        linear_metric: float,    # 线性界稳定度 0-1
        performance_metric: float, # 性能界指标 0-1
        hard_power_weight: float = 0.5,
        soft_power_weight: float = 0.5
    ):
        """
        初始化主权节点

        参数:
            node_id: 节点ID
            node_name: 节点名称
            survival_metric: 生存界稳定度
            security_metric: 安全界稳定度
            linear_metric: 线性界稳定度
            performance_metric: 性能界指标
            hard_power_weight: 硬实力权重
            soft_power_weight: 软实力权重
        """
        self.node_id = node_id
        self.node_name = node_name

        # 三界约束核心指标
        self.metrics = {
            "survival": survival_metric,
            "security": security_metric,
            "linear": linear_metric,
            "performance": performance_metric
        }

        # 实力权重
        self.hard_power_weight = hard_power_weight
        self.soft_power_weight = soft_power_weight

        # 节点拓扑邻接矩阵（自身闭环）
        self.self_adjacency = np.eye(1)

        # 演化目标向量
        self.evolution_goal = np.array([survival_metric, security_metric, linear_metric, performance_metric])

        # 行动节奏
        self.action_rhythm = 1.0

        # 节点状态
        self.state = "stable"  # stable, unstable, evolving

        # 历史演化记录
        self.evolution_history = []

    def update_metrics(self, new_metrics: dict[str, float]):
        """
        更新节点指标

        参数:
            new_metrics: 新的指标字典
        """
        self.metrics.update(new_metrics)

        # 更新演化目标向量
        self.evolution_goal = np.array([
            self.metrics["survival"],
            self.metrics["security"],
            self.metrics["linear"],
            self.metrics["performance"]
        ])

        # 记录演化历史
        self.evolution_history.append({
            "metrics": self.metrics.copy(),
            "action_rhythm": self.action_rhythm,
            "timestamp": len(self.evolution_history)
        })

    def get_psi(self) -> np.ndarray:
        """
        获取节点的拓扑波动场Ψ

        返回:
            np.ndarray: 节点的拓扑波动场
        """
        return np.array(list(self.metrics.values()))

    def check_constraints(self) -> tuple[bool, list[str]]:
        """
        检查节点是否满足三界约束

        返回:
            tuple[bool, list[str]]: (是否满足约束, 违规项列表)
        """
        from core_framework.tft_core.axioms import check_three_realms_constraint
        return check_three_realms_constraint(self.metrics)

    def calculate_power(self) -> float:
        """
        计算节点综合实力

        返回:
            float: 节点综合实力
        """
        # 硬实力计算
        hard_power = (
            0.4 * self.metrics["survival"] +
            0.4 * self.metrics["security"] +
            0.2 * self.metrics["linear"]
        )

        # 软实力计算
        soft_power = (
            0.3 * self.metrics["linear"] +
            0.7 * self.metrics["performance"]
        )

        # 综合实力
        total_power = (
            hard_power * self.hard_power_weight +
            soft_power * self.soft_power_weight
        )

        return total_power

    def evolve(self, time_step: int, evolution_rate: float = 0.01):
        """
        节点演化

        参数:
            time_step: 时间步
            evolution_rate: 演化速率
        """
        # 基于当前状态和演化目标进行演化
        new_metrics = {}
        for metric_name, current_value in self.metrics.items():
            # 向目标值演化
            target_value = current_value + evolution_rate * (1 - current_value)
            new_metrics[metric_name] = min(1.0, max(0.0, target_value))

        # 更新指标
        self.update_metrics(new_metrics)

        # 更新状态
        is_stable, _ = self.check_constraints()
        if is_stable:
            self.state = "stable"
        else:
            self.state = "unstable"

    def interact(self, other_node: 'SovereignNode', interaction_strength: float = 0.1):
        """
        与其他节点交互

        参数:
            other_node: 其他节点
            interaction_strength: 交互强度
        """
        # 计算交互影响
        self_psi = self.get_psi()
        other_psi = other_node.get_psi()

        # 计算影响矩阵
        influence = interaction_strength * np.outer(self_psi, other_psi)

        # 更新自身指标
        new_metrics = {}
        for i, (metric_name, current_value) in enumerate(self.metrics.items()):
            # 基于交互影响更新指标
            influence_factor = np.mean(influence[i, :])
            new_value = current_value + influence_factor * 0.1
            new_metrics[metric_name] = min(1.0, max(0.0, new_value))

        # 更新指标
        self.update_metrics(new_metrics)

    def get_state(self) -> dict:
        """
        获取节点状态

        返回:
            dict: 节点状态
        """
        return {
            "node_id": self.node_id,
            "node_name": self.node_name,
            "metrics": self.metrics,
            "hard_power_weight": self.hard_power_weight,
            "soft_power_weight": self.soft_power_weight,
            "action_rhythm": self.action_rhythm,
            "state": self.state,
            "evolution_goal": self.evolution_goal.tolist(),
            "total_power": self.calculate_power(),
            "evolution_history_length": len(self.evolution_history)
        }

    def __str__(self) -> str:
        """
        节点字符串表示

        返回:
            str: 节点字符串表示
        """
        return f"SovereignNode({self.node_id}: {self.node_name}, state={self.state}, survival_metric={self.calculate_power():.4f})"

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
        节点表示

        返回:
            str: 节点表示
        """
        return self.__str__()
