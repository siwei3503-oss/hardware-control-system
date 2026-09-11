"""智能家居系统示例
Smart Home System Example
"""

import time
from datetime import datetime
from hardware_controller import (
    LEDController, ButtonController, MotorController,
    TemperatureSensor, HardwareControlSystem
)
from data_analyzer import RealTimeMonitor


class SmartHomeDemo:
    """智能家居演示系统"""
    
    def __init__(self):
        self.system = HardwareControlSystem()
        self.monitor = None
        self.setup()
    
    def setup(self):
        """初始化系统"""
        print("\n[初始化] 智能家居系统启动...\n")
        
        # 创建设备
        self.light = LEDController(pin=17)
        self.button = ButtonController(pin=27, callback=self.on_button_press)
        self.fan = MotorController(
            forward_pin=23,
            backward_pin=24,
            enable_pin=25
        )
        self.temp_sensor = TemperatureSensor(pin=4)
        
        # 注册设备
        self.system.add_device("Light", self.light)
        self.system.add_device("Button", self.button)
        self.system.add_device("Fan", self.fan)
        self.system.add_device("TempSensor", self.temp_sensor)
        
        # 初始化监控
        self.monitor = RealTimeMonitor(self.system)
        self.system.status_report()
    
    def on_button_press(self):
        """按钮按下回调"""
        print("[事件] 按钮被按下 - 切换照明")
        self.light.toggle()
    
    def run_climate_control(self):
        """运行温度控制演示"""
        print("\n" + "="*60)
        print("功能演示: 智能温度控制")
        print("="*60 + "\n")
        
        print("模式: 自动温度控制")
        print("- 温度 < 20°C: 关闭风扇")
        print("- 温度 20-25°C: 风扇低速 (50%)")
        print("- 温度 > 25°C: 风扇高速 (100%)\n")
        
        # 模拟温度变化
        temps = [18, 22, 26, 28, 25, 22, 20]
        
        for i, target_temp in enumerate(temps, 1):
            temp, humidity = self.temp_sensor.read_temperature()
            
            # 实际使用时用真实温度，这里用模拟值
            current_temp = target_temp + (i % 2) - 0.5
            
            print(f"\n[{i}/{len(temps)}] 当前温度: {current_temp:.1f}°C")
            
            if current_temp < 20:
                print("      状态: 温度过低 - 关闭风扇")
                self.fan.stop()
                fan_speed = 0
            elif current_temp < 25:
                print("      状态: 温度适中 - 风扇低速")
                self.fan.forward(speed=50)
                fan_speed = 50
            else:
                print("      状态: 温度过高 - 风扇高速")
                self.fan.forward(speed=100)
                fan_speed = 100
            
            # 记录数据
            self.monitor.collect_metrics("Climate", {
                'temperature': current_temp,
                'humidity': 60 + (i % 20),
                'fan_speed': fan_speed,
                'target_temp': 24
            })
            
            time.sleep(1)
        
        self.fan.stop()
        print("\n✓ 温度控制演示完成\n")
    
    def run_lighting_scene(self):
        """运行照明场景演示"""
        print("\n" + "="*60)
        print("功能演示: 智能照明场景")
        print("="*60 + "\n")
        
        scenes = [
            ("朝阳场景", 3, 0.3),
            ("工作场景", 5, 0.1),
            ("放松场景", 3, 0.4),
            ("夜间场景", 2, 0.6)
        ]
        
        for scene_name, flashes, interval in scenes:
            print(f"\n应用场景: {scene_name}")
            
            for j in range(flashes):
                self.light.turn_on()
                print(f"  闪烁 {j+1}/{flashes} - 开")
                time.sleep(interval)
                
                self.light.turn_off()
                print(f"  闪烁 {j+1}/{flashes} - 关")
                time.sleep(interval)
            
            # 记录场景
            self.monitor.collect_metrics("Lighting", {
                'scene': scene_name,
                'brightness': int(50 + (flashes * 10)),
                'power': 0.5 * flashes
            })
        
        print("\n✓ 照明场景演示完成\n")
    
    def run_energy_monitoring(self):
        """运行能耗监控演示"""
        print("\n" + "="*60)
        print("功能演示: 能耗监控")
        print("="*60 + "\n")
        
        devices_power = [
            ("客厅照灯", 10, 0.5),
            ("卧室照灯", 10, 0.3),
            ("风扇", 12, 1.5),
            ("冰箱", 220, 0.1),
            ("电视", 12, 2.0)
        ]
        
        print("设备功耗清单:\n")
        total_power = 0
        
        for device, voltage, current in devices_power:
            power = voltage * current
            total_power += power
            print(f"  {device:12} : {voltage:3}V × {current}A = {power:6.1f}W")
            
            self.monitor.power_analyzer.add_power_reading(
                datetime.now(), device, voltage, current
            )
        
        print(f"\n  {'总功耗':12} : {total_power:6.1f}W")
        
        # 计算24小时能耗
        daily_energy = total_power * 24 / 1000  # 转换为kWh
        print(f"  {'24h能耗':12} : {daily_energy:6.2f} kWh")
        
        # 模拟电费计算 (假设1元/kWh)
        daily_cost = daily_energy * 1.0
        monthly_cost = daily_cost * 30
        
        print(f"\n  {'日均费用':12} : ¥{daily_cost:.2f}")
        print(f"  {'月均费用':12} : ¥{monthly_cost:.2f}")
        
        print("\n✓ 能耗监控演示完成\n")
    
    def generate_report(self):
        """生成系统报告"""
        print("\n" + "="*60)
        print("生成系统报告")
        print("="*60)
        
        self.monitor.generate_report()
        self.monitor.export_all_data("smart_home_demo")
        
        print("\n数据已导出:")
        print("  - smart_home_demo_all.csv")
        print("  - smart_home_demo_all.json")
    
    def run(self):
        """运行完整演示"""
        try:
            self.run_lighting_scene()
            time.sleep(2)
            
            self.run_climate_control()
            time.sleep(2)
            
            self.run_energy_monitoring()
            time.sleep(2)
            
            self.generate_report()
            
            print("\n" + "="*60)
            print("智能家居演示完成！✓")
            print("="*60 + "\n")
        
        except KeyboardInterrupt:
            print("\n\n用户中断演示")
        
        finally:
            print("清理系统...")
            self.system.cleanup()


if __name__ == "__main__":
    demo = SmartHomeDemo()
    demo.run()
