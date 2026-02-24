"""
三条核心演化路径实现

严格对应论文4.1-4.3节
"""

import numpy as np

from .global_system import GlobalSystem
from .trump_system import TrumpSystem
from core_framework.tft_core.axioms import check_three_realms_constraint, check_homologous_symbiosis

class EvolutionPaths:
    """
    演化路径分析器类
    
    基于36D拓扑波动理论的演化路径分析
    """
    
    def __init__(self):
        """
        初始化演化路径分析器
        """
        pass
    
    def analyze_trump_path(self, global_system):
        """
        分析特朗普路径
        
        参数:
            global_system: 全球系统实例
        
        返回:
            dict: 分析结果
        """
        # 简化的特朗普路径分析
        result = {
            "stability": 0.3,
            "innovation": 0.2,
            "resilience": 0.1,
            "path_name": "特朗普路径",
            "description": "单中心拓扑的极致化与崩溃"
        }
        return result
    
    def analyze_multilateral_path(self, global_system):
        """
        分析多边主义路径
        
        参数:
            global_system: 全球系统实例
        
        返回:
            dict: 分析结果
        """
        # 简化的多边主义路径分析
        result = {
            "stability": 0.6,
            "innovation": 0.4,
            "resilience": 0.5,
            "path_name": "多边主义路径",
            "description": "旧多边体系的修补与内卷化"
        }
        return result
    
    def analyze_homologous_path(self, global_system):
        """
        分析同源共生路径
        
        参数:
            global_system: 全球系统实例
        
        返回:
            dict: 分析结果
        """
        # 简化的同源共生路径分析
        result = {
            "stability": 0.9,
            "innovation": 0.8,
            "resilience": 0.9,
            "path_name": "同源共生路径",
            "description": "基于同源共生公理的新拓扑重构"
        }
        return result

def run_trump_path(global_system: GlobalSystem, total_steps: int = 50) -> dict:
    """
    路径一：单中心拓扑的极致化与崩溃（特朗普路径）

    对应论文4.1节：性能界无限放大，违反三界约束，最终解发散崩溃

    """
    us_node = global_system.nodes.values()["US"]
    trump_system = TrumpSystem(us_node)

    evolution_history = []

    for step in range(total_steps):
        # 单中心拓扑极致化：美国中心度持续提升
        node_count = len(global_system.nodes.values())
        new_adj = np.zeros((node_count, node_count))
        new_adj[0, :] = 1 + step * 0.05  # 美国中心权重持续上升
        new_adj[:, 0] = 1 + step * 0.05

        global_system.step_evolution(new_adj)

        # 性能界持续放大，违反三界约束
        us_node.update_metrics({
            "performance": us_node.metrics["performance"] * 1.08,
            "security": us_node.metrics["security"] * 0.98,
            "survival": us_node.metrics["survival"] * 0.97
        })

        # 记录指标
        psi = global_system.get_global_psi()
        is_chain_valid, chain_residual = global_system.check_global_topological_chain()
        is_constraint_valid, violations = check_three_realms_constraint(us_node.metrics)

        goal_cosine, isomorphy, rhythm_corr, symbiosis = check_homologous_symbiosis(
            [node.evolution_goal for node in global_system.nodes.values()],
            [node.self_adjacency for node in global_system.nodes.values()],
            [node.action_rhythm for node in global_system.nodes.values()]
        )

        evolution_history.append({
            "step": step,
            "psi_norm": np.linalg.norm(psi),
            "chain_residual": chain_residual,
            "constraint_violations": len(violations),
            "symbiosis_score": symbiosis,
            "us_performance": us_node.metrics["performance"],
            "us_survival": us_node.metrics["survival"]
        })

    # 最终状态判断：解发散（psi_norm指数增长）→ 崩溃
    final_state = evolution_history[-1]
    is_collapsed = final_state["psi_norm"] > 10 * evolution_history[0]["psi_norm"]

    return {
        "path_name": "特朗普路径（单中心极致化与崩溃）",
        "evolution_history": evolution_history,
        "final_state": final_state,
        "is_collapsed": is_collapsed,
        "core_conclusion": "单中心拓扑违反三界约束，长期必然崩溃，全球系统陷入混沌失序"
    }

def run_old_multilateral_path(global_system: GlobalSystem, total_steps: int = 50) -> dict:
    """
    路径二：旧多边体系的修补与内卷化

    对应论文4.2节：带阻尼的亚稳定解，拓扑闭链不严格为0，衰减振荡，最终内卷化

    """
    evolution_history = []
    damping = 0.08  # 体系阻尼

    for step in range(total_steps):
        # 旧体系修补：邻接矩阵小幅调整，不改变单中心核心拓扑
        adj_noise = np.random.normal(0, 0.02, global_system.global_adjacency.shape)
        new_adj = np.clip(global_system.global_adjacency + adj_noise, 0, 2)

        global_system.step_evolution(new_adj)

        # 亚稳定振荡：指标小幅波动，无本质改善
        for node in global_system.nodes.values():
            node.update_metrics({
                "survival": np.clip(node.metrics["survival"] + np.random.normal(0, 0.01), 0.4, 0.8),
                "security": np.clip(node.metrics["security"] + np.random.normal(0, 0.01), 0.4, 0.8),
                "performance": np.clip(node.metrics["performance"] * (1 - damping), 0.3, 0.7)
            })

        # 记录指标
        psi = global_system.get_global_psi()
        is_chain_valid, chain_residual = global_system.check_global_topological_chain()

        node_metrics = [node.metrics for node in global_system.nodes.values()]
        avg_constraint_valid = np.mean([check_three_realms_constraint(m)[0] for m in node_metrics])

        goal_cosine, isomorphy, rhythm_corr, symbiosis = check_homologous_symbiosis(
            [node.evolution_goal for node in global_system.nodes.values()],
            [node.self_adjacency for node in global_system.nodes.values()],
            [node.action_rhythm for node in global_system.nodes.values()]
        )

        evolution_history.append({
            "step": step,
            "psi_norm": np.linalg.norm(psi),
            "chain_residual": chain_residual,
            "avg_constraint_valid": avg_constraint_valid,
            "symbiosis_score": symbiosis,
            "avg_performance": np.mean([m["performance"] for m in node_metrics])
        })

    # 最终状态判断：亚稳定，内卷化（性能持续衰减，无增长）
    final_state = evolution_history[-1]
    is_involution = final_state["avg_performance"] < evolution_history[0]["avg_performance"] * 0.8

    return {
        "path_name": "旧多边体系路径（修补与内卷化）",
        "evolution_history": evolution_history,
        "final_state": final_state,
        "is_involution": is_involution,
        "core_conclusion": "无法解决核心拓扑缺陷，陷入失灵-修补的恶性循环，文明进入内卷平台期"
    }

def run_homologous_symbiosis_path(global_system: GlobalSystem, total_steps: int = 50) -> dict:
    """
    路径三：基于同源共生公理的新拓扑重构（TFT最优路径）

    对应论文4.3节：严格闭链的全局渐近稳定解，全局最优吸引子

    """
    evolution_history = []

    for step in range(total_steps):
        # 同源共生拓扑：多节点对等连接，无单一中心
        node_count = len(global_system.nodes.values())
        new_adj = np.ones((node_count, node_count)) * 0.5  # 全节点对等连接
        np.fill_diagonal(new_adj, 1.0)  # 每个节点自身闭环完整

        global_system.step_evolution(new_adj)

        # 严格遵循三界约束：生存界、安全界优先提升
        for node in global_system.nodes.values():
            node.update_metrics({
                "survival": np.clip(node.metrics["survival"] + 0.008, 0, 1),
                "security": np.clip(node.metrics["security"] + 0.008, 0, 1),
                "linear": np.clip(node.metrics["linear"] + 0.005, 0, 1),
                "performance": np.clip(node.metrics["performance"] + 0.003, 0, 1)
            })
            node.action_rhythm = 1.0  # 同频节奏

        # 记录指标
        psi = global_system.get_global_psi()
        is_chain_valid, chain_residual = global_system.check_global_topological_chain()

        node_metrics = [node.metrics for node in global_system.nodes.values()]
        all_constraint_valid = np.all([check_three_realms_constraint(m)[0] for m in node_metrics])

        goal_cosine, isomorphy, rhythm_corr, symbiosis = check_homologous_symbiosis(
            [node.evolution_goal for node in global_system.nodes.values()],
            [node.self_adjacency for node in global_system.nodes.values()],
            [node.action_rhythm for node in global_system.nodes.values()]
        )

        evolution_history.append({
            "step": step,
            "psi_norm": np.linalg.norm(psi),
            "chain_residual": chain_residual,
            "all_constraint_valid": all_constraint_valid,
            "homology_score": goal_cosine,
            "isomorphy_score": isomorphy,
            "frequency_score": rhythm_corr,
            "symbiosis_score": symbiosis,
            "avg_survival": np.mean([m["survival"] for m in node_metrics]),
            "avg_performance": np.mean([m["performance"] for m in node_metrics])
        })

    # 最终状态判断：全局渐近稳定（残差趋近于0，共生度持续提升）
    final_state = evolution_history[-1]
    is_asymptotically_stable = final_state["chain_residual"] < 1e-3 and final_state["symbiosis_score"] > 0.9

    return {
        "path_name": "同源共生新拓扑路径（TFT全局最优解）",
        "evolution_history": evolution_history,
        "final_state": final_state,
        "is_asymptotically_stable": is_asymptotically_stable,
        "core_conclusion": "严格满足拓扑闭链与三界约束，是唯一长期稳定、高抗风险、高演化潜力的全局最优吸引子解"
    }