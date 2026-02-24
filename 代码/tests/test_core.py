"""
测试TFT系统核心功能

基于36D拓扑波动理论的核心功能测试
"""

import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core import TFTSystem, EvolutionAnalyzer

class TestTFTSystem(unittest.TestCase):
    """
    测试TFT系统类
    """
    
    def setUp(self):
        """
        设置测试环境
        """
        self.tft_system = TFTSystem()
    
    def test_initialization(self):
        """
        测试系统初始化
        """
        self.assertEqual(len(self.tft_system.global_system.nodes.values()), 0)
        self.assertEqual(self.tft_system.current_step, 0)
        self.assertEqual(len(self.tft_system.evolution_history), 0)
        self.assertAlmostEqual(self.tft_system.global_system.energy, 100.0)
    
    def test_add_node(self):
        """
        测试添加节点
        """
        # 添加节点
        node_data = {
            "name": "Test_Node",
            "power": 1.0,
            "stability": 0.5,
            "influence": 0.5,
            "resilience": 0.5,
            "innovation": 0.5
        }
        node = self.tft_system.add_node(node_data)
        
        # 验证节点添加成功
        self.assertEqual(len(self.tft_system.global_system.nodes.values()), 1)
        self.assertEqual(node.node_name, "Test_Node")
        self.assertAlmostEqual(node.calculate_power(), 1.0)
        self.assertAlmostEqual(node.stability, 0.5)
    
    def test_remove_node(self):
        """
        测试移除节点
        """
        # 添加节点
        node_data = {
            "name": "Test_Node",
            "power": 1.0,
            "stability": 0.5,
            "influence": 0.5,
            "resilience": 0.5,
            "innovation": 0.5
        }
        self.tft_system.add_node(node_data)
        
        # 验证节点添加成功
        self.assertEqual(len(self.tft_system.global_system.nodes.values()), 1)
        
        # 移除节点
        result = self.tft_system.remove_node("Test_Node")
        
        # 验证节点移除成功
        self.assertTrue(result)
        self.assertEqual(len(self.tft_system.global_system.nodes.values()), 0)
    
    def test_get_node(self):
        """
        测试获取节点
        """
        # 添加节点
        node_data = {
            "name": "Test_Node",
            "power": 1.0,
            "stability": 0.5,
            "influence": 0.5,
            "resilience": 0.5,
            "innovation": 0.5
        }
        self.tft_system.add_node(node_data)
        
        # 获取节点
        node = self.tft_system.get_node("Test_Node")
        
        # 验证节点获取成功
        self.assertIsNotNone(node)
        self.assertEqual(node.node_name, "Test_Node")
    
    def test_evolve(self):
        """
        测试系统演化
        """
        # 添加节点
        node_data = {
            "name": "Test_Node",
            "power": 1.0,
            "stability": 0.5,
            "influence": 0.5,
            "resilience": 0.5,
            "innovation": 0.5
        }
        self.tft_system.add_node(node_data)
        
        # 执行演化
        initial_step = self.tft_system.current_step
        self.tft_system.evolve(1)
        
        # 验证演化成功
        self.assertEqual(self.tft_system.current_step, initial_step + 1)
        self.assertEqual(len(self.tft_system.evolution_history), 1)
    
    def test_analyze_system(self):
        """
        测试系统分析
        """
        # 添加节点
        node_data = {
            "name": "Test_Node",
            "power": 1.0,
            "stability": 0.5,
            "influence": 0.5,
            "resilience": 0.5,
            "innovation": 0.5
        }
        self.tft_system.add_node(node_data)
        
        # 分析系统
        analysis_result = self.tft_system.analyze_system()
        
        # 验证分析结果
        self.assertIn("system_properties", analysis_result)
        self.assertIn("node_analyses", analysis_result)
        self.assertIn("evolution_analyses", analysis_result)
        self.assertEqual(analysis_result["system_properties"]["total_nodes"], 1)
    
    def test_optimize_system(self):
        """
        测试系统优化
        """
        # 添加节点
        node_data = {
            "name": "Test_Node",
            "power": 1.0,
            "stability": 0.5,
            "influence": 0.5,
            "resilience": 0.5,
            "innovation": 0.5
        }
        self.tft_system.add_node(node_data)
        
        # 优化系统
        optimization_result = self.tft_system.optimize_system(10)
        
        # 验证优化结果
        self.assertIn("initial_objective", optimization_result)
        self.assertIn("final_objective", optimization_result)
        self.assertIn("improvement", optimization_result)
        self.assertIn("optimization_history", optimization_result)
    
    def test_calculate_system_resonance(self):
        """
        测试系统共振计算
        """
        # 添加两个节点
        node_data1 = {
            "name": "Node_1",
            "power": 1.0,
            "stability": 0.5,
            "influence": 0.5,
            "resilience": 0.5,
            "innovation": 0.5
        }
        node_data2 = {
            "name": "Node_2",
            "power": 0.8,
            "stability": 0.6,
            "influence": 0.4,
            "resilience": 0.6,
            "innovation": 0.4
        }
        self.tft_system.add_node(node_data1)
        self.tft_system.add_node(node_data2)
        
        # 计算系统共振
        resonance_result = self.tft_system.calculate_system_resonance()
        
        # 验证共振计算结果
        self.assertTrue(resonance_result["resonance_possible"])
        self.assertIn("total_resonance", resonance_result)
        self.assertIn("average_resonance", resonance_result)
        self.assertIn("node_resonances", resonance_result)
    
    def test_save_and_load_system_state(self):
        """
        测试保存和加载系统状态
        """
        import tempfile
        
        # 添加节点
        node_data = {
            "name": "Test_Node",
            "power": 1.0,
            "stability": 0.5,
            "influence": 0.5,
            "resilience": 0.5,
            "innovation": 0.5
        }
        self.tft_system.add_node(node_data)
        
        # 执行演化
        self.tft_system.evolve(5)
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as temp_file:
            temp_file_path = temp_file.name
        
        try:
            # 保存系统状态
            self.tft_system.save_system_state(temp_file_path)
            
            # 创建新系统
            new_tft_system = TFTSystem()
            
            # 加载系统状态
            new_tft_system.load_system_state(temp_file_path)
            
            # 验证系统状态加载成功
            self.assertEqual(len(new_tft_system.global_system.nodes.values()), 1)
            self.assertEqual(new_tft_system.current_step, 5)
            self.assertEqual(len(new_tft_system.evolution_history), 5)
        finally:
            # 清理临时文件
            import os
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

class TestEvolutionAnalyzer(unittest.TestCase):
    """
    测试演化分析器类
    """
    
    def setUp(self):
        """
        设置测试环境
        """
        self.tft_system = TFTSystem()
        self.evolution_analyzer = EvolutionAnalyzer(self.tft_system)
        
        # 添加测试节点
        for i in range(3):
            node_data = {
                "name": f"Node_{i+1}",
                "power": 1.0 + i * 0.2,
                "stability": 0.5,
                "influence": 0.5 + i * 0.1,
                "resilience": 0.5,
                "innovation": 0.5 + i * 0.1
            }
            self.tft_system.add_node(node_data)
    
    def test_analyze_evolution_paths(self):
        """
        测试分析演化路径
        """
        # 分析演化路径
        analysis_result = self.evolution_analyzer.analyze_evolution_paths()
        
        # 验证分析结果
        self.assertIn("path_analyses", analysis_result)
        self.assertIn("path_evaluations", analysis_result)
        self.assertIn("best_path", analysis_result)
        self.assertIn("best_path_score", analysis_result)
        self.assertIn("best_path_validity", analysis_result)
        
        # 验证路径分析包含所有路径
        self.assertIn("trump_path", analysis_result["path_analyses"])
        self.assertIn("multilateral_path", analysis_result["path_analyses"])
        self.assertIn("homologous_path", analysis_result["path_analyses"])
    
    def test_simulate_evolution_paths(self):
        """
        测试模拟演化路径
        """
        # 模拟演化路径
        simulation_result = self.evolution_analyzer.simulate_evolution_paths(10)
        
        # 验证模拟结果
        self.assertIn("path_simulation_results", simulation_result)
        self.assertIn("path_comparison", simulation_result)
        self.assertIn("simulation_steps", simulation_result)
        
        # 验证模拟结果包含所有路径
        self.assertIn("trump_path", simulation_result["path_simulation_results"])
        self.assertIn("multilateral_path", simulation_result["path_simulation_results"])
        self.assertIn("homologous_path", simulation_result["path_simulation_results"])

if __name__ == "__main__":
    unittest.main()
