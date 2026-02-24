"""
TFT-Practice-Project 核心代码模块

基于36D拓扑波动理论的AGI架构实现
"""

__version__ = "1.0.0"
__author__ = "拓扑波动AI架构团队"
__description__ = "基于36D拓扑波动理论的AGI实践项目"

from .core import *
from .utils import *
from .applications import *

__all__ = [
    "__version__",
    "__author__",
    "__description__",
    "TFTSystem",
    "SovereignNode",
    "EvolutionAnalyzer",
    "DataIngestor",
    "ModelTrainer",
    "GlobalSystemAnalyzer"
]
