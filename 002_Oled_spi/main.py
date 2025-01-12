import led_blink as led_blue
from machine import Pin,SPI
import ssd1306a
import font

led_blue.start_led_blink(10,50)

hspi = SPI(1,baudrate=40000000,polarity=0,phase=0)

display = ssd1306a.SSD1306_SPI(128,64,hspi,Pin(5),Pin(4),Pin(16))

display.init_display()
display.text('Hello,World', 0, 0)  # 显示字
display.draw_chinese_fast('天气多云', 0, 1)
display.draw_chinese_fast('天气多云', 0, 2)
display.draw_chinese_fast('天气多云', 0, 3)
display.show()




