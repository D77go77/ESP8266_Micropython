# ESP8266 MicroPython 示例

本仓库包含了一些用于 ESP8266 的 MicroPython 示例代码，旨在帮助开发者快速上手并测试 ESP8266 的功能。

## 目录

- [001_Blink](./001_Blink): 一个简单的 LED 闪烁示例，演示如何控制 ESP8266 的 GPIO 引脚。
- [002_Oled_spi](./002_Oled_spi): 演示如何通过 SPI 接口驱动 OLED 显示屏。

## 快速开始

1. **准备工作**:
   - 确保您的 ESP8266 已刷入 MicroPython 固件。
   - 安装一个支持 MicroPython 的开发环境，例如 [uPyCraft IDE](http://docs.dfrobot.com.cn/upycraft/) 或 [Thonny IDE](https://thonny.org/)。

2. **克隆仓库**:
   ```bash
   git clone https://github.com/D77go77/ESP8266_Micropython.git
   ```

3. **上传脚本**:
   - 使用开发环境将示例代码上传到 ESP8266。
   - 例如，在 uPyCraft 中，打开相应的 `.py` 文件，连接设备，然后点击“下载”按钮将脚本上传。

4. **运行示例**:
   - 在开发环境的终端中，执行相应的脚本，观察 ESP8266 的行为。
   - 例如，对于 `001_Blink` 示例，LED 应该以设定的频率闪烁。

## 资源

- [MicroPython 官方文档](https://docs.micropython.org/en/latest/esp8266/): 提供详细的 MicroPython 使用指南和 ESP8266 特定信息。
- [MicroPython 中文教程](https://github.com/micropython-Chinese-Community/mpycn-docs): 由社区维护的中文文档，适合中文用户参考。

## 许可证

本项目基于 GPL-3.0 许可证进行分发。有关详细信息，请参阅 [LICENSE](./LICENSE) 文件。

```
