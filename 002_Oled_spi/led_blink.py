import time
from machine import Pin

# 初始化LED引脚，这里配置引脚2连接了一个LED
led_p2 = Pin(2, Pin.OUT)


def start_led_blink(blink_count, blink_tims_ms):
    """
    初始化阻塞闪烁，使LED闪烁指定次数和时间间隔。

    参数:
    blink_count (int): 闪烁次数，必须是1或更大的整数。
    blink_tims_ms (int): 每次闪烁的持续时间（毫秒），决定闪烁的速度。

    返回:
    无
    """
    # 检查闪烁次数是否满足要求
    if blink_count >= 1:
        # 循环执行闪烁操作
        for i in range(0, blink_count):
            # 关闭LED
            led_p2.off()
            # 等待一段时间，以控制闪烁速度
            time.sleep_ms(blink_tims_ms)
            # 打开LED
            led_p2.on()
            # 再次等待相同的时间，完成一次闪烁周期
            time.sleep_ms(blink_tims_ms)
