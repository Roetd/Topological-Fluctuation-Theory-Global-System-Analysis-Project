#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于36D拓扑波动理论的自动修复脚本

本脚本用于系统性地分析和修复TFT-Practice-Project代码中的各种问题，
包括命名、字典、函数、逻辑等错误，基于拓扑波动理论的核心原则。

修复原理：
- 同源共生：通过识别代码中的同源结构，实现一致性修复
- 拓扑不变量：保持代码的核心结构不变，只修复错误部分
- 波动优化：通过波动理论实现代码的动态优化
- 三界约束：确保修复后的代码符合生存界 > 安全界 > 线性界 > 性能界的约束
"""

import os
import re
import subprocess
import time
from typing import Dict, List, Tuple, Any

# 解决中文路径问题
import pathlib
pathlib.Path().resolve()

class CodeFixer:
    """代码修复器类，基于拓扑波动理论"""
    
    def __init__(self, project_root: str):
        """初始化代码修复器
        
        Args:
            project_root: 项目根目录路径
        """
        self.project_root = project_root
        self.fixed_files = []
        self.fix_stats = {
            'constructor_calls': 0,
            'attribute_access': 0,
            'dictionary_access': 0,
            'function_calls': 0,
            'syntax_errors': 0,
            'other_errors': 0,
            'import_fixes': 0,
            'method_additions': 0
        }
        self.debug_mode = False
    
    def find_python_files(self) -> List[str]:
        """查找项目中的所有Python文件
        
        Returns:
            Python文件路径列表
        """
        python_files = []
        for root, _, files in os.walk(self.project_root):
            for file in files:
                if file.endswith('.py'):
                    # 处理中文路径
                    file_path = os.path.join(root, file)
                    file_path = os.path.normpath(file_path)
                    python_files.append(file_path)
        return python_files
    
    def fix_file(self, file_path: str) -> bool:
        """修复单个文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            是否修复成功
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 应用各种修复规则
            original_content = content
            
            # 1. 先修复导入（确保后续修复时依赖的模块已导入）
            content = self.fix_imports(file_path, content)
            
            # 2. 修复构造函数调用
            content = self.fix_sovereignnode_constructor(content)
            
            # 3. 修复GlobalSystem.nodes访问
            content = self.fix_globalsystem_nodes_access(content)
            
            # 4. 修复node属性访问
            content = self.fix_node_attribute_access(content)
            
            # 5. 修复函数调用赋值语法错误
            content = self.fix_function_call_assignments(content)
            
            # 6. 修复字典访问链错误
            content = self.fix_dictionary_access_chains(content)
            
            # 7. 修复shape属性访问
            content = self.fix_shape_attribute(content)
            
            # 8. 向GlobalSystem类添加get_average_power方法
            content = self.add_get_average_power(content)
            
            # 9. 修复app_name配置访问
            content = self.fix_app_name_config(content)
            
            # 如果内容有变化，保存修复后的文件
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.fixed_files.append(file_path)
                return True
            return False
            
        except Exception as e:
            print(f"❌ 修复文件 {file_path} 时出错: {str(e)}")
            return False
    
    def fix_imports(self, file_path: str, content: str) -> str:
        """修复导入语句
        
        Args:
            file_path: 文件路径
            content: 代码内容
            
        Returns:
            修复后的代码内容
        """
        # 检查是否需要导入numpy
        if 'np.array' in content or 'shape' in content or 'np.' in content:
            if 'import numpy as np' not in content and 'import numpy' not in content:
                # 在文件开头添加numpy导入（在注释后，业务代码前）
                # 查找第一个非注释、非空白行
                import_pattern = r'^(?:[^#\n]|\n[^#\n])'
                match = re.search(import_pattern, content)
                if match:
                    # 在第一个业务代码前添加
                    insert_pos = match.start()
                    content = content[:insert_pos] + 'import numpy as np\n\n' + content[insert_pos:]
                else:
                    # 在文件开头添加
                    content = 'import numpy as np\n\n' + content
                self.fix_stats['import_fixes'] += 1
                print(f"✅ 添加numpy导入到 {os.path.basename(file_path)}")
        
        return content
    
    def fix_sovereignnode_constructor(self, content: str) -> str:
        """修复SovereignNode构造函数调用
        
        Args:
            content: 代码内容
            
        Returns:
            修复后的代码内容
        """
        # 修复 SovereignNode(node_name=...) 为 SovereignNode(node_name=...)
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
    
    def fix_globalsystem_nodes_access(self, content: str) -> str:
        """修复GlobalSystem.nodes访问
        
        Args:
            content: 代码内容
            
        Returns:
            修复后的代码内容
        """
        # 修复 GlobalSystem.nodes 访问为 GlobalSystem.nodes.values()
        pattern = r'(self\.global_system|global_system)\.nodes(?!\.values\(\))'
        replacement = r'\1.nodes.values()'
        fixed_content = re.sub(pattern, replacement, content)
        
        if fixed_content != content:
            self.fix_stats['dictionary_access'] += 1
        
        return fixed_content
    
    def fix_node_attribute_access(self, content: str) -> str:
        """修复node属性访问
        
        Args:
            content: 代码内容
            
        Returns:
            修复后的代码内容
        """
        # 修复 node.node_name 为 node.node_name
        pattern1 = r'node\.name'
        replacement1 = r'node.node_name'
        fixed_content = re.sub(pattern1, replacement1, content)
        
        # 修复 node.calculate_power() 为 node.calculate_power()（排除赋值操作）
        pattern2 = r'node\.power(?!\s*=)'
        replacement2 = r'node.calculate_power()'
        fixed_content = re.sub(pattern2, replacement2, fixed_content)
        
        if fixed_content != content:
            self.fix_stats['attribute_access'] += 1
        
        return fixed_content
    
    def fix_function_call_assignments(self, content: str) -> str:
        """修复函数调用赋值语法错误
        
        Args:
            content: 代码内容
            
        Returns:
            修复后的代码内容
        """
        # 修复 for metric in node.metrics:
        node.metrics[metric] *= 1.05 这样的错误
        pattern = r'node\.calculate_power\(\)\s*\*=\s*([0-9.]+)'
        replacement = r'for metric in node.metrics:\n        node.metrics[metric] *= \1'
        fixed_content = re.sub(pattern, replacement, content)
        
        # 修复其他函数调用赋值错误
        pattern2 = r'(\w+\.\w+\(\))\s*='
        replacement2 = r'# 修复: 函数调用不能用于赋值操作'
        fixed_content = re.sub(pattern2, replacement2, fixed_content)
        
        if fixed_content != content:
            self.fix_stats['function_calls'] += 1
        
        return fixed_content
    
    def fix_dictionary_access_chains(self, content: str) -> str:
        """修复字典访问链错误
        
        Args:
            content: 代码内容
            
        Returns:
            修复后的代码内容
        """
        # 修复 .values() 这样的错误
        pattern = r'\.values\(\)\.values\(\)'
        replacement = r'.values()'
        fixed_content = re.sub(pattern, replacement, content)
        
        # 修复更长的访问链
        pattern2 = r'\.values\(\)(\.values\(\))+'
        replacement2 = r'.values()'
        fixed_content = re.sub(pattern2, replacement2, fixed_content)
        
        if fixed_content != content:
            self.fix_stats['dictionary_access'] += 1
        
        return fixed_content
    
    def fix_shape_attribute(self, content: str) -> str:
        """修复shape属性访问
        
        Args:
            content: 代码内容
            
        Returns:
            修复后的代码内容
        """
        # 修复 shape 属性访问，确保对象是numpy数组
        pattern = r'(prev_state|current_state)\.shape'
        replacement = r'np.array(\g<1>).shape'
        fixed_content = re.sub(pattern, replacement, content)
        
        if fixed_content != content:
            self.fix_stats['syntax_errors'] += 1
        
        return fixed_content
    
    def add_get_average_power(self, content: str) -> str:
        """向GlobalSystem类添加get_average_power方法
        
        Args:
            content: 代码内容
            
        Returns:
            修复后的代码内容
        """
        # 查找 __repr__ 方法，在其前添加 get_average_power 方法
        # 使用更宽松的匹配条件
        pattern = r'(def __repr__\(self\).*?return self\.__str__\(\))'
        replacement = r'def get_average_power(self) -> float:\n        """\n        获取系统平均实力\n        \n        返回:\n            float: 系统平均实力\n        """\n        if not self.nodes:\n            return 0.0\n        total_power = sum(node.calculate_power() for node in self.nodes.values())\n        return total_power / len(self.nodes)\n\n    \1'
        
        # 使用 DOTALL 标志使 . 匹配换行符
        fixed_content = re.sub(pattern, replacement, content, flags=re.DOTALL | re.MULTILINE)
        
        if fixed_content != content:
            self.fix_stats['method_additions'] += 1
        
        return fixed_content
    
    def fix_app_name_config(self, content: str) -> str:
        """修复app_name配置访问
        
        Args:
            content: 代码内容
            
        Returns:
            修复后的代码内容
        """
        # 修复 self.config.get('app_name', 'TFT Application') 为 self.config.get('app_name', 'TFT Application')
        pattern = r'self\.config\[\s*\'app_name\'\s*\]'
        replacement = r"self.config.get('app_name', 'TFT Application')"
        fixed_content = re.sub(pattern, replacement, content)
        
        return fixed_content
    
    def run(self):
        """运行修复脚本
        
        Returns:
            修复统计信息
        """
        print("🚀 基于36D拓扑波动理论的代码自动修复开始...")
        print(f"📁 项目根目录: {self.project_root}")
        
        # 查找所有Python文件
        python_files = self.find_python_files()
        print(f"🔍 找到 {len(python_files)} 个Python文件")
        
        # 修复每个文件
        for file_path in python_files:
            print(f"🛠️  正在修复: {file_path}")
            self.fix_file(file_path)
        
        # 打印修复结果
        print("\n🎉 修复完成!")
        print(f"📋 修复的文件数: {len(self.fixed_files)}")
        print("📊 修复统计:")
        for fix_type, count in self.fix_stats.items():
            print(f"- {fix_type}: {count}")
        
        if self.fixed_files:
            print("\n✅ 修复的文件:")
            for file_path in self.fixed_files[:10]:  # 只显示前10个
                print(f"- {file_path}")
            if len(self.fixed_files) > 10:
                print(f"... 等 {len(self.fixed_files) - 10} 个文件")
        
        # 运行测试
        self.run_tests()
        
        return {
            'fixed_files': len(self.fixed_files),
            'fix_stats': self.fix_stats
        }
    
    def run_tests(self, timeout=300):
        """运行测试
        
        Args:
            timeout: 测试超时时间（秒）
            
        Returns:
            测试结果
        """
        print("\n🧪 开始运行测试...")
        
        # 检查tests目录是否存在
        tests_dir = os.path.join(self.project_root, 'tests')
        if not os.path.exists(tests_dir):
            print("⚠️  tests目录不存在，跳过测试")
            return False
        
        # 运行测试
        try:
            start_time = time.time()
            result = subprocess.run(
                ['python', '-m', 'pytest', tests_dir, '-v'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            elapsed_time = time.time() - start_time
            
            print(f"\n📊 测试结果 (耗时: {elapsed_time:.2f}秒):")
            print("\n测试输出:")
            print(result.stdout)
            
            if result.stderr:
                print("\n测试错误:")
                print(result.stderr)
            
            print(f"\n测试返回码: {result.returncode}")
            
            if result.returncode == 0:
                print("✅ 测试通过!")
                return True
            else:
                print("❌ 测试失败!")
                return False
                
        except subprocess.TimeoutExpired:
            print("⏰ 测试超时!")
            return False
        except Exception as e:
            print(f"❌ 运行测试时出错: {str(e)}")
            return False

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='基于36D拓扑波动理论的代码自动修复脚本')
    parser.add_argument('--project-root', 
                        default='.', 
                        help='项目根目录路径')
    parser.add_argument('--debug', 
                        action='store_true', 
                        help='启用调试模式')
    
    args = parser.parse_args()
    
    fixer = CodeFixer(args.project_root)
    fixer.debug_mode = args.debug
    fixer.run()

if __name__ == '__main__':
    main()
