"""
拓扑波动理论核心算子

基于36D拓扑波动理论的核心算子实现
"""

import numpy as np
from .constants import TOPOLOGICAL_CHAIN_TOLERANCE

def p_order_power_mean(data: np.ndarray, p: float) -> float:
    """
    p阶幂平均收敛算子 Mp(Ψ)

    基于36D拓扑波动理论的p阶幂平均算子实现

    参数:
        data: 输入数据数组
        p: 幂平均的阶数

    返回:
        float: p阶幂平均值

    特性:
        p=-1 → 调和平均
        p=0 → 几何平均
        p=1 → 算术平均
        p=2 → 平方平均
        满足单调性: M_-1 ≤ M_0 ≤ M_1 ≤ M_2
    """
    data = np.asarray(data)

    if np.any(data <= 0) and p <= 0:
        raise ValueError("p≤0时数据必须全为正数")

    if p == 0:
        return np.exp(np.mean(np.log(data)))
    elif p == -np.inf:
        return np.min(data)
    elif p == np.inf:
        return np.max(data)
    else:
        return np.mean(data ** p) ** (1 / p)

def topological_boundary_operator(psi: np.ndarray, adjacency_matrix: np.ndarray) -> np.ndarray:
    """
    拓扑边界算子 ∂Ψ

    基于36D拓扑波动理论的拓扑边界算子实现
    对应拓扑闭链公理 ∂²=0

    参数:
        psi: 拓扑波动总场 Ψ
        adjacency_matrix: 系统拓扑邻接矩阵

    返回:
        np.ndarray: 边界算子作用结果 ∂Ψ
    """
    return adjacency_matrix @ psi

def topological_chain_check(psi: np.ndarray, adjacency_matrix: np.ndarray) -> tuple[bool, float]:
    """
    拓扑闭链公理校验 ∂²Ψ = 0

    基于36D拓扑波动理论的拓扑闭链公理校验
    对应生存界核心约束：闭环无泄漏、无源无旋

    参数:
        psi: 拓扑波动总场 Ψ
        adjacency_matrix: 系统拓扑邻接矩阵

    返回:
        tuple[bool, float]: (是否满足闭链公理, 二阶边界算子的模长)
    """
    d_psi = topological_boundary_operator(psi, adjacency_matrix)
    d2_psi = topological_boundary_operator(d_psi, adjacency_matrix)
    residual = np.linalg.norm(d2_psi)
    return residual < TOPOLOGICAL_CHAIN_TOLERANCE, residual

def topological_invariant_calculator(adjacency_matrix: np.ndarray) -> dict:
    """
    拓扑不变量计算器

    基于36D拓扑波动理论的拓扑不变量计算

    参数:
        adjacency_matrix: 系统拓扑邻接矩阵

    返回:
        dict: 拓扑不变量字典
    """
    invariants = {}
    
    # 计算矩阵秩
    invariants['rank'] = np.linalg.matrix_rank(adjacency_matrix)
    
    # 计算特征值
    eigenvalues = np.linalg.eigvals(adjacency_matrix)
    invariants['eigenvalues'] = eigenvalues
    invariants['eigenvalue_count'] = len(eigenvalues)
    invariants['non_zero_eigenvalues'] = np.sum(np.abs(eigenvalues) > 1e-10)
    
    # 计算矩阵范数
    invariants['frobenius_norm'] = np.linalg.norm(adjacency_matrix, 'fro')
    invariants['spectral_norm'] = np.linalg.norm(adjacency_matrix, 2)
    
    # 计算图的基本不变量
    invariants['node_count'] = adjacency_matrix.shape[0]
    invariants['edge_count'] = np.sum(adjacency_matrix > 0) // 2  # 无向图
    
    return invariants

def homology_group_approximation(adjacency_matrix: np.ndarray) -> dict:
    """
    同调群近似计算

    基于36D拓扑波动理论的同调群近似计算

    参数:
        adjacency_matrix: 系统拓扑邻接矩阵

    返回:
        dict: 同调群近似结果
    """
    # 简化的同调群近似计算
    n = adjacency_matrix.shape[0]
    rank = np.linalg.matrix_rank(adjacency_matrix)
    
    # 近似计算贝蒂数
    betti_numbers = {
        'beta_0': 1,  # 连通分支数（假设连通）
        'beta_1': max(0, n - rank - 1),  # 环数
        'beta_2': 0  # 三维以上同调群（简化计算）
    }
    
    return {
        'betti_numbers': betti_numbers,
        'rank': rank,
        'node_count': n
    }

def data_normalization(data: np.ndarray, min_val: float = 0, max_val: float = 1) -> np.ndarray:
    """
    数据归一化

    基于36D拓扑波动理论的数据归一化方法

    参数:
        data: 输入数据
        min_val: 归一化最小值
        max_val: 归一化最大值

    返回:
        np.ndarray: 归一化后的数据
    """
    data = np.asarray(data)
    data_min = np.min(data)
    data_max = np.max(data)
    
    if data_max == data_min:
        return np.full_like(data, (min_val + max_val) / 2)
    
    return (data - data_min) / (data_max - data_min) * (max_val - min_val) + min_val

def topological_similarity(matrix1: np.ndarray, matrix2: np.ndarray) -> float:
    """
    拓扑相似度计算

    基于36D拓扑波动理论的拓扑相似度计算

    参数:
        matrix1: 第一个拓扑邻接矩阵
        matrix2: 第二个拓扑邻接矩阵

    返回:
        float: 拓扑相似度（0-1）
    """
    # 确保矩阵形状相同
    if matrix1.shape != matrix2.shape:
        raise ValueError("两个矩阵形状必须相同")
    
    # 计算矩阵差异
    diff = np.linalg.norm(matrix1 - matrix2, 'fro')
    norm1 = np.linalg.norm(matrix1, 'fro')
    norm2 = np.linalg.norm(matrix2, 'fro')
    
    # 计算相似度
    if norm1 == 0 and norm2 == 0:
        return 1.0
    
    similarity = 1 - diff / (norm1 + norm2 + 1e-10)
    return max(0, min(1, similarity))

def homologous_resonance_calculator(psi1: np.ndarray, psi2: np.ndarray, adjacency_matrix: np.ndarray) -> float:
    """
    同源共振计算器

    基于36D拓扑波动理论的同源共振计算
    对应TW022同源共振概念

    参数:
        psi1: 第一个拓扑波动场 Ψ1
        psi2: 第二个拓扑波动场 Ψ2
        adjacency_matrix: 系统拓扑邻接矩阵

    返回:
        float: 同源共振强度（0-1）
    """
    # 计算两个场的相关性
    correlation = np.corrcoef(psi1, psi2)[0, 1]

    # 计算拓扑边界算子作用结果
    d_psi1 = topological_boundary_operator(psi1, adjacency_matrix)
    d_psi2 = topological_boundary_operator(psi2, adjacency_matrix)

    # 计算边界算子作用结果的相关性
    boundary_correlation = np.corrcoef(d_psi1, d_psi2)[0, 1]

    # 综合共振强度
    resonance_strength = (correlation + boundary_correlation) / 2

    return max(0, min(1, resonance_strength))

def topological_evolution_operator(psi: np.ndarray, adjacency_matrix: np.ndarray, parameters: dict) -> np.ndarray:
    """
    拓扑演化算子

    基于36D拓扑波动理论的拓扑演化算子实现

    参数:
        psi: 拓扑波动总场 Ψ
        adjacency_matrix: 系统拓扑邻接矩阵
        parameters: 演化参数

    返回:
        np.ndarray: 演化后的拓扑波动场
    """
    damping = parameters.get('damping', 0.1)
    survival_weight = parameters.get('survival_weight', 1.0)
    security_weight = parameters.get('security_weight', 1.0)
    linear_weight = parameters.get('linear_weight', 1.0)
    performance_weight = parameters.get('performance_weight', 1.0)

    # 计算边界算子
    d_psi = topological_boundary_operator(psi, adjacency_matrix)
    d2_psi = topological_boundary_operator(d_psi, adjacency_matrix)

    # 计算演化后的场
    evolved_psi = (
        survival_weight * d2_psi +
        security_weight * d_psi +
        linear_weight * psi +
        performance_weight * np.random.normal(0, 0.1, size=psi.shape)
    )

    # 应用阻尼
    evolved_psi = (1 - damping) * psi + damping * evolved_psi

    return evolved_psi
