# 公开原始数据说明

本目录包含可公开获取的原始数据，用于拓扑波动理论的研究和应用。

## 目录结构

```
公开原始数据/
├── README.md              # 本说明文件
├── data_sources.md        # 数据来源说明
├── sample_global_data.csv # 示例全球数据
└── sample_api_config.yaml # 示例API配置文件
```

## 数据类型

### 1. 全球系统数据
- **sample_global_data.csv**：包含全球主要国家和地区的基本指标数据，包括生存界、安全界、线性界和性能界的稳定度，以及硬实力和软实力权重。

### 2. API数据
- **sample_api_config.yaml**：示例API配置文件，用于从公开API获取实时数据。

### 3. 其他公开数据
- 可以根据研究需要添加其他公开数据集，如经济指标、社会发展指数、环境数据等。

## 使用方法

### 1. 直接使用CSV数据
```python
from core_framework.system_modeling.global_system import GlobalSystem

# 初始化全球系统
global_system = GlobalSystem()

# 加载CSV数据
global_system.load_nodes_from_csv('原始资料/公开原始数据/sample_global_data.csv')

# 查看加载的节点
print(f"加载了 {len(global_system.nodes)} 个节点")
for node_id, node in global_system.nodes.items():
    print(f"节点 {node_id}: {node.node_name}")
```

### 2. 使用API获取数据
```python
import yaml
import requests

# 加载API配置
with open('原始资料/公开原始数据/sample_api_config.yaml', 'r') as f:
    api_config = yaml.safe_load(f)

# 从API获取数据
def get_api_data(endpoint, params):
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# 示例：获取全球GDP数据
gdp_data = get_api_data(
    api_config['endpoints']['gdp'],
    {'year': 2023}
)
print(gdp_data)
```

## 数据来源

详细的数据来源说明请参考 `data_sources.md` 文件。

## 数据更新

- 定期更新CSV数据，确保数据的时效性。
- 根据研究需要添加新的数据集和API配置。

## 注意事项

- 公开数据可能存在一定的误差和局限性，使用时请谨慎。
- 从API获取的数据可能需要进行预处理和验证。
- 请遵守数据来源的使用条款和版权要求。

## 联系信息

如果您有任何问题或建议，请联系项目维护者。
