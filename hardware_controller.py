"""
硬件控制系统 - 软件控制硬件的核心模块
Hardware Control System - Software controlling hardware operations
"""

import RPi.GPIO as GPIO
import time
import threading
from datetime import datetime
import json
import csv
from abc import ABC, abstractmethod

# ============================================================================
# 1. GPIO 基础控制
# ============================================================================
class GPIOController:
    """GPIO控制器 - 管理GPIO引脚"""
    
    def __init__(self):
        """初始化GPIO"""
        GPIO.setmode(GPIO.BCM)  # 使用BCM编号
        GPIO.setwarnings(False)
        self.pins = {}
        print("[GPIO控制器] 已初始化")
    
    def setup_pin(self, pin, mode):
        """
        设置GPIO引脚
        pin: 引脚号
        mode: GPIO.IN (输入) 或 GPIO.OUT (输出)
        """
        GPIO.setup(pin, mode)
        self.pins[pin] = mode
        print(f"[GPIO] 引脚 {pin} 已设置为 {'输入' if mode == GPIO.IN else '输出'} 模式")
    
    def set_pin_high(self, pin):
        """设置引脚为高电平（打开）"""
        GPIO.output(pin, GPIO.HIGH)
        print(f"[GPIO] 引脚 {pin} -> 高电平 ✓")
    
    def set_pin_low(self, pin):
        """设置引脚为低电平（关闭）"""
        GPIO.output(pin, GPIO.LOW)
        print(f"[GPIO] 引脚 {pin} -> 低电平 ✓")
    
    def read_pin(self, pin):
        """读取GPIO引脚状态"""
        state = GPIO.input(pin)
        status = "高电平" if state else "低电平"
        print(f"[GPIO] 引脚 {pin} 状态: {status}")
        return state
    
    def cleanup(self):
        """清理GPIO"""
        GPIO.cleanup()
        print("[GPIO控制器] 已清理")


# ============================================================================
# 2. LED 控制
# ============================================================================
class LEDController(GPIOController):
    """LED控制器 - 控制LED灯"""
    
    def __init__(self, led_pin):
        """
        初始化LED
        led_pin: LED连接的GPIO引脚
        """
        super().__init__()
        self.led_pin = led_pin
        self.setup_pin(led_pin, GPIO.OUT)
        self.is_on = False
    
    def turn_on(self):
        """打开LED"""
        self.set_pin_high(self.led_pin)
        self.is_on = True
        print(f"[LED] LED已打开 🔴")
    
    def turn_off(self):
        """关闭LED"""
        self.set_pin_low(self.led_pin)
        self.is_on = False
        print(f"[LED] LED已关闭 ⚫")
    
    def toggle(self):
        """切换LED状态"""
        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()
    
    def blink(self, times=5, interval=0.5):
        """
        LED闪烁
        times: 闪烁次数
        interval: 闪烁间隔（秒）
        """
        print(f"[LED] 开始闪烁 ({times}次, 间隔{interval}秒)")
        for i in range(times):
            self.turn_on()
            time.sleep(interval)
            self.turn_off()
            time.sleep(interval)
        print(f"[LED] 闪烁完成")
    
    def pwm_brightness(self, frequency=1000, duty_cycle=50):
        """
        PWM控制LED亮度
        frequency: 频率（Hz）
        duty_cycle: 占空比 (0-100)
        """
        pwm = GPIO.PWM(self.led_pin, frequency)
        pwm.start(duty_cycle)
        print(f"[LED] PWM已启动 - 频率: {frequency}Hz, 占空比: {duty_cycle}%")
        return pwm


# ============================================================================
# 3. 按钮控制
# ============================================================================
class ButtonController(GPIOController):
    """按钮控制器 - 处理按钮输入"""
    
    def __init__(self, button_pin, callback=None):
        """
        初始化按钮
        button_pin: 按钮连接的GPIO引脚
        callback: 按钮按下时的回调函数
        """
        super().__init__()
        self.button_pin = button_pin
        self.setup_pin(button_pin, GPIO.IN)
        self.callback = callback
        self.press_count = 0
    
    def setup_interrupt(self, bouncetime=200):
        """
        设置按钮中断
        bouncetime: 防抖延迟（毫秒）
        """
        GPIO.add_event_detect(self.button_pin, GPIO.FALLING, 
                            callback=self._on_press, bouncetime=bouncetime)
        print(f"[按钮] 中断已设置")
    
    def _on_press(self, channel):
        """按钮按下处理"""
        self.press_count += 1
        print(f"[按钮] 被按下 #{self.press_count}")
        if self.callback:
            self.callback()
    
    def get_state(self):
        """获取按钮当前状态"""
        return self.read_pin(self.button_pin)


# ============================================================================
# 4. 温度传感器控制
# ============================================================================
class TemperatureSensor(GPIOController):
    """温度传感器控制器 - DHT11/DHT22"""
    
    def __init__(self, sensor_pin, sensor_type="DHT11"):
        """
        初始化温度传感器
        sensor_pin: 传感器连接的GPIO引脚
        sensor_type: "DHT11" 或 "DHT22"
        """
        super().__init__()
        self.sensor_pin = sensor_pin
        self.sensor_type = sensor_type
        
        # 尝试导入Adafruit库
        try:
            import Adafruit_DHT
            self.dht = Adafruit_DHT
        except ImportError:
            print("[温度传感器] 未安装Adafruit库")
            self.dht = None
        
        self.temperatures = []
        self.humidity_values = []
    
    def read_temperature(self):
        """读取温度和湿度"""
        if self.dht is None:
            print("[温度传感器] 模拟数据: 25.5°C, 65% 湿度")
            return 25.5, 65.0
        
        sensor = self.dht.DHT11 if self.sensor_type == "DHT11" else self.dht.DHT22
        humidity, temperature = self.dht.read_retry(sensor, self.sensor_pin)
        
        if humidity is not None and temperature is not None:
            self.temperatures.append(temperature)
            self.humidity_values.append(humidity)
            print(f"[温度传感器] 温度: {temperature:.1f}°C, 湿度: {humidity:.1f}%")
            return temperature, humidity
        else:
            print("[温度传感器] 读取失败")
            return None, None
    
    def get_average_temperature(self):
        """获取平均温度"""
        if self.temperatures:
            avg = sum(self.temperatures) / len(self.temperatures)
            print(f"[温度传感器] 平均温度: {avg:.2f}°C")
            return avg
        return None
    
    def continuous_monitoring(self, interval=5, duration=60):
        """
        持续监测温度
        interval: 读取间隔（秒）
        duration: 监测持续时间（秒）
        """
        print(f"[温度传感器] 开始监测 ({duration}秒)")
        start_time = time.time()
        
        while time.time() - start_time < duration:
            self.read_temperature()
            time.sleep(interval)
        
        print(f"[温度传感器] 监测完成")


# ============================================================================
# 5. 马达控制
# ============================================================================
class MotorController(GPIOController):
    """马达控制器 - 直流电机"""
    
    def __init__(self, forward_pin, backward_pin, enable_pin):
        """
        初始化马达
        forward_pin: 正向GPIO引脚
        backward_pin: 反向GPIO引脚
        enable_pin: 使能GPIO引脚（PWM）
        """
        super().__init__()
        self.forward_pin = forward_pin
        self.backward_pin = backward_pin
        self.enable_pin = enable_pin
        
        self.setup_pin(forward_pin, GPIO.OUT)
        self.setup_pin(backward_pin, GPIO.OUT)
        self.setup_pin(enable_pin, GPIO.OUT)
        
        self.pwm = GPIO.PWM(enable_pin, 1000)
        self.pwm.start(0)
        self.is_running = False
        print(f"[马达控制器] 已初始化")
    
    def forward(self, speed=100):
        """
        马达正向旋转
        speed: 速度 (0-100)
        """
        self.set_pin_high(self.forward_pin)
        self.set_pin_low(self.backward_pin)
        self.pwm.ChangeDutyCycle(speed)
        self.is_running = True
        print(f"[马达] 正向旋转，速度: {speed}%")
    
    def backward(self, speed=100):
        """
        马达反向旋转
        speed: 速度 (0-100)
        """
        self.set_pin_low(self.forward_pin)
        self.set_pin_high(self.backward_pin)
        self.pwm.ChangeDutyCycle(speed)
        self.is_running = True
        print(f"[马达] 反向旋转，速度: {speed}%")
    
    def stop(self):
        """停止马达"""
        self.set_pin_low(self.forward_pin)
        self.set_pin_low(self.backward_pin)
        self.pwm.ChangeDutyCycle(0)
        self.is_running = False
        print(f"[马达] 已停止")
    
    def change_speed(self, speed):
        """改变马达速度"""
        speed = max(0, min(100, speed))  # 限制范围0-100
        self.pwm.ChangeDutyCycle(speed)
        print(f"[马达] 速度已改变为: {speed}%")


# ============================================================================
# 6. 传感器基类
# ============================================================================
class Sensor(ABC):
    """传感器基类"""
    
    def __init__(self, name):
        self.name = name
        self.data = []
    
    @abstractmethod
    def read(self):
        """读取传感器数据"""
        pass
    
    def save_data(self, filename):
        """保存数据到CSV文件"""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.data)
        print(f"[{self.name}] 数据已保存到 {filename}")


# ============================================================================
# 7. 超声波传感器
# ============================================================================
class UltrasonicSensor(Sensor, GPIOController):
    """超声波距离传感器"""
    
    def __init__(self, trig_pin, echo_pin):
        """
        初始化超声波传感器
        trig_pin: 触发引脚
        echo_pin: 回声引脚
        """
        Sensor.__init__(self, "超声波传感器")
        GPIOController.__init__(self)
        
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        
        self.setup_pin(trig_pin, GPIO.OUT)
        self.setup_pin(echo_pin, GPIO.IN)
    
    def read(self):
        """读取距离"""
        # 发送触发信号
        self.set_pin_low(self.trig_pin)
        time.sleep(0.00001)
        self.set_pin_high(self.trig_pin)
        time.sleep(0.00001)
        self.set_pin_low(self.trig_pin)
        
        # 接收回声
        while GPIO.input(self.echo_pin) == 0:
            start_time = time.time()
        
        while GPIO.input(self.echo_pin) == 1:
            end_time = time.time()
        
        # 计算距离（声速340m/s）
        duration = end_time - start_time
        distance = duration * 340 / 2 * 100  # 转换为cm
        
        print(f"[超声波] 距离: {distance:.2f} cm")
        self.data.append([datetime.now(), distance])
        return distance


# ============================================================================
# 8. 光传感器
# ============================================================================
class LightSensor(Sensor, GPIOController):
    """光强度传感器"""
    
    def __init__(self, sensor_pin):
        """
        初始化光传感器
        sensor_pin: 传感器连接的GPIO引脚
        """
        Sensor.__init__(self, "光传感器")
        GPIOController.__init__(self)
        
        self.sensor_pin = sensor_pin
        self.setup_pin(sensor_pin, GPIO.IN)
    
    def read(self):
        """读取光强度"""
        brightness = GPIO.input(self.sensor_pin)
        status = "明亮" if brightness else "黑暗"
        print(f"[光传感器] 状态: {status}")
        self.data.append([datetime.now(), brightness])
        return brightness


# ============================================================================
# 9. 综合硬件控制系统
# ============================================================================
class HardwareControlSystem:
    """综合硬件控制系统"""
    
    def __init__(self):
        """初始化硬件控制系统"""
        self.devices = {}
        self.running = False
        print("\n" + "="*60)
        print("硬件控制系统已启动")
        print("="*60 + "\n")
    
    def add_device(self, name, device):
        """添加设备"""
        self.devices[name] = device
        print(f"[系统] 已添加设备: {name}")
    
    def get_device(self, name):
        """获取设备"""
        return self.devices.get(name)
    
    def execute_command(self, device_name, command, *args):
        """
        执行硬件命令
        device_name: 设备名称
        command: 命令名称
        *args: 命令参数
        """
        device = self.get_device(device_name)
        if device:
            method = getattr(device, command, None)
            if method:
                return method(*args)
            else:
                print(f"[错误] 设备 {device_name} 没有命令 {command}")
        else:
            print(f"[错误] 找不到设备 {device_name}")
    
    def status_report(self):
        """生成状态报告"""
        print("\n" + "="*60)
        print("硬件系统状态报告")
        print("="*60)
        print(f"已注册设备数: {len(self.devices)}")
        for name, device in self.devices.items():
            print(f"  ✓ {name}: {device.__class__.__name__}")
        print("="*60 + "\n")
    
    def emergency_stop(self):
        """紧急停止所有设备"""
        print("\n[系统] 执行紧急停止...")
        for name, device in self.devices.items():
            if hasattr(device, 'stop'):
                device.stop()
            elif hasattr(device, 'turn_off'):
                device.turn_off()
        print("[系统] 所有设备已停止")
    
    def cleanup(self):
        """清理系统"""
        self.emergency_stop()
        GPIO.cleanup()
        print("[系统] 已清理")


# ============================================================================
# 10. 示例使用
# ============================================================================
if __name__ == "__main__":
    # 创建硬件控制系统
    system = HardwareControlSystem()
    
    # 配置GPIO引脚
    LED_PIN = 17
    BUTTON_PIN = 27
    MOTOR_FORWARD = 23
    MOTOR_BACKWARD = 24
    MOTOR_ENABLE = 25
    TEMP_PIN = 4
    ULTRASONIC_TRIG = 5
    ULTRASONIC_ECHO = 6
    LIGHT_PIN = 12
    
    # 创建设备
    led = LEDController(LED_PIN)
    button = ButtonController(BUTTON_PIN, callback=led.toggle)
    motor = MotorController(MOTOR_FORWARD, MOTOR_BACKWARD, MOTOR_ENABLE)
    temp_sensor = TemperatureSensor(TEMP_PIN)
    ultrasonic = UltrasonicSensor(ULTRASONIC_TRIG, ULTRASONIC_ECHO)
    
    # 添加到系统
    system.add_device("LED", led)
    system.add_device("Button", button)
    system.add_device("Motor", motor)
    system.add_device("TemperatureSensor", temp_sensor)
    system.add_device("UltrasonicSensor", ultrasonic)
    
    # 生成状态报告
    system.status_report()
    
    try:
        # LED 测试
        print(">>> LED测试")
        system.execute_command("LED", "turn_on")
        time.sleep(1)
        system.execute_command("LED", "turn_off")
        time.sleep(1)
        system.execute_command("LED", "blink", 3, 0.5)
        
        # 马达测试
        print("\n>>> 马达测试")
        system.execute_command("Motor", "forward", 100)
        time.sleep(2)
        system.execute_command("Motor", "backward", 50)
        time.sleep(2)
        system.execute_command("Motor", "stop")
        
        # 温度传感器测试
        print("\n>>> 温度传感器测试")
        system.execute_command("TemperatureSensor", "read_temperature")
        
        # 超声波传感器测试
        print("\n>>> 超声波传感器测试")
        system.execute_command("UltrasonicSensor", "read")
        
        # 按钮中断测试
        print("\n>>> 按钮中断已设置（按Ctrl+C停止）")
        button.setup_interrupt()
        
        # 保持运行
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n[系统] 用户中断")
    
    finally:
        system.cleanup()
