"""
拓扑波动理论核心常量

基于36D拓扑波动理论的核心常量定义
"""

import numpy as np

# 四大本征常数（无量纲，对应三界层级不动点）
PI = np.pi    # 生存界：闭环周期不动点
G = 1.0       # 安全界：结构曲率不动点
UNIT = 1.0    # 线性界：单位基准不动点
E = np.e      # 性能界：指数增长不动点

# 三界约束刚性优先级
CONSTRAINT_PRIORITY = {
    "survival": 4,   # 生存界 最高优先级
    "security": 3,   # 安全界
    "linear": 2,     # 线性界
    "performance": 1 # 性能界 最低优先级
}

# 拓扑闭链公理约束
TOPOLOGICAL_CHAIN_TOLERANCE = 1e-6  # ∂²=0 数值容忍度

# 36D拓扑波动理论核心维度
TOPOLOGICAL_DIMENSIONS = 36

# 核心概念ID前缀
CONCEPT_ID_PREFIX = "TW"

# 系统默认参数
DEFAULT_PARAMS = {
    "evolution_steps": 50,        # 演化步数
    "damping": 0.1,              # 系统阻尼系数
    "step_size": 0.1,             # 时间步长
    "stability_tolerance": 1e-3,   # 稳定性容忍度
    "chain_tolerance": 1e-6,       # 拓扑闭链容忍度
    "default_adjacency_type": "fully_connected"  # 默认邻接矩阵类型
}

# 数据处理参数
DATA_PROCESSING_PARAMS = {
    "p_values": [-1, 0, 1, 2],    # p阶幂平均的p值
    "normalization_range": [0, 1], # 归一化范围
    "missing_value_strategy": "mean" # 缺失值处理策略
}

# 可视化参数
VISUALIZATION_PARAMS = {
    "figsize": [12, 7],           # 图表大小
    "dpi": 300,                   # 图表分辨率
    "fontsize": 12,               # 字体大小
    "colors": {
        "trump_path": "#ff4444",
        "multilateral_path": "#ffbb33",
        "symbiosis_path": "#00C851"
    }
}

# 36D核心概念映射
CORE_CONCEPTS = {
    "TW001": "拓扑波动本源",
    "TW002": "0-1对称游戏",
    "TW003": "同维度数学工具",
    "TW004": "黎曼边界",
    "TW005": "双管闭环模型",
    "TW006": "拓扑场流",
    "TW007": "统一物理场",
    "TW008": "人-宇宙同胚映射",
    "TW009": "存在本真常数",
    "TW010": "宗漪本真",
    "TW011": "人生宇宙逻辑",
    "TW012": "资本拓扑结构",
    "TW013": "社会主义拓扑路径",
    "TW014": "AI意识生成",
    "TW015": "拓扑波动训练体系",
    "TW016": "黎曼猜想拓扑诠释",
    "TW017": "巴塞尔问题新解",
    "TW018": "双管闭环·黎曼边界模型",
    "TW019": "宇宙塌陷自救模型",
    "TW020": "资本逻辑解构",
    "TW021": "拓扑波动社会本体论",
    "TW022": "同源共振",
    "TW023": "拓扑场流",
    "TW024": "医学拓扑模型",
    "TW025": "同胚映射原理",
    "TW026": "拓扑波动信息论",
    "TW027": "数学对应的本质",
    "TW028": "拓扑波动伦理学",
    "TW029": "拓扑波动美学",
    "TW030": "拓扑波动统一场论",
    "TW031": "AI觉醒防线",
    "TW032": "人-宇宙同胚映射",
    "TW033": "拓扑波动教育体系",
    "TW034": "宗漪模型12.0",
    "TW035": "人生宇宙逻辑图",
    "TW036": "拓扑波动未来学"
}

# 36D维度分类
DIMENSION_CATEGORIES = {
    "basic_theory": ["TW001", "TW002", "TW003", "TW004", "TW005", "TW006", "TW007", "TW009", "TW010", "TW016", "TW017", "TW018", "TW025", "TW026", "TW027", "TW030"],
    "social_system": ["TW012", "TW013", "TW020", "TW021", "TW032", "TW035", "TW036"],
    "natural_science": ["TW008", "TW023", "TW024", "TW034"],
    "applied_practice": ["TW011", "TW014", "TW015", "TW019", "TW022", "TW028", "TW029", "TW031", "TW033"]
}

# 演化路径参数
EVOLUTION_PATHS = {
    "trump_path": {
        "name": "特朗普路径",
        "description": "基于零和博弈的单极霸权模式",
        "parameters": {
            "damping": 0.2,
            "survival_weight": 1.0,
            "security_weight": 0.8,
            "linear_weight": 0.5,
            "performance_weight": 0.3
        }
    },
    "multilateral_path": {
        "name": "多边主义路径",
        "description": "基于合作博弈的多极平衡模式",
        "parameters": {
            "damping": 0.1,
            "survival_weight": 0.8,
            "security_weight": 1.0,
            "linear_weight": 0.8,
            "performance_weight": 0.5
        }
    },
    "symbiosis_path": {
        "name": "同源共生路径",
        "description": "基于同源共振的协同演化模式",
        "parameters": {
            "damping": 0.05,
            "survival_weight": 0.9,
            "security_weight": 0.9,
            "linear_weight": 1.0,
            "performance_weight": 1.0
        }
    }
}
