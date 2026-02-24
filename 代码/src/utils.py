"""
TFT系统工具模块

基于36D拓扑波动理论的工具函数实现
"""

import json
import yaml
import pandas as pd
import numpy as np
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from 工具包.data_utils import (
    load_json, save_json, load_yaml, save_yaml, load_csv, save_csv,
    normalize_data, handle_missing_values, validate_data_structure
)
from 工具包.file_utils import (
    ensure_directory, list_files, list_subdirectories, file_exists, directory_exists,
    copy_file, move_file, delete_file, delete_directory, get_file_size, get_file_modified_time,
    get_relative_path, get_absolute_path
)

class DataIngestor:
    """
    数据导入器类
    
    基于36D拓扑波动理论的数据导入功能
    """
    
    def __init__(self, config=None):
        """
        初始化数据导入器
        
        参数:
            config: 配置字典
        """
        self.config = config or {
            "input_dir": "../data/input",
            "output_dir": "../data/processed",
            "default_file_format": "csv",
            "encoding": "utf-8",
            "normalize_data": True,
            "handle_missing_values": True,
            "missing_value_strategy": "mean"
        }
        
        # 确保目录存在
        ensure_directory(self.config["input_dir"])
        ensure_directory(self.config["output_dir"])
    
    def ingest_data(self, file_path=None, data_format=None):
        """
        导入数据
        
        参数:
            file_path: 文件路径
            data_format: 数据格式
        
        返回:
            pd.DataFrame: 导入的数据
        """
        if not file_path:
            # 自动查找输入目录中的文件
            files = list_files(self.config["input_dir"])
            if not files:
                raise ValueError("输入目录中没有文件")
            file_path = files[0]
        
        if not data_format:
            # 从文件扩展名推断格式
            ext = os.path.splitext(file_path)[1].lower()
            if ext == ".json":
                data_format = "json"
            elif ext == ".yaml" or ext == ".yml":
                data_format = "yaml"
            elif ext == ".csv":
                data_format = "csv"
            else:
                data_format = self.config["default_file_format"]
        
        # 加载数据
        try:
            if data_format == "json":
                data = load_json(file_path)
                df = pd.DataFrame(data)
            elif data_format == "yaml":
                data = load_yaml(file_path)
                df = pd.DataFrame(data)
            elif data_format == "csv":
                df = load_csv(file_path)
            else:
                raise ValueError(f"不支持的数据格式: {data_format}")
        except Exception as e:
            raise ValueError(f"加载数据失败: {e}")
        
        # 处理数据
        if self.config["handle_missing_values"]:
            for col in df.columns:
                if df[col].isnull().any():
                    df[col] = handle_missing_values(df[col].values, self.config["missing_value_strategy"])
        
        if self.config["normalize_data"]:
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            for col in numeric_columns:
                df[col] = normalize_data(df[col].values)
        
        # 保存处理后的数据
        output_file = os.path.join(
            self.config["output_dir"],
            f"processed_{os.path.basename(file_path)}"
        )
        
        if data_format == "json":
            save_json(df.to_dict('records'), output_file)
        elif data_format == "yaml":
            save_yaml(df.to_dict('records'), output_file)
        elif data_format == "csv":
            save_csv(df, output_file)
        
        return df
    
    def ingest_multiple_files(self, file_paths=None):
        """
        导入多个文件
        
        参数:
            file_paths: 文件路径列表
        
        返回:
            dict: 导入的数据字典
        """
        if not file_paths:
            # 导入输入目录中的所有文件
            file_paths = list_files(self.config["input_dir"])
        
        ingested_data = {}
        for file_path in file_paths:
            try:
                file_name = os.path.basename(file_path)
                data = self.ingest_data(file_path)
                ingested_data[file_name] = data
            except Exception as e:
                print(f"导入文件 {file_path} 失败: {e}")
        
        return ingested_data
    
    def generate_synthetic_data(self, n_samples=1000, n_features=5, seed=42):
        """
        生成合成数据
        
        参数:
            n_samples: 样本数量
            n_features: 特征数量
            seed: 随机种子
        
        返回:
            pd.DataFrame: 合成数据
        """
        np.random.seed(seed)
        
        # 生成特征数据
        features = np.random.rand(n_samples, n_features)
        
        # 基于拓扑波动理论生成目标值
        targets = np.zeros(n_samples)
        for i in range(n_samples):
            # 简单的拓扑波动模型
            targets[i] = (
                np.sin(features[i, 0]) + 
                np.cos(features[i, 1]) + 
                features[i, 2] * features[i, 3] + 
                np.log(features[i, 4] + 1)
            )
        
        # 组合数据
        data = np.hstack((features, targets.reshape(-1, 1)))
        columns = [f"feature_{i+1}" for i in range(n_features)] + ["target"]
        
        df = pd.DataFrame(data, columns=columns)
        
        # 保存合成数据
        output_file = os.path.join(
            self.config["output_dir"],
            f"synthetic_data_{n_samples}_{n_features}.csv"
        )
        save_csv(df, output_file)
        
        return df
    
    def validate_data(self, data, expected_structure):
        """
        验证数据结构
        
        参数:
            data: 输入数据
            expected_structure: 期望的数据结构
        
        返回:
            bool: 数据结构是否有效
        """
        if isinstance(data, pd.DataFrame):
            # 验证列名
            if isinstance(expected_structure, list):
                return all(col in data.columns for col in expected_structure)
            elif isinstance(expected_structure, dict):
                return all(col in data.columns for col in expected_structure.keys())
        elif isinstance(data, dict):
            return validate_data_structure(data, expected_structure)
        elif isinstance(data, list):
            return validate_data_structure(data, expected_structure)
        
        return False

class FileManager:
    """
    文件管理器类
    
    基于36D拓扑波动理论的文件管理功能
    """
    
    def __init__(self, config=None):
        """
        初始化文件管理器
        
        参数:
            config: 配置字典
        """
        self.config = config or {
            "base_dir": "../data",
            "input_dir": "input",
            "output_dir": "output",
            "processed_dir": "processed",
            "models_dir": "models",
            "logs_dir": "logs"
        }
        
        # 初始化目录结构
        self._init_directories()
    
    def _init_directories(self):
        """
        初始化目录结构
        """
        # 创建基础目录
        ensure_directory(self.config["base_dir"])
        
        # 创建子目录
        for dir_name in ["input_dir", "output_dir", "processed_dir", "models_dir", "logs_dir"]:
            dir_path = os.path.join(self.config["base_dir"], self.config[dir_name])
            ensure_directory(dir_path)
            # 更新配置中的绝对路径
            self.config[dir_name] = dir_path
    
    def get_file_path(self, file_name, directory="input_dir"):
        """
        获取文件路径
        
        参数:
            file_name: 文件名
            directory: 目录类型
        
        返回:
            str: 文件路径
        """
        if directory not in self.config:
            raise ValueError(f"不支持的目录类型: {directory}")
        
        return os.path.join(self.config[directory], file_name)
    
    def list_files_by_type(self, file_type="all", directory="input_dir"):
        """
        按类型列出文件
        
        参数:
            file_type: 文件类型
            directory: 目录类型
        
        返回:
            list: 文件路径列表
        """
        if directory not in self.config:
            raise ValueError(f"不支持的目录类型: {directory}")
        
        files = list_files(self.config[directory])
        
        if file_type != "all":
            ext_map = {
                "json": ".json",
                "yaml": [".yaml", ".yml"],
                "csv": ".csv",
                "txt": ".txt"
            }
            
            if file_type not in ext_map:
                raise ValueError(f"不支持的文件类型: {file_type}")
            
            ext = ext_map[file_type]
            if isinstance(ext, list):
                files = [f for f in files if any(f.lower().endswith(e) for e in ext)]
            else:
                files = [f for f in files if f.lower().endswith(ext)]
        
        return files
    
    def backup_file(self, file_path, backup_dir=None):
        """
        备份文件
        
        参数:
            file_path: 文件路径
            backup_dir: 备份目录
        
        返回:
            str: 备份文件路径
        """
        if not file_exists(file_path):
            raise ValueError(f"文件不存在: {file_path}")
        
        if not backup_dir:
            backup_dir = os.path.join(self.config["base_dir"], "backup")
            ensure_directory(backup_dir)
        
        # 创建备份文件名
        base_name = os.path.basename(file_path)
        name, ext = os.path.splitext(base_name)
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        backup_file_name = f"{name}_{timestamp}{ext}"
        backup_file_path = os.path.join(backup_dir, backup_file_name)
        
        # 复制文件
        copy_file(file_path, backup_file_path)
        
        return backup_file_path
    
    def cleanup_files(self, directory="processed_dir", days=7):
        """
        清理文件
        
        参数:
            directory: 目录类型
            days: 保留天数
        
        返回:
            int: 清理的文件数量
        """
        if directory not in self.config:
            raise ValueError(f"不支持的目录类型: {directory}")
        
        cleanup_count = 0
        cutoff_time = pd.Timestamp.now() - pd.Timedelta(days=days)
        cutoff_timestamp = cutoff_time.timestamp()
        
        files = list_files(self.config[directory])
        for file_path in files:
            modified_time = get_file_modified_time(file_path)
            if modified_time < cutoff_timestamp:
                delete_file(file_path)
                cleanup_count += 1
        
        return cleanup_count

def setup_environment(config=None):
    """
    设置环境
    
    参数:
        config: 配置字典
    
    返回:
        dict: 环境配置
    """
    default_config = {
        "project_root": os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')),
        "data_dir": os.path.join(os.path.dirname(__file__), '..', '..', 'data'),
        "code_dir": os.path.join(os.path.dirname(__file__), '..'),
        "logs_dir": os.path.join(os.path.dirname(__file__), '..', '..', 'logs'),
        "models_dir": os.path.join(os.path.dirname(__file__), '..', '..', 'models')
    }
    
    if config:
        default_config.update(config)
    
    # 确保所有目录存在
    for dir_path in default_config.values():
        if isinstance(dir_path, str) and os.path.isdir(os.path.dirname(dir_path)):
            ensure_directory(dir_path)
    
    return default_config

def get_project_info():
    """
    获取项目信息
    
    返回:
        dict: 项目信息
    """
    return {
        "project_name": "TFT-Practice-Project",
        "version": "1.0.0",
        "description": "基于36D拓扑波动理论的AGI实践项目",
        "author": "拓扑波动AI架构团队",
        "based_on": "36D拓扑波动理论",
        "core_components": [
            "TFTSystem",
            "SovereignNode",
            "EvolutionAnalyzer",
            "DataIngestor",
            "ModelTrainer",
            "GlobalSystemAnalyzer"
        ],
        "evolution_paths": [
            "特朗普路径",
            "多边主义路径",
            "同源共生路径"
        ]
    }
