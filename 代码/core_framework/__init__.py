"""
拓扑波动理论核心框架

基于36D拓扑波动理论的全球系统分析框架
"""

__version__ = '1.1'
__description__ = '拓扑波动理论核心框架'
__author__ = '拓扑波动思维链系统'

from . import tft_core
from . import system_modeling
from . import diagnosis
from . import visualization
from . import dimensions
from . import applications
from . import utils

__all__ = [
    'tft_core',
    'system_modeling',
    'diagnosis',
    'visualization',
    'dimensions',
    'applications',
    'utils'
]
