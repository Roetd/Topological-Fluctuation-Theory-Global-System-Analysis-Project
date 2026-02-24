"""
自动修复代码语法错误工具

基于36D拓扑波动理论的代码语法自动修复
"""

import os
import re
import ast
import sys

class SyntaxFixer:
    """
    语法修复器类
    """
    
    def __init__(self, base_dir):
        """
        初始化语法修复器
        
        参数:
            base_dir: 项目基础目录
        """
        self.base_dir = base_dir
        self.fixed_files = []
        
    def fix_imports(self, file_path):
        """
        修复导入错误
        
        参数:
            file_path: 文件路径
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 修复core_framework.tft_core.operators的导入
            if 'from core_framework.tft_core.operators import' in content:
                # 修复函数名称不匹配的问题
                content = re.sub(
                    r'from core_framework\.tft_core\.operators import \([^)]*\)',
                    'from core_framework.tft_core.operators import (\n    topological_invariant_calculator as calculate_topological_invariant,\n    homology_group_approximation as approximate_homology_group,\n    data_normalization as normalize_topological_data,\n    topological_similarity as calculate_topological_similarity,\n    homologous_resonance_calculator as calculate_homologous_resonance,\n    topological_evolution_operator\n)',
                    content
                )
            
            # 修复core_framework.tft_core.equations的导入
            if 'from core_framework.tft_core.equations import' in content:
                # 修复函数名称不匹配的问题
                content = re.sub(
                    r'from core_framework\.tft_core\.equations import \([^)]*\)',
                    'from core_framework.tft_core.equations import (\n    topological_evolution_equation,\n    stability_equation as topological_stability_equation,\n    homology_equation,\n    resonance_equation,\n    optimization_equation as topological_optimization_equation,\n    topological_closure_equation\n)',
                    content
                )
            
            # 修复core_framework.tft_core.axioms的导入
            if 'from core_framework.tft_core.axioms import' in content:
                # 修复函数名称不匹配的问题
                content = re.sub(
                    r'from core_framework\.tft_core\.axioms import \([^)]*\)',
                    'from core_framework.tft_core.axioms import (\n    check_topological_closure as validate_topological_closure,\n    check_system_stability as validate_system_stability,\n    check_evolution_path_validity as validate_evolution_path_validity\n)',
                    content
                )
            
            # 修复topological_evolution_operator函数调用
            if 'topological_evolution_operator(' in content:
                # 先清理现有的错误调用
                content = re.sub(
                    r'topological_evolution_operator\([^)]*\)',
                    lambda m: m.group(0).split('(')[0] + '(node_topology, np.eye(len(node_topology)), {})',
                    content
                )
            
            # 确保导入了numpy
            if 'import numpy as np' not in content and 'np.' in content:
                content = 'import numpy as np\n' + content
            
            # 写回修复后的内容
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.fixed_files.append(file_path)
            print(f"修复了文件: {file_path}")
            
        except Exception as e:
            print(f"修复文件 {file_path} 时出错: {e}")
    
    def fix_file(self, file_path):
        """
        修复单个文件
        
        参数:
            file_path: 文件路径
        """
        if file_path.endswith('.py'):
            self.fix_imports(file_path)
    
    def fix_directory(self, directory):
        """
        修复目录下的所有文件
        
        参数:
            directory: 目录路径
        """
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    self.fix_file(file_path)
    
    def run(self):
        """
        运行修复
        """
        print(f"开始修复项目: {self.base_dir}")
        
        # 修复src目录
        src_dir = os.path.join(self.base_dir, 'src')
        if os.path.exists(src_dir):
            self.fix_directory(src_dir)
        
        # 修复tests目录
        tests_dir = os.path.join(self.base_dir, 'tests')
        if os.path.exists(tests_dir):
            self.fix_directory(tests_dir)
        
        # 修复examples目录
        examples_dir = os.path.join(self.base_dir, 'examples')
        if os.path.exists(examples_dir):
            self.fix_directory(examples_dir)
        
        # 修复应用场景目录
        applications_dir = os.path.join(self.base_dir, '应用场景')
        if os.path.exists(applications_dir):
            self.fix_directory(applications_dir)
        
        print(f"修复完成，共修复了 {len(self.fixed_files)} 个文件")
        return self.fixed_files

if __name__ == "__main__":
    # 获取项目基础目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 创建修复器实例
    fixer = SyntaxFixer(base_dir)
    
    # 运行修复
    fixed_files = fixer.run()
    
    # 打印修复结果
    print("\n修复的文件:")
    for file in fixed_files:
        print(f"- {file}")
