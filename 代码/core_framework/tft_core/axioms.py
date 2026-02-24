"""
拓扑波动理论核心公理

基于36D拓扑波动理论的核心公理实现
"""

import numpy as np
from .constants import CONSTRAINT_PRIORITY

def check_topological_invariant(
    initial_topology: np.ndarray,
    current_topology: np.ndarray,
    tolerance: float = 1e-3
) -> tuple[bool, float]:
    """
    拓扑不变量公理校验

    基于36D拓扑波动理论的拓扑不变量公理校验
    核心：系统核心拓扑（邻接矩阵秩、贝蒂数）不随连续形变改变

    参数:
        initial_topology: 初始拓扑邻接矩阵
        current_topology: 当前拓扑邻接矩阵
        tolerance: 拓扑差异容忍度

    返回:
        tuple[bool, float]: (拓扑不变量是否保持, 拓扑差异度)
    """
    initial_rank = np.linalg.matrix_rank(initial_topology)
    current_rank = np.linalg.matrix_rank(current_topology)
    rank_diff = np.abs(initial_rank - current_rank)

    # 拓扑结构差异度（Frobenius范数归一化）
    norm_diff = np.linalg.norm(current_topology - initial_topology) / np.linalg.norm(initial_topology)
    is_invariant = (rank_diff == 0) and (norm_diff < tolerance)

    return is_invariant, norm_diff

def check_three_realms_constraint(
    realm_metrics: dict[str, float]
) -> tuple[bool, list[str]]:
    """
    三界约束公理校验

    基于36D拓扑波动理论的三界约束公理校验
    核心：优先级必须严格满足 生存界>安全界>线性界>性能界

    参数:
        realm_metrics: 三界指标字典，格式 {"survival": 稳定度, "security": 稳定度, "linear": 稳定度, "performance": 稳定度}

    返回:
        tuple[bool, list[str]]: (是否满足约束, 违规项列表)
    """
    priority_order = ["survival", "security", "linear", "performance"]
    violations = []

    for i in range(len(priority_order)-1):
        higher_realm = priority_order[i]
        lower_realm = priority_order[i+1]
        if realm_metrics[higher_realm] < realm_metrics[lower_realm]:
            violations.append(f"优先级倒置：{higher_realm} < {lower_realm}")

    return len(violations) == 0, violations

def check_homologous_symbiosis(
    node_goals: np.ndarray,
    node_topologies: list[np.ndarray],
    node_rhythms: np.ndarray
) -> tuple[float, float, float, float]:
    """
    同源共生公理校验

    基于36D拓扑波动理论的同源共生公理校验
    核心：多节点系统需满足 同源(目标一致)、同构(拓扑兼容)、同频(节奏一致)

    参数:
        node_goals: 节点演化目标向量数组
        node_topologies: 节点拓扑邻接矩阵列表
        node_rhythms: 节点行动节奏数组

    返回:
        tuple[float, float, float, float]: (同源度, 同构度, 同频度, 综合共生度)
    """
    # 同源度：节点间演化目标的余弦相似度
    goal_cosine = np.mean([
        np.dot(node_goals[i], node_goals[j]) / (np.linalg.norm(node_goals[i]) * np.linalg.norm(node_goals[j]))
        for i in range(len(node_goals)) for j in range(i+1, len(node_goals))
    ])

    # 同构度：节点间拓扑结构的秩匹配度
    rank_list = [np.linalg.matrix_rank(top) for top in node_topologies]
    isomorphy = 1 - np.std(rank_list) / np.mean(rank_list) if np.mean(rank_list) != 0 else 0

    # 同频度：节点间行动节奏的相关性
    rhythm_corr = np.corrcoef(node_rhythms).mean()

    # 综合共生度（三者乘积，0-1）
    symbiosis_score = goal_cosine * isomorphy * rhythm_corr

    return np.clip(goal_cosine, 0, 1), np.clip(isomorphy, 0, 1), np.clip(rhythm_corr, 0, 1), np.clip(symbiosis_score, 0, 1)

def check_topological_closure(
    adjacency_matrix: np.ndarray,
    tolerance: float = 1e-6
) -> tuple[bool, float]:
    """
    拓扑闭链公理校验

    基于36D拓扑波动理论的拓扑闭链公理校验
    核心：∂²=0，闭环无泄漏、无源无旋

    参数:
        adjacency_matrix: 系统拓扑邻接矩阵
        tolerance: 闭链公理容忍度

    返回:
        tuple[bool, float]: (是否满足闭链公理, 二阶边界算子的模长)
    """
    # 计算二阶边界算子
    d2_adjacency = adjacency_matrix @ adjacency_matrix
    residual = np.linalg.norm(d2_adjacency - adjacency_matrix)
    is_closed = residual < tolerance

    return is_closed, residual

def check_system_stability(
    system_metrics: dict[str, float]
) -> tuple[bool, dict[str, float]]:
    """
    系统稳定性公理校验

    基于36D拓扑波动理论的系统稳定性公理校验

    参数:
        system_metrics: 系统指标字典

    返回:
        tuple[bool, dict[str, float]]: (是否稳定, 稳定性指标)
    """
    # 计算稳定性指标
    stability_metrics = {}
    
    # 生存界稳定性
    survival_stability = system_metrics.get("survival", 0)
    stability_metrics["survival_stability"] = survival_stability
    
    # 安全界稳定性
    security_stability = system_metrics.get("security", 0)
    stability_metrics["security_stability"] = security_stability
    
    # 线性界稳定性
    linear_stability = system_metrics.get("linear", 0)
    stability_metrics["linear_stability"] = linear_stability
    
    # 性能界稳定性
    performance_stability = system_metrics.get("performance", 0)
    stability_metrics["performance_stability"] = performance_stability
    
    # 综合稳定性
    overall_stability = (
        0.4 * survival_stability +
        0.3 * security_stability +
        0.2 * linear_stability +
        0.1 * performance_stability
    )
    stability_metrics["overall_stability"] = overall_stability
    
    # 判断系统是否稳定
    is_stable = overall_stability > 0.6
    
    return is_stable, stability_metrics

def check_evolution_path_validity(
    evolution_path: list[np.ndarray],
    adjacency_matrix: np.ndarray
) -> tuple[bool, list[str]]:
    """
    演化路径有效性校验

    基于36D拓扑波动理论的演化路径有效性校验

    参数:
        evolution_path: 演化路径数组
        adjacency_matrix: 系统拓扑邻接矩阵

    返回:
        tuple[bool, list[str]]: (路径是否有效, 无效原因列表)
    """
    invalid_reasons = []
    
    # 检查路径长度
    if len(evolution_path) < 2:
        invalid_reasons.append("演化路径长度不足")
        return False, invalid_reasons
    
    # 检查路径连续性
    for i in range(len(evolution_path)-1):
        prev_state = evolution_path[i]
        current_state = evolution_path[i+1]
        
        # 检查维度一致性
        if np.array(prev_state).shape != np.array(current_state).shape:
            invalid_reasons.append(f"路径第{i}步到第{i+1}步维度不一致")
        
        # 检查状态变化是否连续
        state_diff = np.linalg.norm(current_state - prev_state)
        if state_diff > 1.0:  # 阈值可调整
            invalid_reasons.append(f"路径第{i}步到第{i+1}步变化过大")
    
    # 检查路径终点是否稳定
    final_state = evolution_path[-1]
    from .equations import stability_equation
    is_stable, stability_index = stability_equation(final_state, adjacency_matrix)
    if not is_stable:
        invalid_reasons.append("演化路径终点不稳定")
    
    return len(invalid_reasons) == 0, invalid_reasons
