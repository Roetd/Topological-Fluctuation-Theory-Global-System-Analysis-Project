"""
测试TFT系统应用模块

基于36D拓扑波动理论的应用场景测试
"""

import unittest
import sys
import os
import tempfile

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.applications import (
    TFTApplication, GlobalSystemAnalysisApp,
    EvolutionPathSimulationApp, SystemOptimizationApp, DataAnalysisApp
)
from 应用场景.global_system_analysis import GlobalSystemAnalyzer

class TestTFTApplication(unittest.TestCase):
    """
    测试TFT应用基类
    """
    
    def test_initialization(self):
        """
        测试应用初始化
        """
        app = TFTApplication({"debug": True})
        app.initialize()
        
        # 验证应用初始化成功
        self.assertIsNotNone(app.tft_system)
        self.assertIsNotNone(app.data_ingestor)
        self.assertIsNotNone(app.file_manager)
        
        app.cleanup()

class TestGlobalSystemAnalysisApp(unittest.TestCase):
    """
    测试全球系统分析应用
    """
    
    def test_initialization(self):
        """
        测试应用初始化
        """
        app = GlobalSystemAnalysisApp({"debug": True})
        app.initialize()
        
        # 验证应用初始化成功
        self.assertIsNotNone(app.tft_system)
        self.assertIsNotNone(app.analyzer)
        
        app.cleanup()
    
    def test_load_system(self):
        """
        测试加载系统
        """
        analyzer = GlobalSystemAnalyzer()
        system = analyzer.load_system()
        
        # 验证系统加载成功
        self.assertIsNotNone(system)

class TestEvolutionPathSimulationApp(unittest.TestCase):
    """
    测试演化路径模拟应用
    """
    
    def test_initialization(self):
        """
        测试应用初始化
        """
        app = EvolutionPathSimulationApp({"debug": True})
        app.initialize()
        
        # 验证应用初始化成功
        self.assertIsNotNone(app.tft_system)
        self.assertIsNotNone(app.evolution_analyzer)
        self.assertEqual(len(app.tft_system.global_system.nodes.values()), 5)
        
        app.cleanup()

class TestSystemOptimizationApp(unittest.TestCase):
    """
    测试系统优化应用
    """
    
    def test_initialization(self):
        """
        测试应用初始化
        """
        app = SystemOptimizationApp({"debug": True})
        app.initialize()
        
        # 验证应用初始化成功
        self.assertIsNotNone(app.tft_system)
        self.assertEqual(len(app.tft_system.global_system.nodes.values()), 10)
        
        app.cleanup()

class TestDataAnalysisApp(unittest.TestCase):
    """
    测试数据分析应用
    """
    
    def test_initialization(self):
        """
        测试应用初始化
        """
        app = DataAnalysisApp({"debug": True})
        app.initialize()
        
        # 验证应用初始化成功
        self.assertIsNotNone(app.tft_system)
        self.assertIsNotNone(app.data_processor)
        self.assertIsNotNone(app.model_trainer)
        
        app.cleanup()

if __name__ == "__main__":
    unittest.main()
