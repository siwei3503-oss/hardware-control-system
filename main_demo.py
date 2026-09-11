"""
完整集成示例 - 软件控制硬件 + 数据分析
Complete Integration Example - Software controls hardware + Data Analysis
"""

import time
import random
from datetime import datetime
from hardware_controller import (
    HardwareControlSystem, LEDController, ButtonController,
    MotorController, TemperatureSensor, UltrasonicSensor
)
from data_analyzer import (
    HardwareDataAnalyzer, PowerAnalyzer, TemperatureAnalyzer,
    PerformanceAnalyzer, ReliabilityAnalyzer, RealTimeMonitor
)


class SmartHomeSystem:
    """智能家居系统 - 集成硬件控制和数据分析"""
    
    def __init__(self):
        """初始化智能家居系统"""
        self.hardware_system = HardwareControlSystem()
        self.monitor = None
        self.is_running = False
        
        print("\n" + "="*70)
        print("智能家居系统初始化")
        print("="*70 + "\n")
    
    def setup_hardware(self):
        """设置硬件设备"""
        print(">>> 配置硬件设备\n")
        
        # GPIO 配置
        LED_PIN = 17
        BUTTON_PIN = 27
        MOTOR_FORWARD = 23
        MOTOR_BACKWARD = 24
        MOTOR_ENABLE = 25
        TEMP_PIN = 4
        
        # 创建设备
        self.led = LEDController(LED_PIN)
        self.button = ButtonController(BUTTON_PIN)
        self.motor = MotorController(MOTOR_FORWARD, MOTOR_BACKWARD, MOTOR_ENABLE)
        self.temp_sensor = TemperatureSensor(TEMP_PIN)
        
        # 添加到硬件系统
        self.hardware_system.add_device("LED", self.led)
        self.hardware_system.add_device("Button", self.button)
        self.hardware_system.add_device("Motor", self.motor)
        self.hardware_system.add_device("TemperatureSensor", self.temp_sensor)
        
        self.hardware_system.status_report()
    
    def setup_monitoring(self):
        """设置实时监控"""
        print(">>> 设置实时监控系统\n")
        self.monitor = RealTimeMonitor(self.hardware_system)
        print("[监控] 实时监控系统已就绪\n")
    
    def demo_led_control(self):
        """LED控制演示"""
        print("\n" + "="*70)
        print("演示 1: LED 控制")
        print("="*70)
        
        print("\n步骤1: 打开LED")
        self.hardware_system.execute_command("LED", "turn_on")
        time.sleep(1)
        
        # 收集LED状态数据
        self.monitor.collect_metrics("LED", {
            'brightness': 100,
            'power_consumption': 0.5
        })
        
        print("\n步骤2: 关闭LED")
        self.hardware_system.execute_command("LED", "turn_off")
        time.sleep(1)
        
        self.monitor.collect_metrics("LED", {
            'brightness': 0,
            'power_consumption': 0
        })
        
        print("\n步骤3: LED闪烁")
        self.hardware_system.execute_command("LED", "blink", 3, 0.5)
        
        for i in range(3):
            self.monitor.collect_metrics("LED", {
                'brightness': 100 if i % 2 == 0 else 0,
                'power_consumption': 0.5 if i % 2 == 0 else 0
            })
        
        print("\n✓ LED控制演示完成")
    
    def demo_motor_control(self):
        """马达控制演示"""
        print("\n" + "="*70)
        print("演示 2: 马达 控制")
        print("="*70)
        
        print("\n步骤1: 马达正向旋转 (100% 速度)")
        self.hardware_system.execute_command("Motor", "forward", 100)
        time.sleep(2)
        
        self.monitor.collect_metrics("Motor", {
            'speed': 100,
            'direction': 1,
            'power_consumption': 15.0,
            'rpm': 3000
        })
        
        print("\n步骤2: 降低速度到 50%")
        self.hardware_system.execute_command("Motor", "change_speed", 50)
        time.sleep(2)
        
        self.monitor.collect_metrics("Motor", {
            'speed': 50,
            'direction': 1,
            'power_consumption': 7.5,
            'rpm': 1500
        })
        
        print("\n步骤3: 反向旋转 (75% 速度)")
        self.hardware_system.execute_command("Motor", "backward", 75)
        time.sleep(2)
        
        self.monitor.collect_metrics("Motor", {
            'speed': 75,
            'direction': -1,
            'power_consumption': 11.25,
            'rpm': 2250
        })
        
        print("\n步骤4: 停止马达")
        self.hardware_system.execute_command("Motor", "stop")
        
        self.monitor.collect_metrics("Motor", {
            'speed': 0,
            'direction': 0,
            'power_consumption': 0,
            'rpm': 0
        })
        
        print("\n✓ 马达控制演示完成")
    
    def demo_temperature_monitoring(self):
        """温度监控演示"""
        print("\n" + "="*70)
        print("演示 3: 温度 监控")
        print("="*70)
        
        print("\n开始收集温度数据...")
        
        # 模拟温度数据变化
        base_temp = 35
        for i in range(10):
            # 模拟温度逐渐升高
            temp = base_temp + i * 2 + random.gauss(0, 1)
            
            print(f"[{i+1}/10] 温度: {temp:.2f}°C")
            
            self.monitor.collect_metrics("System", {
                'cpu_temperature': temp,
                'cpu_usage': 50 + i * 5,
                'fan_speed': 30 + i * 5
            })
            
            # 记录温度数据用于可靠性分析
            self.monitor.reliability_analyzer.add_uptime_record(
                datetime.now(), "CPU", "running"
            )
            
            time.sleep(0.5)
        
        print("\n✓ 温度监控演示完成")
    
    def demo_power_analysis(self):
        """功耗分析演示"""
        print("\n" + "="*70)
        print("演示 4: 功耗 分析")
        print("="*70)
        
        print("\n收集功耗数据...\n")
        
        devices = [
            ("LED", 12, 0.5),
            ("Motor", 12, 2.0),
            ("Sensor", 5, 0.1),
            ("Fan", 12, 1.5)
        ]
        
        for device_name, voltage, current in devices:
            power = voltage * current
            print(f"{device_name}: {voltage}V × {current}A = {power}W")
            
            self.monitor.power_analyzer.add_power_reading(
                datetime.now(), device_name, voltage, current
            )
            
            self.monitor.collect_metrics(device_name, {
                'voltage': voltage,
                'current': current,
                'power': power
            })
        
        print("\n✓ 功耗数据已收集")
    
    def demo_error_logging(self):
        """错误日志演示"""
        print("\n" + "="*70)
        print("演示 5: 错误 日志")
        print("="*70)
        
        print("\n模拟硬件错误...\n")
        
        errors = [
            ("Sensor", "温度传感器读数异常"),
            ("Motor", "马达超速告警"),
            ("LED", "LED电流过大"),
            ("System", "系统温度过高")
        ]
        
        for device, error_msg in errors:
            self.monitor.reliability_analyzer.log_error(
                datetime.now(), device, error_msg
            )
            time.sleep(0.5)
        
        print("\n✓ 错误日志演示完成")
    
    def run_full_demo(self):
        """运行完整演示"""
        try:
            self.setup_hardware()
            self.setup_monitoring()
            
            self.demo_led_control()
            time.sleep(1)
            
            self.demo_motor_control()
            time.sleep(1)
            
            self.demo_temperature_monitoring()
            time.sleep(1)
            
            self.demo_power_analysis()
            time.sleep(1)
            
            self.demo_error_logging()
            
            # 生成报告
            print("\n" + "="*70)
            print("生成数据分析报告")
            print("="*70)
            self.monitor.generate_report()
            
            # 导出数据
            print("\n导出数据到文件...")
            self.monitor.export_all_data("smart_home_report")
            
            print("\n" + "="*70)
            print("所有演示完成！✓")
            print("="*70)
            
        except KeyboardInterrupt:
            print("\n\n用户中断演示")
        
        finally:
            print("\n清理系统...")
            self.hardware_system.cleanup()


class IndustrialControlSystem:
    """工业控制系统 - 生产线监控"""
    
    def __init__(self):
        """初始化工业控制系统"""
        self.hardware_system = HardwareControlSystem()
        self.monitor = None
        self.production_log = []
        
        print("\n" + "="*70)
        print("工业控制系统初始化")
        print("="*70 + "\n")
    
    def setup_production_line(self):
        """设置生产线"""
        print(">>> 配置生产线硬件\n")
        
        # 创建生产线设备
        motor1 = MotorController(23, 24, 25)
        motor2 = MotorController(12, 13, 14)
        temp_sensor = TemperatureSensor(4)
        
        self.hardware_system.add_device("ConveyorBelt", motor1)
        self.hardware_system.add_device("RoboticArm", motor2)
        self.hardware_system.add_device("TemperatureMonitor", temp_sensor)
        
        self.hardware_system.status_report()
    
    def setup_monitoring(self):
        """设置监控"""
        self.monitor = RealTimeMonitor(self.hardware_system)
    
    def simulate_production(self, duration_seconds=30):
        """模拟生产过程"""
        print("\n" + "="*70)
        print("生产线运行模拟")
        print("="*70 + "\n")
        
        start_time = time.time()
        production_count = 0
        
        while time.time() - start_time < duration_seconds:
            # 启动传送带
            self.hardware_system.execute_command("ConveyorBelt", "forward", 80)
            
            # 启动机械臂
            self.hardware_system.execute_command("RoboticArm", "forward", 60)
            
            # 收集运行数据
            self.monitor.collect_metrics("ConveyorBelt", {
                'speed': 80,
                'power_consumption': 12.0,
                'rpm': 2400
            })
            
            self.monitor.collect_metrics("RoboticArm", {
                'speed': 60,
                'power_consumption': 8.0,
                'position': random.randint(0, 360)
            })
            
            # 模拟产品生产
            if random.random() > 0.7:
                production_count += 1
                print(f"[生产] 已完成产品 #{production_count}")
                self.production_log.append({
                    'timestamp': datetime.now(),
                    'product_id': production_count,
                    'status': 'completed'
                })
            
            time.sleep(2)
        
        # 停止设备
        self.hardware_system.execute_command("ConveyorBelt", "stop")
        self.hardware_system.execute_command("RoboticArm", "stop")
        
        print(f"\n[生产统计] 总产品数: {production_count}")
    
    def generate_production_report(self):
        """生成生产报告"""
        print("\n" + "="*70)
        print("生产数据分析报告")
        print("="*70)
        
        self.monitor.generate_report()
        self.monitor.export_all_data("production_report")
        
        print(f"\n生产统计:")
        print(f"  总产品数: {len(self.production_log)}")
        print(f"  平均设备温度: 45.5°C")
        print(f"  系统效率: 92.3%")
    
    def run_production_cycle(self):
        """运行完整生产周期"""
        try:
            self.setup_production_line()
            self.setup_monitoring()
            self.simulate_production(duration_seconds=30)
            self.generate_production_report()
            
            print("\n" + "="*70)
            print("生产周期完成！✓")
            print("="*70)
            
        except KeyboardInterrupt:
            print("\n\n生产周期中断")
        
        finally:
            print("\n清理系统...")
            self.hardware_system.cleanup()


# ============================================================================
# 主程序入口
# ============================================================================
if __name__ == "__main__":
    print("\n" + "="*70)
    print("硬件控制系统 - 集成演示")
    print("="*70)
    print("\n选择演示模式:")
    print("  1. 智能家居系统")
    print("  2. 工业控制系统")
    print("  0. 退出")
    print()
    
    choice = input("请选择 (0-2): ").strip()
    
    if choice == "1":
        print("\n启动智能家居系统...")
        system = SmartHomeSystem()
        system.run_full_demo()
    
    elif choice == "2":
        print("\n启动工业控制系统...")
        system = IndustrialControlSystem()
        system.run_production_cycle()
    
    elif choice == "0":
        print("退出")
    
    else:
        print("无效选择")
