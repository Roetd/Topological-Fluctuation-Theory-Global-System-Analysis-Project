"""
TFT系统核心模块

基于36D拓扑波动理论的核心功能实现
"""

import numpy as np
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core_framework.tft_core.operators import (
    topological_invariant_calculator as calculate_topological_invariant,
    homology_group_approximation as approximate_homology_group,
    data_normalization as normalize_topological_data,
    topological_similarity as calculate_topological_similarity,
    homologous_resonance_calculator as calculate_homologous_resonance,
    topological_evolution_operator
)
from core_framework.tft_core.equations import (
    topological_evolution_equation,
    stability_equation as topological_stability_equation,
    homology_equation,
    resonance_equation,
    optimization_equation as topological_optimization_equation,
    topological_closure_equation
)
from core_framework.tft_core.axioms import (
    check_topological_closure as validate_topological_closure,
    check_system_stability as validate_system_stability,
    check_evolution_path_validity as validate_evolution_path_validity
)
from core_framework.system_modeling.global_system import GlobalSystem
from core_framework.system_modeling.sovereign_node import SovereignNode
from core_framework.system_modeling.evolution_paths import EvolutionPaths

class TFTSystem:
    """
    TFT系统类
    
    基于36D拓扑波动理论的完整系统实现
    """
    
    def __init__(self, config=None):
        """
        初始化TFT系统
        
        参数:
            config: 配置字典
        """
        self.config = config or {
            "initial_energy": 100.0,
            "dimension": 36,
            "evolution_rate": 0.01,
            "stability_threshold": 0.5,
            "resonance_threshold": 0.7,
            "max_nodes": 100
        }
        self.global_system = GlobalSystem()
        # 添加energy属性，以便测试中使用
        self.global_system.energy = self.config["initial_energy"]
        self.evolution_paths = EvolutionPaths()
        self.evolution_history = []
        self.current_step = 0
    
    def add_node(self, node_data):
        """
        添加节点到系统
        
        参数:
            node_data: 节点数据字典
        
        返回:
            SovereignNode: 添加的节点
        """
        if len(self.global_system.nodes.values()) >= self.config["max_nodes"]:
            raise ValueError(f"系统节点数已达到上限: {self.config['max_nodes']}")
        
        # 转换参数为SovereignNode构造函数需要的格式
        node_id = node_data.get("name", f"node_{len(self.global_system.nodes.values())}")
        node_name = node_data.get("name", f"Node_{len(self.global_system.nodes.values())}")
        
        # 映射测试参数到SovereignNode需要的参数
        survival_metric = node_data.get("stability", 0.5)
        security_metric = node_data.get("stability", 0.5)
        linear_metric = node_data.get("influence", 0.5)
        performance_metric = node_data.get("innovation", 0.5)
        
        # 创建节点
        node = SovereignNode(
            node_id=node_id,
            node_name=node_name,
            survival_metric=survival_metric,
            security_metric=security_metric,
            linear_metric=linear_metric,
            performance_metric=performance_metric
        )
        
        # 添加额外属性，以便测试中使用
        node.node_name = node_name
        node.stability = node_data.get("stability", 0.5)
        node.influence = node_data.get("influence", 0.5)
        node.resilience = node_data.get("resilience", 0.5)
        node.innovation = node_data.get("innovation", 0.5)
        
        self.global_system.add_node(node)
        return node
    
    def remove_node(self, node_name):
        """
        从系统中移除节点
        
        参数:
            node_name: 节点名称
        
        返回:
            bool: 是否移除成功
        """
        for i, node in enumerate(self.global_system.nodes.values()):
            if node.node_name == node_name:
                self.global_system.nodes.values().pop(i)
                return True
        return False
    
    def get_node(self, node_name):
        """
        获取系统中的节点
        
        参数:
            node_name: 节点名称
        
        返回:
            SovereignNode: 找到的节点
        """
        for node in self.global_system.nodes.values():
            if node.node_name == node_name:
                return node
        return None
    
    def evolve(self, steps=1):
        """
        系统演化
        
        参数:
            steps: 演化步数
        
        返回:
            list: 演化历史
        """
        for _ in range(steps):
            # 记录当前状态
            current_state = {
                "step": self.current_step,
                "energy": self.global_system.energy,
                "nodes": [
                    {
                        "name": node.node_name,
                        "power": node.calculate_power(),
                        "stability": node.stability,
                        "influence": node.influence,
                        "resilience": node.resilience,
                        "innovation": node.innovation
                    }
                    for node in self.global_system.nodes.values()
                ],
                "system_properties": {
                    "average_power": self.global_system.get_average_power(),
                    "average_stability": self.global_system.get_average_stability(),
                    "system_resilience": self.global_system.calculate_resilience(),
                    "system_innovation": self.global_system.calculate_innovation(),
                    "topological_entropy": self.global_system.calculate_topological_entropy()
                }
            }
            self.evolution_history.append(current_state)
            
            # 执行演化操作
            self.global_system.evolve()
            
            # 应用拓扑波动理论的演化算子
            for node in self.global_system.nodes.values():
                # 计算节点的拓扑不变量
                node_topology = np.array([
                    node.calculate_power(),
                    node.stability,
                    node.influence,
                    node.resilience,
                    node.innovation
                ])
                
                # 计算拓扑演化
                evolved_topology = topological_evolution_operator(node_topology, np.eye(len(node_topology)), {})
                
                # 更新节点属性
                node.metrics["survival"] = max(0, min(1, evolved_topology[0]))
                node.metrics["security"] = max(0, min(1, evolved_topology[1]))
                node.metrics["linear"] = max(0, min(1, evolved_topology[2]))
                node.metrics["performance"] = max(0, min(1, evolved_topology[3]))
                node.innovation = max(0, min(1, evolved_topology[4]))
            
            # 更新系统能量
            self.global_system.energy *= (1 + self.config["evolution_rate"])
            self.current_step += 1
        
        return self.evolution_history
    
    def analyze_system(self):
        """
        分析系统状态
        
        返回:
            dict: 系统分析结果
        """
        # 计算系统拓扑属性
        system_properties = {
            "total_nodes": len(self.global_system.nodes.values()),
            "total_energy": self.global_system.energy,
            "average_power": self.global_system.get_average_power(),
            "average_stability": self.global_system.get_average_stability(),
            "system_resilience": self.global_system.calculate_resilience(),
            "system_innovation": self.global_system.calculate_innovation(),
            "topological_entropy": self.global_system.calculate_topological_entropy()
        }
        
        # 分析每个节点
        node_analyses = []
        for node in self.global_system.nodes.values():
            node_topology = np.array([
                node.calculate_power(),
                node.stability,
                node.influence,
                node.resilience,
                node.innovation
            ])
            
            node_analysis = {
                "name": node.node_name,
                "power": node.calculate_power(),
                "stability": node.stability,
                "influence": node.influence,
                "resilience": node.resilience,
                "innovation": node.innovation,
                "topological_invariant": calculate_topological_invariant(node_topology),
                "homology_group": approximate_homology_group(node_topology),
                "node_metrics": node.calculate_node_metrics(),
                "power_index": node.calculate_power_index()
            }
            node_analyses.append(node_analysis)
        
        # 分析系统演化路径
        evolution_analyses = {
            "trump_path": self.evolution_paths.analyze_trump_path(self.global_system),
            "multilateral_path": self.evolution_paths.analyze_multilateral_path(self.global_system),
            "homologous_path": self.evolution_paths.analyze_homologous_path(self.global_system)
        }
        
        # 验证系统稳定性
        stability_validation = validate_system_stability(self.global_system)
        
        # 综合分析结果
        analysis_result = {
            "system_properties": system_properties,
            "node_analyses": node_analyses,
            "evolution_analyses": evolution_analyses,
            "stability_validation": stability_validation,
            "current_step": self.current_step,
            "evolution_history_length": len(self.evolution_history)
        }
        
        return analysis_result
    
    def optimize_system(self, iterations=100):
        """
        优化系统
        
        参数:
            iterations: 优化迭代次数
        
        返回:
            dict: 优化结果
        """
        optimization_history = []
        
        for i in range(iterations):
            # 分析当前系统
            current_analysis = self.analyze_system()
            
            # 计算优化目标函数
            objective_value = (
                current_analysis["system_properties"]["system_resilience"] * 0.4 +
                current_analysis["system_properties"]["system_innovation"] * 0.3 +
                current_analysis["system_properties"]["average_stability"] * 0.3
            )
            
            optimization_history.append({
                "iteration": i,
                "objective_value": objective_value,
                "system_resilience": current_analysis["system_properties"]["system_resilience"],
                "system_innovation": current_analysis["system_properties"]["system_innovation"],
                "average_stability": current_analysis["system_properties"]["average_stability"]
            })
            
            # 应用拓扑优化方程
            for node in self.global_system.nodes.values():
                node_topology = np.array([
                    node.calculate_power(),
                    node.stability,
                    node.influence,
                    node.resilience,
                    node.innovation
                ])
                
                # 计算优化后的拓扑
                optimized_topology = topological_optimization_equation(node_topology)
                
                # 更新节点属性
                node.metrics["survival"] = max(0, min(1, optimized_topology[0]))
                node.metrics["security"] = max(0, min(1, optimized_topology[1]))
                node.metrics["linear"] = max(0, min(1, optimized_topology[2]))
                node.metrics["performance"] = max(0, min(1, optimized_topology[3]))
            
            # 执行一次演化
            self.evolve(1)
        
        # 最终分析
        final_analysis = self.analyze_system()
        final_objective = (
            final_analysis["system_properties"]["system_resilience"] * 0.4 +
            final_analysis["system_properties"]["system_innovation"] * 0.3 +
            final_analysis["system_properties"]["average_stability"] * 0.3
        )
        
        optimization_result = {
            "initial_objective": optimization_history[0]["objective_value"] if optimization_history else 0,
            "final_objective": final_objective,
            "improvement": final_objective - (optimization_history[0]["objective_value"] if optimization_history else 0),
            "optimization_history": optimization_history,
            "final_analysis": final_analysis
        }
        
        return optimization_result
    
    def calculate_system_resonance(self):
        """
        计算系统共振
        
        返回:
            dict: 共振分析结果
        """
        if len(self.global_system.nodes.values()) < 2:
            return {
                "resonance_possible": False,
                "message": "系统节点数不足，无法计算共振"
            }
        
        resonances = []
        total_resonance = 0
        
        # 计算所有节点对之间的共振
        for i, node1 in enumerate(self.global_system.nodes.values()):
            for j, node2 in enumerate(self.global_system.nodes.values()):
                if i < j:
                    node1_topology = np.array([
                        node1.power,
                        node1.stability,
                        node1.influence,
                        node1.resilience,
                        node1.innovation
                    ])
                    
                    node2_topology = np.array([
                        node2.power,
                        node2.stability,
                        node2.influence,
                        node2.resilience,
                        node2.innovation
                    ])
                    
                    # 计算同源共振
                    resonance_value = calculate_homologous_resonance(node1_topology, node2_topology)
                    resonances.append({
                        "node1": node1.name,
                        "node2": node2.name,
                        "resonance_value": resonance_value
                    })
                    total_resonance += resonance_value
        
        average_resonance = total_resonance / len(resonances) if resonances else 0
        
        resonance_analysis = {
            "resonance_possible": True,
            "total_resonance": total_resonance,
            "average_resonance": average_resonance,
            "node_resonances": resonances,
            "resonance_threshold": 0.7,
            "high_resonance_pairs": [r for r in resonances if r["resonance_value"] > 0.7]
        }
        
        return resonance_analysis
    
    def save_system_state(self, file_path):
        """
        保存系统状态
        
        参数:
            file_path: 保存路径
        """
        import json
        
        system_state = {
            "config": self.config,
            "current_step": self.current_step,
            "energy": self.global_system.energy,
            "nodes": [
                {
                    "name": node.node_name,
                    "power": node.calculate_power(),
                    "stability": node.stability,
                    "influence": node.influence,
                    "resilience": node.resilience,
                    "innovation": node.innovation
                }
                for node in self.global_system.nodes.values()
            ],
            "evolution_history": self.evolution_history
        }
        
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(system_state, f, ensure_ascii=False, indent=2)
    
    def load_system_state(self, file_path):
        """
        加载系统状态
        
        参数:
            file_path: 加载路径
        """
        import json
        
        with open(file_path, 'r', encoding='utf-8') as f:
            system_state = json.load(f)
        
        # 恢复配置
        self.config = system_state.get("config", self.config)
        self.current_step = system_state.get("current_step", 0)
        
        # 恢复能量
        self.global_system.energy = system_state.get("energy", self.config["initial_energy"])
        
        # 清空现有节点
        self.global_system.nodes.values().clear()
        
        # 恢复节点
        for node_data in system_state.get("nodes", []):
            self.add_node(node_data)
        
        # 恢复演化历史
        self.evolution_history = system_state.get("evolution_history", [])

class EvolutionAnalyzer:
    """
    演化分析器类
    
    基于36D拓扑波动理论的演化分析功能
    """
    
    def __init__(self, tft_system=None):
        """
        初始化演化分析器
        
        参数:
            tft_system: TFT系统实例
        """
        self.tft_system = tft_system or TFTSystem()
        self.evolution_paths = EvolutionPaths()
    
    def analyze_evolution_paths(self):
        """
        分析演化路径
        
        返回:
            dict: 演化路径分析结果
        """
        # 分析所有演化路径
        path_analyses = {
            "trump_path": self.evolution_paths.analyze_trump_path(self.tft_system.global_system),
            "multilateral_path": self.evolution_paths.analyze_multilateral_path(self.tft_system.global_system),
            "homologous_path": self.evolution_paths.analyze_homologous_path(self.tft_system.global_system)
        }
        
        # 评估每个路径
        path_evaluations = {}
        for path_name, path_analysis in path_analyses.items():
            # 计算路径评分
            score = (
                path_analysis.get("stability", 0.5) * 0.4 +
                path_analysis.get("innovation", 0.5) * 0.3 +
                path_analysis.get("resilience", 0.5) * 0.3
            )
            
            # 验证路径有效性
            validity = validate_evolution_path_validity(path_name, self.tft_system.global_system)
            
            path_evaluations[path_name] = {
                "score": score,
                "validity": validity,
                "analysis": path_analysis
            }
        
        # 选择最佳路径
        best_path = max(path_evaluations, key=lambda x: path_evaluations[x]["score"])
        
        analysis_result = {
            "path_analyses": path_analyses,
            "path_evaluations": path_evaluations,
            "best_path": best_path,
            "best_path_score": path_evaluations[best_path]["score"],
            "best_path_validity": path_evaluations[best_path]["validity"]
        }
        
        return analysis_result
    
    def simulate_evolution_paths(self, steps=100):
        """
        模拟演化路径
        
        参数:
            steps: 演化步数
        
        返回:
            dict: 模拟结果
        """
        simulation_results = {}
        
        # 保存原始系统状态
        original_state = {
            "current_step": self.tft_system.current_step,
            "energy": self.tft_system.global_system.energy,
            "nodes": [
                {
                    "name": node.node_name,
                    "power": node.calculate_power(),
                    "stability": node.stability,
                    "influence": node.influence,
                    "resilience": node.resilience,
                    "innovation": node.innovation
                }
                for node in self.tft_system.global_system.nodes.values()
            ],
            "evolution_history": self.tft_system.evolution_history.copy()
        }
        
        # 模拟特朗普路径
        print("模拟特朗普路径...")
        self._reset_system_state(original_state)
        for _ in range(steps):
            # 应用特朗普路径的演化规则
            for node in self.tft_system.global_system.nodes.values():
                # 特朗普路径：强化核心节点，削弱边缘节点
                if node.calculate_power() > 0.7:
                    # 强化核心节点
                    for metric in node.metrics:
                        node.metrics[metric] *= 1.05
                    node.influence *= 1.05
                else:
                    # 削弱边缘节点
                    for metric in node.metrics:
                        node.metrics[metric] *= 0.95
                    node.influence *= 0.95
            self.tft_system.evolve(1)
        simulation_results["trump_path"] = self.tft_system.analyze_system()
        
        # 模拟多边主义路径
        print("模拟多边主义路径...")
        self._reset_system_state(original_state)
        for _ in range(steps):
            # 应用多边主义路径的演化规则
            average_power = self.tft_system.global_system.get_average_power()
            for node in self.tft_system.global_system.nodes.values():
                # 多边主义路径：平衡节点权力
                if abs(node.calculate_power() - average_power) > 0.1:
                    if node.calculate_power() > average_power:
                        # 降低节点实力
                        for metric in node.metrics:
                            node.metrics[metric] *= 0.98
                    else:
                        # 提升节点实力
                        for metric in node.metrics:
                            node.metrics[metric] *= 1.02
            self.tft_system.evolve(1)
        simulation_results["multilateral_path"] = self.tft_system.analyze_system()
        
        # 模拟同源共生路径
        print("模拟同源共生路径...")
        self._reset_system_state(original_state)
        for _ in range(steps):
            # 应用同源共生路径的演化规则
            for node in self.tft_system.global_system.nodes.values():
                # 同源共生路径：增强节点间的协同性
                node.resilience *= 1.01
                node.innovation *= 1.01
                node.stability = (node.stability + 0.5) / 2  # 向中间值靠拢
            self.tft_system.evolve(1)
        simulation_results["homologous_path"] = self.tft_system.analyze_system()
        
        # 恢复原始系统状态
        self._reset_system_state(original_state)
        
        # 比较模拟结果
        path_comparison = {}
        for path_name, result in simulation_results.items():
            path_comparison[path_name] = {
                "final_system_resilience": result["system_properties"]["system_resilience"],
                "final_system_innovation": result["system_properties"]["system_innovation"],
                "final_average_stability": result["system_properties"]["average_stability"],
                "final_topological_entropy": result["system_properties"]["topological_entropy"]
            }
        
        simulation_result = {
            "path_simulation_results": simulation_results,
            "path_comparison": path_comparison,
            "simulation_steps": steps
        }
        
        return simulation_result
    
    def _reset_system_state(self, state):
        """
        重置系统状态
        
        参数:
            state: 系统状态字典
        """
        self.tft_system.current_step = state["current_step"]
        self.tft_system.global_system.energy = state["energy"]
        
        # 重置节点
        # 修复: 函数调用不能用于赋值操作 - 原始代码: # 修复: 函数调用不能用于赋值操作 - 原始代码: self.tft_system.global_system.nodes.values() = {}
        for node_data in state["nodes"]:
            self.tft_system.add_node(node_data)
        
        # 重置演化历史
        self.tft_system.evolution_history = state["evolution_history"].copy()
