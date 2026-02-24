"""
系统建模模块

基于36D拓扑波动理论的系统建模实现
"""

from .sovereign_node import SovereignNode
from .global_system import GlobalSystem
from .evolution_paths import run_trump_path, run_old_multilateral_path, run_homologous_symbiosis_path
from .trump_system import TrumpSystem

__all__ = [
    'SovereignNode',
    'GlobalSystem',
    'run_trump_path',
    'run_old_multilateral_path',
    'run_homologous_symbiosis_path',
    'TrumpSystem'
]

__version__ = '1.0'
__description__ = '系统建模模块'
__author__ = '拓扑波动思维链系统'
