# 硬件控制系统 - Software Controlling Hardware

一个完整的Python硬件控制和数据分析系统，用于控制GPIO设备、传感器和电机，并实时监控和分析硬件运行数据。

![系统架构](docs/architecture.png)

## 🎯 核心功能

### 1️⃣ 硬件控制
- ✅ **GPIO控制** - 数字输入/输出
- ✅ **LED控制** - 开关和PWM亮度调节
- ✅ **按钮输入** - 中断和事件处理
- ✅ **马达控制** - 正向、反向、速度调节
- ✅ **传感器接口** - 温度、距离、光强等

### 2️⃣ 实时监控
- 📊 **数据采集** - 自动收集硬件指标
- 📈 **趋势分析** - 绘制时间序列图表
- ⚠️ **告警系统** - 阈值监控和告警
- 📝 **日志记录** - CSV和JSON格式导出

### 3️⃣ 数据分析
- 🔌 **功耗分析** - 电压、电流、功率、能耗
- 🌡️ **温度分析** - 温度监测和热管理
- ⚡ **性能分析** - RPM、速度、效率
- 🛡️ **可靠性分析** - 运行时间、故障率
- 📊 **统计分析** - 均值、方差、分布分析

## 📦 项目结构

```
hardware-control-system/
├── hardware_controller.py      # 硬件控制核心模块
├── data_analyzer.py            # 数据分析模块
├── main_demo.py                # 集成演示程序
├── SETUP_GUIDE.py              # 设置指南
├── requirements.txt            # Python依赖
├── config.yaml                 # 系统配置文件
├── README.md                   # 项目说明文档
└── docs/
    ├── architecture.png        # 系统架构图
    ├── wiring_diagram.png      # 接线图
    └── api_reference.md        # API参考
```

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 基础硬件控制
```python
from hardware_controller import LEDController

led = LEDController(pin=17)
led.turn_on()           # 打开LED
led.turn_off()          # 关闭LED
led.blink(times=5)      # 闪烁5次
```

### 3. 运行完整演示
```bash
sudo python main_demo.py
# 选择: 1 (智能家居) 或 2 (工业控制)
```

### 4. 数据分析
```python
from data_analyzer import HardwareDataAnalyzer

analyzer = HardwareDataAnalyzer()
analyzer.add_data(timestamp, "LED", "brightness", 100)
analyzer.get_statistics()
analyzer.save_to_csv("data.csv")
```

## 🔧 硬件接线

### LED连接
```
GPIO 17 ──┬──[220Ω]──> LED ──> GND
          └──────────────────> +5V
```

### DC马达连接
```
      GPIO 23 ──┐
      GPIO 24 ──┼──> L298N驱动模块 ──> 马达
      GPIO 25 ──┘
```

### 温度传感器 (DHT11)
```
GPIO 4 ──> DHT11 信号脚
+5V    ──> DHT11 电源
GND    ──> DHT11 地线
```

## 📊 支持的分析类型

| 分析类型 | 功能 | 输出 |
|---------|------|------|
| **功耗分析** | 计算功耗、能耗 | 图表、报告 |
| **温度分析** | 监测温度、告警 | 告警、趋势图 |
| **性能分析** | 分析RPM、速度 | 对比图、统计 |
| **可靠性分析** | 计算运行时间 | MTBF、故障率 |
| **统计分析** | 均值、方差等 | 统计表格 |

## 📚 API参考

### GPIO控制器
```python
from hardware_controller import GPIOController

gpio = GPIOController()
gpio.setup_pin(pin, mode)      # 设置引脚
gpio.set_pin_high(pin)         # 高电平
gpio.set_pin_low(pin)          # 低电平
gpio.read_pin(pin)             # 读取状态
```

### LED控制器
```python
from hardware_controller import LEDController

led = LEDController(pin)
led.turn_on()                   # 打开
led.turn_off()                  # 关闭
led.toggle()                    # 切换
led.blink(times, interval)      # 闪烁
led.pwm_brightness(freq, duty)  # PWM控制
```

### 马达控制器
```python
from hardware_controller import MotorController

motor = MotorController(fwd_pin, bwd_pin, en_pin)
motor.forward(speed)            # 正向
motor.backward(speed)           # 反向
motor.change_speed(speed)       # 改变速度
motor.stop()                    # 停止
```

### 数据分析器
```python
from data_analyzer import HardwareDataAnalyzer

analyzer = HardwareDataAnalyzer()
analyzer.add_data(ts, device, metric, value)     # 添加数据
analyzer.get_statistics()                        # 获取统计
analyzer.filter_by_device(name)                  # 按设备筛选
analyzer.plot_metric_trend(device, metric)       # 绘制趋势
analyzer.save_to_csv(filename)                   # 保存CSV
```

## 🎓 学习资源

### 初级教程
- [GPIO基础](docs/gpio_basics.md)
- [LED控制](docs/led_control.md)
- [按钮输入](docs/button_input.md)

### 中级教程
- [马达控制](docs/motor_control.md)
- [传感器使用](docs/sensor_usage.md)
- [PWM调速](docs/pwm_control.md)

### 高级教程
- [实时监控](docs/real_time_monitoring.md)
- [数据分析](docs/data_analysis.md)
- [系统集成](docs/system_integration.md)

## 🐛 故障排除

### GPIO权限错误
```
RuntimeError: No access to /dev/mem
```
**解决**: 使用sudo运行
```bash
sudo python main_demo.py
```

### 传感器无响应
- 检查GPIO编号是否正确
- 验证硬件接线
- 检查传感器电源

### 数据保存失败
- 检查目录权限: `chmod 777 ./data/`
- 确保磁盘空间足够

## 📝 配置文件

编辑 `config.yaml` 自定义系统参数：

```yaml
gpio:
  mode: BCM
  warnings: false

devices:
  LED:
    pin: 17
    type: digital_output

alarms:
  temperature:
    warning: 80
    critical: 90
```

## 🔒 安全建议

1. **电源安全**
   - 使用合适的电压
   - 添加保护电阻
   - 避免短路

2. **GPIO安全**
   - 使用程序退出时清理GPIO
   - 检查引脚冲突
   - 避免过流

3. **电机安全**
   - 启动前检查状态
   - 监测温度
   - 定期维护

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 👨‍💻 作者

**siwei3503-oss** - GitHub用户

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 贡献步骤
1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📞 联系方式

- GitHub Issues: [提交问题](../../issues)
- Email: siwei3503@gmail.com

## 🙏 致谢

感谢以下项目的支持：
- [RPi.GPIO](https://pypi.org/project/RPi.GPIO/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- [Raspberry Pi官方文档](https://www.raspberrypi.com/)

---

**最后更新**: 2026-09-11

⭐ 如果这个项目对你有帮助，请给个Star!
