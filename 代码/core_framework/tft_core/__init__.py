"""
拓扑波动理论核心模块

基于36D拓扑波动理论实现的核心功能
"""

from .constants import (
    PI, G, UNIT, E, CONSTRAINT_PRIORITY, TOPOLOGICAL_CHAIN_TOLERANCE,
    TOPOLOGICAL_DIMENSIONS, CONCEPT_ID_PREFIX, DEFAULT_PARAMS, DATA_PROCESSING_PARAMS,
    VISUALIZATION_PARAMS, CORE_CONCEPTS, DIMENSION_CATEGORIES, EVOLUTION_PATHS
)
from .operators import (
    p_order_power_mean, topological_boundary_operator, topological_chain_check,
    topological_invariant_calculator, homology_group_approximation,
    data_normalization, topological_similarity
)
from .equations import (
    global_unified_tft_equation, topological_evolution_equation,
    stability_equation, homology_equation, resonance_equation,
    optimization_equation
)
from .axioms import (
    check_topological_invariant, check_three_realms_constraint, check_homologous_symbiosis,
    check_topological_closure, check_system_stability, check_evolution_path_validity
)

__all__ = [
    # 常量
    'PI', 'G', 'UNIT', 'E', 'CONSTRAINT_PRIORITY', 'TOPOLOGICAL_CHAIN_TOLERANCE',
    'TOPOLOGICAL_DIMENSIONS', 'CONCEPT_ID_PREFIX', 'DEFAULT_PARAMS', 'DATA_PROCESSING_PARAMS',
    'VISUALIZATION_PARAMS', 'CORE_CONCEPTS', 'DIMENSION_CATEGORIES', 'EVOLUTION_PATHS',
    # 算子
    'p_order_power_mean', 'topological_boundary_operator', 'topological_chain_check',
    'topological_invariant_calculator', 'homology_group_approximation',
    'data_normalization', 'topological_similarity',
    # 方程
    'global_unified_tft_equation', 'topological_evolution_equation',
    'stability_equation', 'homology_equation', 'resonance_equation',
    'optimization_equation',
    # 公理校验
    'check_topological_invariant', 'check_three_realms_constraint', 'check_homologous_symbiosis',
    'check_topological_closure', 'check_system_stability', 'check_evolution_path_validity'
]

__version__ = '1.1'
__description__ = '拓扑波动理论核心模块'
__author__ = '拓扑波动思维链系统'
__theory_version__ = '36D'
