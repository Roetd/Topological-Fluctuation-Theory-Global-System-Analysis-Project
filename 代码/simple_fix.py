#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于36D拓扑波动理论的简化自动修复脚本

专注于修复核心问题，避免语法错误
"""

import os
import re

class SimpleCodeFixer:
    """简化版代码修复器类"""
    
    def __init__(self, project_root):
        self.project_root = project_root
        self.fixed_files = []
        self.fix_stats = {
            'constructor_calls': 0,
            'attribute_access': 0,
            'dictionary_access': 0,
            'function_calls': 0,
            'method_additions': 0
        }
    
    def find_python_files(self):
        """查找项目中的所有Python文件"""
        python_files = []
        for root, _, files in os.walk(self.project_root):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    file_path = os.path.normpath(file_path)
                    python_files.append(file_path)
        return python_files
    
    def fix_file(self, file_path):
        """修复单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 1. 修复 SovereignNode 构造函数调用
            content = self.fix_sovereignnode_constructor(content)
            
            # 2. 修复 GlobalSystem.nodes 访问
            content = self.fix_globalsystem_nodes_access(content)
            
            # 3. 修复 node 属性访问
            content = self.fix_node_attribute_access(content)
            
            # 4. 修复函数调用赋值错误
            content = self.fix_function_call_assignments(content)
            
            # 5. 向 GlobalSystem 类添加 get_average_power 方法
            content = self.add_get_average_power(content)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.fixed_files.append(file_path)
                return True
            return False
            
        except Exception as e:
            print(f"修复文件 {file_path} 时出错: {str(e)}")
            return False
    
    def fix_sovereignnode_constructor(self, content):
        """修复 SovereignNode 构造函数调用"""
        # 修复 name 参数
        pattern = r'SovereignNode\(\s*name=(\s*[^,)]+)'
        replacement = r'SovereignNode(node_name=\1'
        fixed_content = re.sub(pattern, replacement, content)
        
        # 修复其他参数映射
        param_mappings = {
            'power': 'survival_metric',
            'stability': 'security_metric',
            'influence': 'linear_metric',
            'resilience': 'performance_metric',
            'innovation': 'performance_metric'
        }
        
        for old_param, new_param in param_mappings.items():
            pattern = rf'\b{old_param}='
            replacement = f'{new_param}='
            fixed_content = re.sub(pattern, replacement, fixed_content)
        
        if fixed_content != content:
            self.fix_stats['constructor_calls'] += 1
        
        return fixed_content
    
    def fix_globalsystem_nodes_access(self, content):
        """修复 GlobalSystem.nodes 访问"""
        pattern = r'(self\.global_system|global_system)\.nodes(?!\.values\(\))'
        replacement = r'\1.nodes.values()'
        fixed_content = re.sub(pattern, replacement, content)
        
        if fixed_content != content:
            self.fix_stats['dictionary_access'] += 1
        
        return fixed_content
    
    def fix_node_attribute_access(self, content):
        """修复 node 属性访问"""
        # 修复 node.node_name
        pattern1 = r'node\.name'
        replacement1 = r'node.node_name'
        fixed_content = re.sub(pattern1, replacement1, content)
        
        # 修复 node.calculate_power()（排除赋值操作）
        pattern2 = r'node\.power(?!\s*=)'
        replacement2 = r'node.calculate_power()'
        fixed_content = re.sub(pattern2, replacement2, fixed_content)
        
        if fixed_content != content:
            self.fix_stats['attribute_access'] += 1
        
        return fixed_content
    
    def fix_function_call_assignments(self, content):
        """修复函数调用赋值错误"""
        # 修复 for metric in node.metrics:
        node.metrics[metric] *= 1.05
        pattern = r'node\.calculate_power\(\)\s*\*=\s*([0-9.]+)'
        replacement = r'for metric in node.metrics:\n        node.metrics[metric] *= \1'
        fixed_content = re.sub(pattern, replacement, content)
        
        # 修复其他函数调用赋值错误
        pattern2 = r'([a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)*\(\))\s*=\s*(.+)'  
        replacement2 = r'# 修复: 函数调用不能用于赋值操作 - 原始代码: \1 = \3'
        fixed_content = re.sub(pattern2, replacement2, fixed_content)
        
        if fixed_content != content:
            self.fix_stats['function_calls'] += 1
        
        return fixed_content
    
    def add_get_average_power(self, content):
        """向 GlobalSystem 类添加 get_average_power 方法"""
        pattern = r'(def __repr__\(self\).*?return self\.__str__\(\))'
        replacement = r'def get_average_power(self) -> float:\n        """\n        获取系统平均实力\n        \n        返回:\n            float: 系统平均实力\n        """\n        if not self.nodes:\n            return 0.0\n        total_power = sum(node.calculate_power() for node in self.nodes.values())\n        return total_power / len(self.nodes)\n\n    \1'
        
        fixed_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        if fixed_content != content:
            self.fix_stats['method_additions'] += 1
        
        return fixed_content
    
    def run(self):
        """运行修复脚本"""
        print("开始修复代码...")
        print(f"项目根目录: {self.project_root}")
        
        python_files = self.find_python_files()
        print(f"找到 {len(python_files)} 个Python文件")
        
        for file_path in python_files:
            print(f"正在修复: {file_path}")
            self.fix_file(file_path)
        
        print("\n修复完成!")
        print(f"修复的文件数: {len(self.fixed_files)}")
        print("修复统计:")
        for fix_type, count in self.fix_stats.items():
            print(f"- {fix_type}: {count}")
        
        if self.fixed_files:
            print("\n修复的文件:")
            for file_path in self.fixed_files[:10]:
                print(f"- {file_path}")
            if len(self.fixed_files) > 10:
                print(f"... 等 {len(self.fixed_files) - 10} 个文件")
        
        return {
            'fixed_files': len(self.fixed_files),
            'fix_stats': self.fix_stats
        }

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='基于36D拓扑波动理论的简化自动修复脚本')
    parser.add_argument('--project-root', 
                        default='.', 
                        help='项目根目录路径')
    
    args = parser.parse_args()
    
    fixer = SimpleCodeFixer(args.project_root)
    fixer.run()

if __name__ == '__main__':
    main()
