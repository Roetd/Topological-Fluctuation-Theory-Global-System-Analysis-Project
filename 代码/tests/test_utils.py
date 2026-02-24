"""
测试TFT系统工具模块

基于36D拓扑波动理论的工具功能测试
"""

import unittest
import sys
import os
import tempfile
import pandas as pd
import numpy as np

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import DataIngestor, FileManager, setup_environment, get_project_info
from 工具包.data_utils import load_json, save_json, load_yaml, save_yaml, load_csv, save_csv
from 工具包.file_utils import ensure_directory, list_files, file_exists

class TestDataIngestor(unittest.TestCase):
    """
    测试数据导入器类
    """
    
    def setUp(self):
        """
        设置测试环境
        """
        # 创建临时目录
        self.temp_dir = tempfile.mkdtemp()
        self.input_dir = os.path.join(self.temp_dir, "input")
        self.output_dir = os.path.join(self.temp_dir, "output")
        
        # 创建目录
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 创建数据导入器
        self.config = {
            "input_dir": self.input_dir,
            "output_dir": self.output_dir,
            "normalize_data": True,
            "handle_missing_values": True,
            "missing_value_strategy": "mean"
        }
        self.data_ingestor = DataIngestor(self.config)
    
    def tearDown(self):
        """
        清理测试环境
        """
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_ingest_csv(self):
        """
        测试导入CSV文件
        """
        # 创建测试CSV文件
        test_data = {
            "name": ["Node_1", "Node_2", "Node_3"],
            "power": [1.0, 0.8, 0.6],
            "stability": [0.5, 0.6, 0.4],
            "influence": [0.5, 0.4, 0.6],
            "resilience": [0.5, 0.6, 0.4],
            "innovation": [0.5, 0.4, 0.6]
        }
        df = pd.DataFrame(test_data)
        csv_file = os.path.join(self.input_dir, "test_data.csv")
        df.to_csv(csv_file, index=False)
        
        # 导入数据
        ingested_df = self.data_ingestor.ingest_data(csv_file, "csv")
        
        # 验证数据导入成功
        self.assertEqual(len(ingested_df), 3)
        self.assertIn("name", ingested_df.columns)
        self.assertIn("power", ingested_df.columns)
        self.assertIn("stability", ingested_df.columns)
    
    def test_ingest_json(self):
        """
        测试导入JSON文件
        """
        # 创建测试JSON文件
        test_data = [
            {
                "name": "Node_1",
                "power": 1.0,
                "stability": 0.5,
                "influence": 0.5,
                "resilience": 0.5,
                "innovation": 0.5
            },
            {
                "name": "Node_2",
                "power": 0.8,
                "stability": 0.6,
                "influence": 0.4,
                "resilience": 0.6,
                "innovation": 0.4
            }
        ]
        json_file = os.path.join(self.input_dir, "test_data.json")
        save_json(test_data, json_file)
        
        # 导入数据
        ingested_df = self.data_ingestor.ingest_data(json_file, "json")
        
        # 验证数据导入成功
        self.assertEqual(len(ingested_df), 2)
        self.assertIn("name", ingested_df.columns)
        self.assertIn("power", ingested_df.columns)
    
    def test_ingest_yaml(self):
        """
        测试导入YAML文件
        """
        # 创建测试YAML文件
        test_data = [
            {
                "name": "Node_1",
                "power": 1.0,
                "stability": 0.5,
                "influence": 0.5,
                "resilience": 0.5,
                "innovation": 0.5
            },
            {
                "name": "Node_2",
                "power": 0.8,
                "stability": 0.6,
                "influence": 0.4,
                "resilience": 0.6,
                "innovation": 0.4
            }
        ]
        yaml_file = os.path.join(self.input_dir, "test_data.yaml")
        save_yaml(test_data, yaml_file)
        
        # 导入数据
        ingested_df = self.data_ingestor.ingest_data(yaml_file, "yaml")
        
        # 验证数据导入成功
        self.assertEqual(len(ingested_df), 2)
        self.assertIn("name", ingested_df.columns)
        self.assertIn("power", ingested_df.columns)
    
    def test_generate_synthetic_data(self):
        """
        测试生成合成数据
        """
        # 生成合成数据
        synthetic_df = self.data_ingestor.generate_synthetic_data(100, 5)
        
        # 验证合成数据生成成功
        self.assertEqual(len(synthetic_df), 100)
        self.assertEqual(len(synthetic_df.columns), 6)  # 5个特征 + 1个目标
        self.assertIn("target", synthetic_df.columns)
    
    def test_validate_data(self):
        """
        测试验证数据结构
        """
        # 创建测试数据
        test_data = {
            "name": ["Node_1", "Node_2"],
            "power": [1.0, 0.8],
            "stability": [0.5, 0.6]
        }
        df = pd.DataFrame(test_data)
        
        # 验证数据结构
        expected_structure = ["name", "power", "stability"]
        result = self.data_ingestor.validate_data(df, expected_structure)
        
        # 验证验证结果
        self.assertTrue(result)

class TestFileManager(unittest.TestCase):
    """
    测试文件管理器类
    """
    
    def setUp(self):
        """
        设置测试环境
        """
        # 创建临时目录
        self.temp_dir = tempfile.mkdtemp()
        
        # 创建文件管理器
        self.config = {
            "base_dir": self.temp_dir,
            "input_dir": "input",
            "output_dir": "output",
            "processed_dir": "processed",
            "models_dir": "models",
            "logs_dir": "logs"
        }
        self.file_manager = FileManager(self.config)
    
    def tearDown(self):
        """
        清理测试环境
        """
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_initialization(self):
        """
        测试文件管理器初始化
        """
        # 验证目录创建成功
        self.assertTrue(os.path.exists(self.file_manager.config["input_dir"]))
        self.assertTrue(os.path.exists(self.file_manager.config["output_dir"]))
        self.assertTrue(os.path.exists(self.file_manager.config["processed_dir"]))
        self.assertTrue(os.path.exists(self.file_manager.config["models_dir"]))
        self.assertTrue(os.path.exists(self.file_manager.config["logs_dir"]))
    
    def test_get_file_path(self):
        """
        测试获取文件路径
        """
        # 获取文件路径
        file_path = self.file_manager.get_file_path("test_file.csv", "input_dir")
        
        # 验证文件路径正确
        expected_path = os.path.join(self.file_manager.config["input_dir"], "test_file.csv")
        self.assertEqual(file_path, expected_path)
    
    def test_list_files_by_type(self):
        """
        测试按类型列出文件
        """
        # 创建测试文件
        csv_file = os.path.join(self.file_manager.config["input_dir"], "test_data.csv")
        json_file = os.path.join(self.file_manager.config["input_dir"], "test_data.json")
        
        # 创建空文件
        open(csv_file, 'w').close()
        open(json_file, 'w').close()
        
        # 列出CSV文件
        csv_files = self.file_manager.list_files_by_type("csv", "input_dir")
        self.assertEqual(len(csv_files), 1)
        
        # 列出JSON文件
        json_files = self.file_manager.list_files_by_type("json", "input_dir")
        self.assertEqual(len(json_files), 1)
    
    def test_backup_file(self):
        """
        测试备份文件
        """
        # 创建测试文件
        test_file = os.path.join(self.file_manager.config["input_dir"], "test_data.csv")
        with open(test_file, 'w') as f:
            f.write("name,power,stability\nNode_1,1.0,0.5\n")
        
        # 备份文件
        backup_path = self.file_manager.backup_file(test_file)
        
        # 验证备份成功
        self.assertTrue(os.path.exists(backup_path))
        self.assertTrue("backup" in backup_path)

class TestUtils(unittest.TestCase):
    """
    测试工具函数
    """
    
    def test_setup_environment(self):
        """
        测试设置环境
        """
        # 设置环境
        env_config = setup_environment()
        
        # 验证环境配置
        self.assertIn("project_root", env_config)
        self.assertIn("data_dir", env_config)
        self.assertIn("code_dir", env_config)
        self.assertIn("logs_dir", env_config)
        self.assertIn("models_dir", env_config)
    
    def test_get_project_info(self):
        """
        测试获取项目信息
        """
        # 获取项目信息
        project_info = get_project_info()
        
        # 验证项目信息
        self.assertIn("project_name", project_info)
        self.assertIn("version", project_info)
        self.assertIn("description", project_info)
        self.assertIn("author", project_info)
        self.assertIn("based_on", project_info)
        self.assertIn("core_components", project_info)
        self.assertIn("evolution_paths", project_info)

if __name__ == "__main__":
    unittest.main()
