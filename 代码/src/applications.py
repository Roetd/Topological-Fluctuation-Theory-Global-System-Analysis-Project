"""
TFT系统应用模块

基于36D拓扑波动理论的应用场景实现
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core import TFTSystem, EvolutionAnalyzer
from src.utils import DataIngestor, FileManager
from 训练体系.data_processing import DataProcessor
from 训练体系.model_training import ModelTrainer
from 应用场景.global_system_analysis import GlobalSystemAnalyzer

class TFTApplication:
    """
    TFT应用基类
    
    基于36D拓扑波动理论的应用场景基类
    """
    
    def __init__(self, config=None):
        """
        初始化TFT应用
        
        参数:
            config: 配置字典
        """
        self.config = config or {
            "app_name": "TFT Application",
            "debug": False,
            "log_level": "info"
        }
        self.tft_system = None
        self.data_ingestor = None
        self.file_manager = None
    
    def initialize(self):
        """
        初始化应用
        """
        # 初始化文件管理器
        self.file_manager = FileManager()
        
        # 初始化数据导入器
        self.data_ingestor = DataIngestor()
        
        # 初始化TFT系统
        self.tft_system = TFTSystem()
        
        if self.config["debug"]:
            print(f"{self.config.get('app_name', 'TFT Application')} 初始化完成")
    
    def run(self):
        """
        运行应用
        """
        raise NotImplementedError("子类必须实现run方法")
    
    def cleanup(self):
        """
        清理应用
        """
        if self.config["debug"]:
            print(f"{self.config.get('app_name', 'TFT Application')} 清理完成")

class GlobalSystemAnalysisApp(TFTApplication):
    """
    全球系统分析应用
    
    基于36D拓扑波动理论的全球系统分析应用
    """
    
    def __init__(self, config=None):
        """
        初始化全球系统分析应用
        
        参数:
            config: 配置字典
        """
        app_config = config or {}
        app_config["app_name"] = "Global System Analysis App"
        super().__init__(app_config)
        self.analyzer = None
    
    def initialize(self):
        """
        初始化应用
        """
        super().initialize()
        self.analyzer = GlobalSystemAnalyzer()
        
        if self.config["debug"]:
            print("全球系统分析器初始化完成")
    
    def run(self):
        """
        运行应用
        """
        try:
            # 加载系统
            print("加载全球系统...")
            self.analyzer.load_system()
            
            # 分析系统
            print("分析全球系统...")
            analysis_result = self.analyzer.analyze_system()
            print(f"系统分析完成，总节点数: {analysis_result['system_properties']['total_nodes']}")
            print(f"系统弹性: {analysis_result['system_properties']['system_resilience']:.4f}")
            print(f"系统创新性: {analysis_result['system_properties']['system_innovation']:.4f}")
            print(f"平均稳定性: {analysis_result['system_properties']['average_stability']:.4f}")
            
            # 模拟演化
            print("模拟系统演化...")
            evolution_history = self.analyzer.simulate_evolution(50)
            print(f"演化模拟完成，共执行 {len(evolution_history)} 步")
            
            # 推荐演化路径
            print("推荐演化路径...")
            recommendation = self.analyzer.recommend_evolution_path()
            print(f"最佳演化路径: {recommendation['best_path']}")
            print("推荐理由:")
            for reason in recommendation['reasons']:
                print(f"- {reason}")
            print("行动项:")
            for action in recommendation['action_items']:
                print(f"- {action}")
                
        except Exception as e:
            print(f"运行应用失败: {e}")
        finally:
            self.cleanup()

class EvolutionPathSimulationApp(TFTApplication):
    """
    演化路径模拟应用
    
    基于36D拓扑波动理论的演化路径模拟应用
    """
    
    def __init__(self, config=None):
        """
        初始化演化路径模拟应用
        
        参数:
            config: 配置字典
        """
        app_config = config or {}
        app_config["app_name"] = "Evolution Path Simulation App"
        super().__init__(app_config)
        self.evolution_analyzer = None
    
    def initialize(self):
        """
        初始化应用
        """
        super().initialize()
        self.evolution_analyzer = EvolutionAnalyzer(self.tft_system)
        
        # 添加默认节点
        for i in range(5):
            self.tft_system.add_node({
                "name": f"Node_{i+1}",
                "power": 1.0 + i * 0.2,
                "stability": 0.5,
                "influence": 0.5 + i * 0.1,
                "resilience": 0.5,
                "innovation": 0.5 + i * 0.1
            })
        
        if self.config["debug"]:
            print("演化路径分析器初始化完成")
    
    def run(self):
        """
        运行应用
        """
        try:
            # 分析演化路径
            print("分析演化路径...")
            path_analysis = self.evolution_analyzer.analyze_evolution_paths()
            print(f"最佳演化路径: {path_analysis['best_path']}")
            print(f"最佳路径评分: {path_analysis['best_path_score']:.4f}")
            print(f"最佳路径有效性: {path_analysis['best_path_validity']}")
            
            # 模拟演化路径
            print("模拟演化路径...")
            simulation_result = self.evolution_analyzer.simulate_evolution_paths(100)
            
            # 打印模拟结果
            print("模拟结果比较:")
            for path_name, comparison in simulation_result['path_comparison'].items():
                print(f"\n{path_name}:")
                print(f"  系统弹性: {comparison['final_system_resilience']:.4f}")
                print(f"  系统创新性: {comparison['final_system_innovation']:.4f}")
                print(f"  平均稳定性: {comparison['final_average_stability']:.4f}")
                print(f"  拓扑熵: {comparison['final_topological_entropy']:.4f}")
                
        except Exception as e:
            print(f"运行应用失败: {e}")
        finally:
            self.cleanup()

class SystemOptimizationApp(TFTApplication):
    """
    系统优化应用
    
    基于36D拓扑波动理论的系统优化应用
    """
    
    def __init__(self, config=None):
        """
        初始化系统优化应用
        
        参数:
            config: 配置字典
        """
        app_config = config or {}
        app_config["app_name"] = "System Optimization App"
        super().__init__(app_config)
    
    def initialize(self):
        """
        初始化应用
        """
        super().initialize()
        
        # 添加默认节点
        for i in range(10):
            self.tft_system.add_node({
                "name": f"Node_{i+1}",
                "power": 0.5 + np.random.rand() * 0.5,
                "stability": 0.3 + np.random.rand() * 0.4,
                "influence": 0.3 + np.random.rand() * 0.4,
                "resilience": 0.3 + np.random.rand() * 0.4,
                "innovation": 0.3 + np.random.rand() * 0.4
            })
        
        if self.config["debug"]:
            print("系统优化应用初始化完成")
    
    def run(self):
        """
        运行应用
        """
        try:
            # 初始分析
            print("初始系统分析...")
            initial_analysis = self.tft_system.analyze_system()
            print(f"初始系统弹性: {initial_analysis['system_properties']['system_resilience']:.4f}")
            print(f"初始系统创新性: {initial_analysis['system_properties']['system_innovation']:.4f}")
            print(f"初始平均稳定性: {initial_analysis['system_properties']['average_stability']:.4f}")
            
            # 优化系统
            print("优化系统...")
            optimization_result = self.tft_system.optimize_system(200)
            print(f"优化完成，迭代次数: {len(optimization_result['optimization_history'])}")
            print(f"初始目标值: {optimization_result['initial_objective']:.4f}")
            print(f"最终目标值: {optimization_result['final_objective']:.4f}")
            print(f"改进幅度: {optimization_result['improvement']:.4f}")
            
            # 最终分析
            print("最终系统分析...")
            final_analysis = optimization_result['final_analysis']
            print(f"最终系统弹性: {final_analysis['system_properties']['system_resilience']:.4f}")
            print(f"最终系统创新性: {final_analysis['system_properties']['system_innovation']:.4f}")
            print(f"最终平均稳定性: {final_analysis['system_properties']['average_stability']:.4f}")
            
            # 计算系统共振
            print("计算系统共振...")
            resonance_analysis = self.tft_system.calculate_system_resonance()
            if resonance_analysis['resonance_possible']:
                print(f"平均共振值: {resonance_analysis['average_resonance']:.4f}")
                print(f"高共振对数量: {len(resonance_analysis['high_resonance_pairs'])}")
            else:
                print(resonance_analysis['message'])
                
        except Exception as e:
            print(f"运行应用失败: {e}")
        finally:
            self.cleanup()

class DataAnalysisApp(TFTApplication):
    """
    数据分析应用
    
    基于36D拓扑波动理论的数据分析应用
    """
    
    def __init__(self, config=None):
        """
        初始化数据分析应用
        
        参数:
            config: 配置字典
        """
        app_config = config or {}
        app_config["app_name"] = "Data Analysis App"
        super().__init__(app_config)
        self.data_processor = None
        self.model_trainer = None
    
    def initialize(self):
        """
        初始化应用
        """
        super().initialize()
        self.data_processor = DataProcessor()
        self.model_trainer = ModelTrainer()
        
        if self.config["debug"]:
            print("数据分析应用初始化完成")
    
    def run(self):
        """
        运行应用
        """
        try:
            # 生成合成数据
            print("生成合成数据...")
            synthetic_data = self.data_ingestor.generate_synthetic_data(1000, 5)
            print(f"合成数据生成完成，形状: {synthetic_data.shape}")
            
            # 预处理数据
            print("预处理数据...")
            processed_data = self.data_processor.preprocess_data(synthetic_data)
            
            # 分割数据
            print("分割数据...")
            train_data, test_data = self.data_processor.split_data(processed_data, test_size=0.2)
            print(f"训练集大小: {train_data.shape}, 测试集大小: {test_data.shape}")
            
            # 提取特征和目标值
            print("提取特征和目标值...")
            X_train, y_train = self.data_processor.extract_features_and_targets(train_data)
            X_test, y_test = self.data_processor.extract_features_and_targets(test_data)
            
            # 训练模型
            print("训练模型...")
            self.model_trainer.config["model_type"] = "linear"
            self.model_trainer.config["epochs"] = 1000
            history = self.model_trainer.train(X_train, y_train)
            print(f"模型训练完成，最终损失: {history['loss'][-1]:.4f}")
            
            # 评估模型
            print("评估模型...")
            metrics = self.model_trainer.evaluate(X_test, y_test)
            print(f"模型评估结果:")
            print(f"  MSE: {metrics['mse']:.4f}")
            print(f"  RMSE: {metrics['rmse']:.4f}")
            print(f"  R2: {metrics['r2']:.4f}")
            
            # 保存模型
            print("保存模型...")
            self.model_trainer.save_model()
            
        except Exception as e:
            print(f"运行应用失败: {e}")
        finally:
            self.cleanup()

# 导入必要的库
import numpy as np

if __name__ == "__main__":
    # 创建应用实例
    print("=== 拓扑波动AI架构应用 ===")
    print("1. 全球系统分析")
    print("2. 演化路径模拟")
    print("3. 系统优化")
    print("4. 数据分析")
    
    choice = input("请选择应用 (1-4): ")
    
    if choice == "1":
        app = GlobalSystemAnalysisApp({"debug": True})
    elif choice == "2":
        app = EvolutionPathSimulationApp({"debug": True})
    elif choice == "3":
        app = SystemOptimizationApp({"debug": True})
    elif choice == "4":
        app = DataAnalysisApp({"debug": True})
    else:
        print("无效选择")
        exit(1)
    
    # 初始化并运行应用
    app.initialize()
    app.run()
