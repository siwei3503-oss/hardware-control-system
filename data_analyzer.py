"""
硬件数据分析模块 - 收集和分析硬件运行数据
Hardware Data Analysis - Collect and analyze hardware data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from datetime import datetime
import csv

class HardwareDataAnalyzer:
    """硬件数据分析器"""
    
    def __init__(self):
        """初始化数据分析器"""
        self.data = []
        self.df = None
        print("[数据分析器] 已初始化")
    
    def add_data(self, timestamp, device_name, metric_name, value):
        """
        添加数据点
        timestamp: 时间戳
        device_name: 设备名称
        metric_name: 指标名称
        value: 指标值
        """
        self.data.append({
            'timestamp': timestamp,
            'device': device_name,
            'metric': metric_name,
            'value': value
        })
    
    def create_dataframe(self):
        """创建数据框"""
        self.df = pd.DataFrame(self.data)
        if len(self.df) > 0:
            self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        print(f"[数据分析] 数据框已创建: {len(self.df)} 行")
        return self.df
    
    def get_statistics(self):
        """获取统计信息"""
        if self.df is None:
            self.create_dataframe()
        
        print("\n=== 数据统计 ===")
        print(self.df.describe())
        return self.df.describe()
    
    def filter_by_device(self, device_name):
        """按设备筛选数据"""
        if self.df is None:
            self.create_dataframe()
        return self.df[self.df['device'] == device_name]
    
    def filter_by_metric(self, metric_name):
        """按指标筛选数据"""
        if self.df is None:
            self.create_dataframe()
        return self.df[self.df['metric'] == metric_name]
    
    def plot_metric_trend(self, device_name, metric_name, title=None):
        """绘制指标趋势图"""
        filtered_data = self.df[(self.df['device'] == device_name) & 
                               (self.df['metric'] == metric_name)]
        
        if len(filtered_data) == 0:
            print(f"[错误] 找不到 {device_name} 的 {metric_name} 数据")
            return
        
        plt.figure(figsize=(12, 6))
        plt.plot(filtered_data['timestamp'], filtered_data['value'], 'b-', linewidth=2)
        plt.xlabel('时间')
        plt.ylabel(metric_name)
        plt.title(title or f"{device_name} - {metric_name} 趋势")
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    def save_to_csv(self, filename):
        """保存数据到CSV"""
        if self.df is None:
            self.create_dataframe()
        self.df.to_csv(filename, index=False)
        print(f"[数据分析] 数据已保存到 {filename}")
    
    def save_to_json(self, filename):
        """保存数据到JSON"""
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=2, default=str)
        print(f"[数据分析] 数据已保存到 {filename}")


class PowerAnalyzer:
    """电源功耗分析"""
    
    def __init__(self):
        self.power_data = []
    
    def add_power_reading(self, timestamp, device, voltage, current):
        """添加电源读数"""
        power = voltage * current
        self.power_data.append({
            'timestamp': timestamp,
            'device': device,
            'voltage': voltage,
            'current': current,
            'power': power
        })
    
    def analyze_power_consumption(self):
        """分析功耗"""
        df = pd.DataFrame(self.power_data)
        
        print("\n=== 功耗分析 ===")
        print(f"平均功耗: {df['power'].mean():.2f} W")
        print(f"最大功耗: {df['power'].max():.2f} W")
        print(f"最小功耗: {df['power'].min():.2f} W")
        print(f"功耗标准差: {df['power'].std():.2f} W")
        
        return df['power'].describe()
    
    def calculate_energy_consumption(self, duration_hours):
        """计算能耗"""
        avg_power = pd.DataFrame(self.power_data)['power'].mean()
        energy = avg_power * duration_hours  # 瓦时
        print(f"[能耗] {duration_hours}小时的能耗: {energy:.2f} Wh")
        return energy


class TemperatureAnalyzer:
    """温度分析"""
    
    def __init__(self):
        self.temp_data = []
    
    def add_temperature_reading(self, timestamp, device, temperature):
        """添加温度读数"""
        self.temp_data.append({
            'timestamp': timestamp,
            'device': device,
            'temperature': temperature
        })
    
    def analyze_temperature(self):
        """分析温度"""
        df = pd.DataFrame(self.temp_data)
        
        print("\n=== 温度分析 ===")
        print(f"平均温度: {df['temperature'].mean():.2f} °C")
        print(f"最高温度: {df['temperature'].max():.2f} °C")
        print(f"最低温度: {df['temperature'].min():.2f} °C")
        print(f"温度标准差: {df['temperature'].std():.2f} °C")
        
        return df['temperature'].describe()
    
    def check_thermal_warnings(self, warning_threshold=80, critical_threshold=90):
        """检查温度告警"""
        df = pd.DataFrame(self.temp_data)
        
        warnings = (df['temperature'] > warning_threshold).sum()
        critical = (df['temperature'] > critical_threshold).sum()
        
        print(f"\n[告警] 温度超过 {warning_threshold}°C: {warnings} 次")
        print(f"[严重] 温度超过 {critical_threshold}°C: {critical} 次")
        
        return warnings, critical


class PerformanceAnalyzer:
    """性能分析"""
    
    def __init__(self):
        self.performance_data = []
    
    def add_performance_metric(self, timestamp, device, metric_name, value):
        """添加性能指标"""
        self.performance_data.append({
            'timestamp': timestamp,
            'device': device,
            'metric': metric_name,
            'value': value
        })
    
    def analyze_performance(self, metric_name):
        """分析性能指标"""
        df = pd.DataFrame(self.performance_data)
        filtered = df[df['metric'] == metric_name]
        
        if len(filtered) == 0:
            print(f"[错误] 找不到 {metric_name} 指标数据")
            return None
        
        print(f"\n=== {metric_name} 分析 ===")
        print(f"平均值: {filtered['value'].mean():.2f}")
        print(f"最大值: {filtered['value'].max():.2f}")
        print(f"最小值: {filtered['value'].min():.2f}")
        
        return filtered['value'].describe()
    
    def compare_devices(self, metric_name):
        """比较设备性能"""
        df = pd.DataFrame(self.performance_data)
        filtered = df[df['metric'] == metric_name]
        
        comparison = filtered.groupby('device')['value'].agg(['mean', 'max', 'min', 'std'])
        print(f"\n=== {metric_name} 设备对比 ===")
        print(comparison)
        
        return comparison


class ReliabilityAnalyzer:
    """可靠性分析"""
    
    def __init__(self):
        self.error_log = []
        self.uptime_data = []
    
    def log_error(self, timestamp, device, error_message):
        """记录错误"""
        self.error_log.append({
            'timestamp': timestamp,
            'device': device,
            'error': error_message
        })
        print(f"[错误日志] {device}: {error_message}")
    
    def add_uptime_record(self, timestamp, device, status):
        """添加运行状态记录"""
        self.uptime_data.append({
            'timestamp': timestamp,
            'device': device,
            'status': status  # 'running' 或 'failed'
        })
    
    def calculate_uptime(self, device_name):
        """计算设备运行时间"""
        df = pd.DataFrame(self.uptime_data)
        device_data = df[df['device'] == device_name]
        
        running_time = (device_data['status'] == 'running').sum()
        total_time = len(device_data)
        
        uptime_percentage = (running_time / total_time * 100) if total_time > 0 else 0
        
        print(f"\n[可靠性] {device_name} 运行时间: {uptime_percentage:.2f}%")
        return uptime_percentage
    
    def get_error_summary(self):
        """获取错误摘要"""
        df = pd.DataFrame(self.error_log)
        
        print("\n=== 错误摘要 ===")
        print(f"总错误数: {len(df)}")
        
        if len(df) > 0:
            error_count = df.groupby('device').size()
            print("\n各设备错误数:")
            print(error_count)
        
        return df


class RealTimeMonitor:
    """实时监控系统"""
    
    def __init__(self, system):
        """
        初始化实时监控
        system: 硬件控制系统实例
        """
        self.system = system
        self.analyzer = HardwareDataAnalyzer()
        self.power_analyzer = PowerAnalyzer()
        self.temp_analyzer = TemperatureAnalyzer()
        self.performance_analyzer = PerformanceAnalyzer()
        self.reliability_analyzer = ReliabilityAnalyzer()
    
    def collect_metrics(self, device_name, metrics_dict):
        """
        收集设备指标
        device_name: 设备名称
        metrics_dict: 指标字典 {'metric_name': value, ...}
        """
        timestamp = datetime.now()
        
        for metric_name, value in metrics_dict.items():
            self.analyzer.add_data(timestamp, device_name, metric_name, value)
            
            # 分别添加到专用分析器
            if 'power' in metric_name.lower():
                if 'voltage' in metrics_dict and 'current' in metrics_dict:
                    self.power_analyzer.add_power_reading(
                        timestamp, device_name,
                        metrics_dict['voltage'],
                        metrics_dict['current']
                    )
            
            elif 'temp' in metric_name.lower():
                self.temp_analyzer.add_temperature_reading(timestamp, device_name, value)
            
            else:
                self.performance_analyzer.add_performance_metric(
                    timestamp, device_name, metric_name, value
                )
    
    def generate_report(self):
        """生成完整报告"""
        print("\n" + "="*60)
        print("硬件系统监控报告")
        print("="*60)
        
        self.analyzer.get_statistics()
        self.power_analyzer.analyze_power_consumption()
        self.temp_analyzer.analyze_temperature()
        self.reliability_analyzer.get_error_summary()
        
        print("="*60 + "\n")
    
    def export_all_data(self, prefix="hardware_report"):
        """导出所有数据"""
        self.analyzer.save_to_csv(f"{prefix}_all.csv")
        self.analyzer.save_to_json(f"{prefix}_all.json")
        print(f"[监控] 数据已导出")


# 示例使用
if __name__ == "__main__":
    # 创建分析器
    analyzer = HardwareDataAnalyzer()
    power_analyzer = PowerAnalyzer()
    temp_analyzer = TemperatureAnalyzer()
    performance_analyzer = PerformanceAnalyzer()
    reliability_analyzer = ReliabilityAnalyzer()
    
    # 模拟数据收集
    import random
    
    print("=== 模拟数据收集 ===\n")
    
    for i in range(100):
        timestamp = datetime.now()
        
        # 收集LED数据
        analyzer.add_data(timestamp, "LED", "brightness", random.randint(0, 100))
        
        # 收集马达数据
        analyzer.add_data(timestamp, "Motor", "speed", random.randint(0, 100))
        performance_analyzer.add_performance_metric(timestamp, "Motor", "RPM", random.uniform(0, 3000))
        
        # 收集温度数据
        temp = 35 + random.gauss(0, 5)
        temp_analyzer.add_temperature_reading(timestamp, "CPU", temp)
        analyzer.add_data(timestamp, "CPU", "temperature", temp)
        
        # 收集功耗数据
        voltage = 12 + random.gauss(0, 0.5)
        current = 2 + random.gauss(0, 0.2)
        power_analyzer.add_power_reading(timestamp, "System", voltage, current)
        analyzer.add_data(timestamp, "System", "power", voltage * current)
    
    # 分析数据
    print("\n>>> 数据统计")
    analyzer.get_statistics()
    
    print("\n>>> 功耗分析")
    power_analyzer.analyze_power_consumption()
    
    print("\n>>> 温度分析")
    temp_analyzer.analyze_temperature()
    temp_analyzer.check_thermal_warnings()
    
    print("\n>>> 性能分析")
    performance_analyzer.analyze_performance("RPM")
    performance_analyzer.compare_devices("speed")
    
    # 导出数据
    analyzer.save_to_csv("hardware_data.csv")
    analyzer.save_to_json("hardware_data.json")
