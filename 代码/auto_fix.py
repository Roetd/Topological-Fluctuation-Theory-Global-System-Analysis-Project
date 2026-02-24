#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动修复脚本

根据36D拓扑波动理论，自动分析和修复代码中的问题，确保代码满足三界约束和拓扑波动理论的核心思想。
"""

import os
import sys
import re
import ast
from typing import Dict, List, Tuple, Any

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# 需要修复的文件列表
FILES_TO_FIX = [
    "src/core.py",
    "src/applications.py",
    "应用场景/global_system_analysis.py",
    "core_framework/tft_core/axioms.py"
]

# 修复规则
FIX_RULES = {
    # SovereignNode构造函数参数修复
    "sovereign_node_constructor": {
        "pattern": r"SovereignNode\((.*?)\)",
        "old_params": ["name", "power", "stability", "influence", "resilience", "innovation"],
        "new_params": ["node_id", "node_name", "survival_metric", "security_metric", "linear_metric", "performance_metric"],
        "default_values": {
            "node_id": "default_node",
            "node_name": "Default Node",
            "survival_metric": 0.5,
            "security_metric": 0.5,
            "linear_metric": 0.5,
            "performance_metric": 0.5
        }
    },
    
    # GlobalSystem.nodes访问修复
    "global_system_nodes": {
        "pattern": r"self\.global_system\.nodes",
        "replacement": "self.global_system.nodes.values()"
    },
    
    # node.node_name访问修复
    "node_name_access": {
        "pattern": r"node\.name",
        "replacement": "node.node_name"
    },
    
    # node.calculate_power()访问修复（仅用于读取操作）
    "node_power_access": {
        "pattern": r"node\.power",
        "replacement": "node.calculate_power()"
    },
    
    # app_name配置修复
    "app_name_config": {
        "pattern": r"self\.config\['app_name'\]",
        "replacement": "self.config.get('app_name', 'TFT Application')"
    },
    
    # shape属性访问修复
    "shape_attribute": {
        "pattern": r"(prev_state|current_state)\.shape",
        "replacement": "np.array(\\1).shape"
    },
    
    # GlobalSystem.get_average_power方法添加
    "add_get_average_power": {
        "pattern": r"def __repr__\(self\) -> str:\s+\"\"\"\s+系统表示\s+\"\"\"\s+return self\.__str__\(\)\s+\}",
        "replacement": "def get_average_power(self) -> float:\n        \"\"\"\n        获取系统平均实力\n        \n        返回:\n            float: 系统平均实力\n        \"\"\"\n        if not self.nodes:\n            return 0.0\n        total_power = sum(node.calculate_power() for node in self.nodes.values())\n        return total_power / len(self.nodes)\n\n    def get_average_power(self) -> float:
        """
        获取系统平均实力
        
        返回:
            float: 系统平均实力
        """
        if not self.nodes:
            return 0.0
        total_power = sum(node.calculate_power() for node in self.nodes.values())
        return total_power / len(self.nodes)

    def get_average_power(self) -> float:
        """
        获取系统平均实力
        
        返回:
            float: 系统平均实力
        """
        if not self.nodes:
            return 0.0
        total_power = sum(node.calculate_power() for node in self.nodes.values())
        return total_power / len(self.nodes)

    def get_average_power(self) -> float:
        """
        获取系统平均实力
        
        返回:
            float: 系统平均实力
        """
        if not self.nodes:
            return 0.0
        total_power = sum(node.calculate_power() for node in self.nodes.values())
        return total_power / len(self.nodes)

    def get_average_power(self) -> float:
        """
        获取系统平均实力
        
        返回:
            float: 系统平均实力
        """
        if not self.nodes:
            return 0.0
        total_power = sum(node.calculate_power() for node in self.nodes.values())
        return total_power / len(self.nodes)

    def get_average_power(self) -> float:
        """
        获取系统平均实力
        
        返回:
            float: 系统平均实力
        """
        if not self.nodes:
            return 0.0
        total_power = sum(node.calculate_power() for node in self.nodes.values())
        return total_power / len(self.nodes)

    def get_average_power(self) -> float:
        """
        获取系统平均实力
        
        返回:
            float: 系统平均实力
        """
        if not self.nodes:
            return 0.0
        total_power = sum(node.calculate_power() for node in self.nodes.values())
        return total_power / len(self.nodes)

    def get_average_power(self) -> float:
        """
        获取系统平均实力
        
        返回:
            float: 系统平均实力
        """
        if not self.nodes:
            return 0.0
        total_power = sum(node.calculate_power() for node in self.nodes.values())
        return total_power / len(self.nodes)

    def __repr__(self) -> str:\n        \"\"\"\n        系统表示\n        \"\"\"\n        return self.__str__()\n    }"
    }
}

# 导入修复
IMPORT_FIXES = {
    "core_framework/tft_core/axioms.py": [
        "import numpy as np"
    ]
}


def read_file(file_path: str) -> str:
    """读取文件内容"""
    full_path = os.path.join(PROJECT_ROOT, file_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(file_path: str, content: str) -> None:
    """写入文件内容"""
    full_path = os.path.join(PROJECT_ROOT, file_path)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)


def fix_sovereign_node_constructor(content: str) -> str:
    """修复SovereignNode构造函数调用"""
    pattern = FIX_RULES["sovereign_node_constructor"]["pattern"]
    old_params = FIX_RULES["sovereign_node_constructor"]["old_params"]
    new_params = FIX_RULES["sovereign_node_constructor"]["new_params"]
    default_values = FIX_RULES["sovereign_node_constructor"]["default_values"]
    
    def replace_constructor(match: re.Match) -> str:
        args = match.group(1)
        args_dict = {}
        
        # 解析参数
        for arg in args.split(','):
            arg = arg.strip()
            if '=' in arg:
                key, value = arg.split('=', 1)
                key = key.strip()
                value = value.strip()
                args_dict[key] = value
        
        # 构建新的参数
        new_args = []
        for i, old_param in enumerate(old_params):
            if old_param in args_dict:
                if old_param == "name":
                    new_args.append(f"node_name={args_dict[old_param]}")
                    new_args.insert(0, f"node_id={args_dict[old_param].replace('\"', '')}")
                else:
                    # 映射到对应的新参数
                    if i < len(new_params):
                        new_args.append(f"{new_params[i]}={args_dict[old_param]}")
        
        # 添加缺失的参数
        if "node_id" not in [arg.split('=')[0] for arg in new_args]:
            new_args.insert(0, f"node_id=\"{default_values['node_id']}\"")
        if "node_name" not in [arg.split('=')[0] for arg in new_args]:
            new_args.append(f"node_name=\"{default_values['node_name']}\"")
        for param in new_params[2:]:
            if param not in [arg.split('=')[0] for arg in new_args]:
                new_args.append(f"{param}={default_values[param]}")
        
        return f"SovereignNode({', '.join(new_args)})"
    
    return re.sub(pattern, replace_constructor, content, flags=re.DOTALL)


def fix_global_system_nodes(content: str) -> str:
    """修复GlobalSystem.nodes访问"""
    pattern = FIX_RULES["global_system_nodes"]["pattern"]
    replacement = FIX_RULES["global_system_nodes"]["replacement"]
    return re.sub(pattern, replacement, content)


def fix_node_name_access(content: str) -> str:
    """修复node.node_name访问"""
    pattern = FIX_RULES["node_name_access"]["pattern"]
    replacement = FIX_RULES["node_name_access"]["replacement"]
    return re.sub(pattern, replacement, content)


def fix_node_power_access(content: str) -> str:
    """修复node.calculate_power()访问"""
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        # 只在不是赋值操作的行中替换node.calculate_power()
        if 'node.power =' not in line:
            line = line.replace('node.calculate_power()', 'node.calculate_power()')
        new_lines.append(line)
    return '\n'.join(new_lines)


def fix_app_name_config(content: str) -> str:
    """修复app_name配置"""
    pattern = FIX_RULES["app_name_config"]["pattern"]
    replacement = FIX_RULES["app_name_config"]["replacement"]
    return re.sub(pattern, replacement, content)


def fix_shape_attribute(content: str) -> str:
    """修复shape属性访问"""
    pattern = FIX_RULES["shape_attribute"]["pattern"]
    replacement = FIX_RULES["shape_attribute"]["replacement"]
    return re.sub(pattern, replacement, content)


def add_get_average_power(content: str) -> str:
    """添加get_average_power方法"""
    pattern = FIX_RULES["add_get_average_power"]["pattern"]
    replacement = FIX_RULES["add_get_average_power"]["replacement"]
    return re.sub(pattern, replacement, content, flags=re.DOTALL)


def add_missing_imports(content: str, imports: List[str]) -> str:
    """添加缺失的导入"""
    # 检查是否已经有导入
    for imp in imports:
        if imp not in content:
            # 在文件开头添加导入
            content = imp + '\n' + content
    return content


def fix_file(file_path: str) -> Tuple[bool, str]:
    """修复单个文件"""
    print(f"正在修复文件: {file_path}")
    
    try:
        content = read_file(file_path)
        original_content = content
        
        # 应用修复规则
        if "global_system.py" in file_path:
            content = add_get_average_power(content)
        elif "global_system_analysis.py" in file_path:
            content = fix_sovereign_node_constructor(content)
        elif "core.py" in file_path:
            content = fix_global_system_nodes(content)
            content = fix_node_name_access(content)
            content = fix_node_power_access(content)
        elif "applications.py" in file_path:
            content = fix_app_name_config(content)
        elif "axioms.py" in file_path:
            content = fix_shape_attribute(content)
            content = add_missing_imports(content, IMPORT_FIXES.get(file_path, []))
        
        # 检查是否有变化
        if content != original_content:
            write_file(file_path, content)
            return True, f"文件 {file_path} 修复成功"
        else:
            return False, f"文件 {file_path} 无需修复"
    except Exception as e:
        return False, f"修复文件 {file_path} 失败: {str(e)}"


def analyze_code_structure():
    """分析代码结构，确保符合拓扑波动理论"""
    print("\n分析代码结构...")
    
    # 检查GlobalSystem类
    global_system_path = os.path.join(PROJECT_ROOT, "core_framework/system_modeling/global_system.py")
    if os.path.exists(global_system_path):
        content = read_file(global_system_path)
        
        # 检查是否有get_average_power方法
        if "def get_average_power" not in content:
            print("GlobalSystem类缺少get_average_power方法，需要添加")
            # 自动添加该方法
            content = add_get_average_power(content)
            write_file(global_system_path, content)
            print("已添加get_average_power方法")
    
    # 检查SovereignNode类
    sovereign_node_path = os.path.join(PROJECT_ROOT, "core_framework/system_modeling/sovereign_node.py")
    if os.path.exists(sovereign_node_path):
        content = read_file(sovereign_node_path)
        
        # 检查是否有calculate_power方法
        if "def calculate_power" not in content:
            print("SovereignNode类缺少calculate_power方法")
    
    print("代码结构分析完成")


def main():
    """主函数"""
    print("开始自动修复代码...")
    print("基于36D拓扑波动理论的自动修复")
    print("三界约束: 生存界 > 安全界 > 线性界 > 性能界")
    print("核心思想: 拓扑为根，波动为魂\n")
    
    # 分析代码结构
    analyze_code_structure()
    
    # 修复文件
    results = []
    for file_path in FILES_TO_FIX:
        full_path = os.path.join(PROJECT_ROOT, file_path)
        if os.path.exists(full_path):
            success, message = fix_file(file_path)
            results.append((success, message))
        else:
            results.append((False, f"文件 {file_path} 不存在"))
    
    # 打印修复结果
    print("\n修复结果:")
    print("=" * 60)
    for success, message in results:
        status = "✓" if success else "✗"
        print(f"{status} {message}")
    print("=" * 60)
    
    # 运行测试
    print("\n运行测试验证修复结果...")
    test_command = f"python -m unittest discover -s {os.path.join(PROJECT_ROOT, 'tests')} -v"
    print(f"执行命令: {test_command}")
    
    try:
        import subprocess
        result = subprocess.run(test_command, shell=True, capture_output=True, text=True)
        print("\n测试输出:")
        print(result.stdout)
        if result.stderr:
            print("\n测试错误:")
            print(result.stderr)
        print(f"\n测试返回码: {result.returncode}")
    except Exception as e:
        print(f"运行测试失败: {str(e)}")
    
    print("\n自动修复完成！")


if __name__ == "__main__":
    main()
