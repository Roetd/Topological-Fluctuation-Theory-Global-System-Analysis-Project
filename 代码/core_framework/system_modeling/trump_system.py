"""
特朗普系统拓扑建模

严格对应论文3.1节 四大核心拓扑不变量
"""

import numpy as np

from .sovereign_node import SovereignNode
from core_framework.tft_core.axioms import check_topological_invariant

class TrumpSystem:
    def __init__(self, us_node: SovereignNode):
        self.us_node = us_node

        # 论文3.1节 四大核心拓扑不变量
        self.core_topology_invariants = {
            "transactional_sovereignty": {
                "description": "交易式主权拓扑：双边关系矩阵秩为1，非对角元为0",
                "adjacency_matrix": self._build_transactional_topology()
            },
            "single_center_closed": {
                "description": "单中心闭合拓扑：全球网络仅存在美国唯一不动点",
                "adjacency_matrix": self._build_single_center_topology()
            },
            "anti_establishment_boundary_breaking": {
                "description": "反建制破界拓扑：政策与规则集的豪斯多夫距离持续增大",
                "boundary_breaking_rate": 0.3
            },
            "hard_power_priority": {
                "description": "硬实力优先拓扑：硬实力投影远大于软实力",
                "hard_power_ratio": 0.9
            }
        }

        # 初始核心拓扑（用于不变量校验）
        self.initial_core_topology = self._build_single_center_topology()

        # 应用特朗普拓扑到美国节点
        self._apply_topology_to_node()

    def _build_transactional_topology(self, node_count: int = 10) -> np.ndarray:
        """构建交易式主权拓扑：一对一标量交易，多边关系为0，矩阵秩为1"""
        adj = np.zeros((node_count, node_count))
        adj[0, :] = 1  # 美国为唯一交易发起方
        adj[:, 0] = 1  # 所有节点仅与美国发生双边交易
        return adj

    def _build_single_center_topology(self, node_count: int = 10) -> np.ndarray:
        """构建单中心闭合拓扑：美国为唯一中心节点"""
        adj = np.zeros((node_count, node_count))
        adj[0, 1:] = 1  # 美国指向所有其他节点
        adj[1:, 0] = 1  # 所有其他节点仅指向美国
        return adj

    def _apply_topology_to_node(self):
        """将特朗普拓扑应用到美国节点"""
        # 硬实力优先
        self.us_node.hard_power_weight = self.core_topology_invariants["hard_power_priority"]["hard_power_ratio"]
        self.us_node.soft_power_weight = 1 - self.us_node.hard_power_weight

        # 破界行为：性能界优先级高于生存界（违反三界约束）
        self.us_node.update_metrics({
            "performance": self.us_node.metrics["performance"] * 1.5,
            "linear": self.us_node.metrics["linear"] * 0.8,
            "security": self.us_node.metrics["security"] * 0.7,
            "survival": self.us_node.metrics["survival"] * 0.6
        })

        # 行动节奏加速
        self.us_node.action_rhythm = 2.0

    def check_topology_invariance(self, current_adjacency: np.ndarray) -> tuple[bool, float]:
        """校验特朗普核心拓扑是否保持不变（论文3.1节）"""
        return check_topological_invariant(self.initial_core_topology, current_adjacency)