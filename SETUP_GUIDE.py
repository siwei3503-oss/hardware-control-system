"""
硬件配置和设置指南
Hardware Configuration and Setup Guide
"""

import os

# 创建README
README_CONTENT = """
# 硬件控制系统 - Software Controlling Hardware

一个完整的Python硬件控制和数据分析系统，用于控制GPIO设备、传感器和电机，并实时监控和分析硬件运行数据。

## 📋 系统架构

```
硬件控制系统
├── 硬件控制层 (Hardware Control Layer)
│   ├── GPIO控制器
│   ├── LED控制
│   ├── 按钮输入
│   ├── 马达控制
│   └── 传感器接口
│
├── 数据采集层 (Data Collection Layer)
│   ├── 实时监控
│   ├── 数据存储
│   └── 事件记录
│
└── 数据分析层 (Data Analysis Layer)
    ├── 功耗分析
    ├── 温度分析
    ├── 性能分析
    └── 可靠性分析
```

## 🎯 功能特性

### 1. 硬件控制模块 (hardware_controller.py)

#### GPIO控制器
```python
from hardware_controller import GPIOController

gpio = GPIOController()
gpio.setup_pin(17, GPIO.OUT)
gpio.set_pin_high(17)  # 设置高电平
```

#### LED控制
```python
from hardware_controller import LEDController

led = LEDController(pin=17)
led.turn_on()           # 打开LED
led.turn_off()          # 关闭LED
led.blink(times=5)      # LED闪烁
led.pwm_brightness(duty_cycle=50)  # PWM亮度控制
```

#### 按钮控制
```python
from hardware_controller import ButtonController

def on_press():
    print("按钮被按下")

button = ButtonController(pin=27, callback=on_press)
button.setup_interrupt()  # 设置中断
```

#### 马达控制
```python
from hardware_controller import MotorController

motor = MotorController(forward_pin=23, backward_pin=24, enable_pin=25)
motor.forward(speed=100)    # 正向100%速度
motor.backward(speed=50)    # 反向50%速度
motor.change_speed(75)      # 改变速度
motor.stop()                # 停止
```

#### 温度传感器
```python
from hardware_controller import TemperatureSensor

sensor = TemperatureSensor(pin=4, sensor_type="DHT11")
temp, humidity = sensor.read_temperature()
sensor.continuous_monitoring(interval=5, duration=60)  # 持续监测
```

#### 超声波传感器
```python
from hardware_controller import UltrasonicSensor

ultrasonic = UltrasonicSensor(trig_pin=5, echo_pin=6)
distance = ultrasonic.read()  # 读取距离(cm)
```

### 2. 数据分析模块 (data_analyzer.py)

#### 硬件数据分析
```python
from data_analyzer import HardwareDataAnalyzer

analyzer = HardwareDataAnalyzer()
analyzer.add_data(timestamp, "LED", "brightness", 100)
analyzer.create_dataframe()
analyzer.get_statistics()
analyzer.save_to_csv("data.csv")
```

#### 功耗分析
```python
from data_analyzer import PowerAnalyzer

power = PowerAnalyzer()
power.add_power_reading(timestamp, "Motor", voltage=12, current=2.5)
power.analyze_power_consumption()
energy = power.calculate_energy_consumption(duration_hours=1)
```

#### 温度分析
```python
from data_analyzer import TemperatureAnalyzer

temp = TemperatureAnalyzer()
temp.add_temperature_reading(timestamp, "CPU", temperature=45.5)
temp.analyze_temperature()
warnings, critical = temp.check_thermal_warnings(warning_threshold=80)
```

#### 性能分析
```python
from data_analyzer import PerformanceAnalyzer

perf = PerformanceAnalyzer()
perf.add_performance_metric(timestamp, "Motor", "RPM", 3000)
perf.analyze_performance("RPM")
perf.compare_devices("RPM")
```

#### 可靠性分析
```python
from data_analyzer import ReliabilityAnalyzer

reliability = ReliabilityAnalyzer()
reliability.log_error(timestamp, "Sensor", "读取失败")
reliability.add_uptime_record(timestamp, "CPU", "running")
uptime = reliability.calculate_uptime("CPU")
```

#### 实时监控
```python
from data_analyzer import RealTimeMonitor

monitor = RealTimeMonitor(hardware_system)
monitor.collect_metrics("LED", {
    'brightness': 100,
    'power_consumption': 0.5
})
monitor.generate_report()
monitor.export_all_data("report")
```

### 3. 集成示例 (main_demo.py)

#### 智能家居系统
```python
from main_demo import SmartHomeSystem

system = SmartHomeSystem()
system.run_full_demo()
```

#### 工业控制系统
```python
from main_demo import IndustrialControlSystem

system = IndustrialControlSystem()
system.run_production_cycle()
```

## 🔧 硬件接线图

### LED连接
```
GPIO 17 --- 220Ω电阻 --- LED --- GND
```

### 按钮连接
```
GPIO 27 --- 按钮 --- GND
(上拉电阻由软件处理)
```

### DC马达连接
```
GPIO 23 (正向) ─┐
               ├─ L298N 驱动模块 ─ 马达
GPIO 24 (反向) ─┤
GPIO 25 (使能) ─┘
```

### 温度传感器 (DHT11)
```
GPIO 4 ─ DHT11信号脚
5V     ─ DHT11电源
GND    ─ DHT11地线
```

### 超声波传感器
```
GPIO 5 (Trig) ─ HC-SR04 触发脚
GPIO 6 (Echo) ─ HC-SR04 回声脚
5V            ─ HC-SR04 电源
GND           ─ HC-SR04 地线
```

## 📦 依赖安装

### 基础依赖
```bash
pip install RPi.GPIO
pip install pandas numpy matplotlib seaborn
```

### 传感器库 (可选)
```bash
# DHT温度传感器
pip install Adafruit-DHT

# 如果使用其他传感器
pip install PyYAML
```

## 🚀 快速开始

### 1. 基础GPIO控制
```bash
python -c "
from hardware_controller import LEDController
led = LEDController(17)
led.turn_on()
input('按Enter关闭LED')
led.turn_off()
"
```

### 2. 运行完整演示
```bash
python main_demo.py
# 选择: 1 (智能家居) 或 2 (工业控制)
```

### 3. 收集和分析数据
```bash
python data_analyzer.py
# 自动生成示例数据并进行分析
```

## 📊 数据分析功能

### 支持的分析类型

| 分析类型 | 功能 |
|---------|------|
| **功耗分析** | 计算功耗、能耗、功率因数 |
| **温度分析** | 监测温度、发出告警 |
| **性能分析** | 分析RPM、速度、效率 |
| **可靠性分析** | 计算运行时间、记录故障 |
| **趋势分析** | 绘制时间序列图表 |
| **对比分析** | 比较多个设备性能 |
| **统计分析** | 均值、方差、分布 |

### 输出格式

- **CSV文件**: 用于Excel分析
- **JSON文件**: 用于程序处理
- **图表**: PNG格式可视化
- **文本报告**: 详细的分析总结

## 🎓 学习路径

### 初级 (第1-2周)
- [ ] 理解GPIO基础
- [ ] 学习LED控制
- [ ] 学习按钮输入
- [ ] 掌握基础数据采集

### 中级 (第3-4周)
- [ ] 掌握马达控制
- [ ] 学习PWM调速
- [ ] 理解传感器接口
- [ ] 数据分析基础

### 高级 (第5-8周)
- [ ] 多设备协同控制
- [ ] 实时监控系统
- [ ] 高级数据分析
- [ ] 系统集成和优化

## 🔒 安全注意事项

1. **电源安全**
   - 使用合适的电源电压
   - 避免短路
   - 使用保护电阻

2. **GPIO安全**
   - 不要同时设置相反的引脚状态
   - 使用程序退出时清理GPIO
   - 避免过流

3. **电机安全**
   - 启动前检查轴承
   - 使用合适的负载
   - 监测电机温度

4. **传感器安全**
   - 确保正确的供电电压
   - 检查数据线连接
   - 定期校准

## 📝 示例程序

### 示例1: 简单的LED闪烁
```python
from hardware_controller import LEDController
import time

led = LEDController(17)
for i in range(10):
    led.turn_on()
    time.sleep(0.5)
    led.turn_off()
    time.sleep(0.5)
led.cleanup()
```

### 示例2: 温度监控和告警
```python
from hardware_controller import TemperatureSensor
from data_analyzer import TemperatureAnalyzer
import time

sensor = TemperatureSensor(4)
analyzer = TemperatureAnalyzer()

for _ in range(60):
    temp, humidity = sensor.read_temperature()
    analyzer.add_temperature_reading(datetime.now(), "CPU", temp)
    time.sleep(1)

analyzer.analyze_temperature()
analyzer.check_thermal_warnings(warning_threshold=80)
```

### 示例3: 马达速度调节
```python
from hardware_controller import MotorController
import time

motor = MotorController(23, 24, 25)

# 逐渐加速
for speed in range(0, 101, 10):
    motor.forward(speed)
    time.sleep(1)

# 逐渐减速
for speed in range(100, -1, -10):
    motor.forward(speed)
    time.sleep(1)

motor.stop()
motor.cleanup()
```

## 🐛 故障排除

### GPIO初始化错误
```
RuntimeError: No access to /dev/mem. Try running as root!
```
**解决**: 使用sudo运行程序
```bash
sudo python main_demo.py
```

### 传感器无响应
```
传感器读取失败
```
**解决**:
1. 检查接线
2. 验证GPIO编号
3. 检查传感器电源

### 数据保存失败
```
PermissionError: [Errno 13] Permission denied
```
**解决**: 检查文件夹权限
```bash
chmod 777 ./output
```

## 📚 参考资源

- [RPi.GPIO文档](https://pypi.org/project/RPi.GPIO/)
- [Raspberry Pi官方文档](https://www.raspberrypi.com/documentation/)
- [Pandas数据分析](https://pandas.pydata.org/docs/)
- [Matplotlib绘图](https://matplotlib.org/stable/contents.html)

## 📄 许可证

MIT License

## 👨‍💻 作者

siwei3503-oss

## 🤝 贡献

欢迎提交Issues和Pull Requests!

---

**最后更新**: 2026-09-11
"""

if __name__ == "__main__":
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(README_CONTENT)
    print("README.md 已生成")
