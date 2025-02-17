# MicroPython SSD1306 OLED driver, I2C and SPI interfaces

from micropython import const
import framebuf
import font
import font_new

# register definitions
SET_CONTRAST = const(0x81)
SET_ENTIRE_ON = const(0xa4)
SET_NORM_INV = const(0xa6)
SET_DISP = const(0xae)
SET_MEM_ADDR = const(0x20)
SET_COL_ADDR = const(0x21)
SET_PAGE_ADDR = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP = const(0xa0)
SET_MUX_RATIO = const(0xa8)
SET_COM_OUT_DIR = const(0xc0)
SET_DISP_OFFSET = const(0xd3)
SET_COM_PIN_CFG = const(0xda)
SET_DISP_CLK_DIV = const(0xd5)
SET_PRECHARGE = const(0xd9)
SET_VCOM_DESEL = const(0xdb)
SET_CHARGE_PUMP = const(0x8d)


# Subclassing FrameBuffer provides support for graphics primitives
# http://docs.micropython.org/en/latest/pyboard/library/framebuf.html
class SSD1306(framebuf.FrameBuffer):
    def __init__(self, width, height, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.init_display()

    def init_display(self):
        for cmd in (
                SET_DISP | 0x00,  # off
                # address setting
                SET_MEM_ADDR, 0x00,  # horizontal
                # resolution and layout
                SET_DISP_START_LINE | 0x00,
                SET_SEG_REMAP | 0x01,  # column addr 127 mapped to SEG0
                SET_MUX_RATIO, self.height - 1,
                SET_COM_OUT_DIR | 0x08,  # scan from COM[N] to COM0
                SET_DISP_OFFSET, 0x00,
                SET_COM_PIN_CFG, 0x02 if self.height == 32 else 0x12,
                # timing and driving scheme
                SET_DISP_CLK_DIV, 0x80,
                SET_PRECHARGE, 0x22 if self.external_vcc else 0xf1,
                SET_VCOM_DESEL, 0x30,  # 0.83*Vcc
                # display
                SET_CONTRAST, 0xff,  # maximum
                SET_ENTIRE_ON,  # output follows RAM contents
                SET_NORM_INV,  # not inverted
                # charge pump
                SET_CHARGE_PUMP, 0x10 if self.external_vcc else 0x14,
                SET_DISP | 0x01):  # on
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def poweroff(self):
        self.write_cmd(SET_DISP | 0x00)

    def poweron(self):
        self.write_cmd(SET_DISP | 0x01)

    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def show(self):
        x0 = 0
        x1 = self.width - 1
        if self.width == 64:
            # displays with width of 64 pixels are shifted by 32
            x0 += 32
            x1 += 32
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(x0)
        self.write_cmd(x1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_data(self.buffer)

    def draw_chinese(self, ch_str, x_axis, y_axis):
        offset_ = 0
        y_axis = y_axis * 16  # 中文高度一行占8个
        x_axis = (x_axis * 16)  # 中文宽度占16个
        order = []
        for i in ch_str:  #这里莫名其妙显示字符串的顺序不对，所以对字符串做一个逆序操作
            order.append(i)
        order.reverse()
        ch_str1 = "".join(order)

        for k in ch_str1:
            code = 0x00  # 将中文转成16进制编码
            data_code = k.encode("utf-8")
            code |= data_code[0] << 16
            code |= data_code[1] << 8
            code |= data_code[2]
            print(hex(code))
            byte_data = font.byte2.get(code)
            for y in range(0, 16):
                a_ = bin(byte_data[y]).replace('0b', '')
                while len(a_) < 8:
                    a_ = '0' + a_
                b_ = bin(byte_data[y + 16]).replace('0b', '')
                while len(b_) < 8:
                    b_ = '0' + b_
                for x in range(0, 8, 1):
                    self.pixel(x_axis + x - offset_, y + y_axis, int(a_[x]))  # 文字的上半部分
                    self.pixel(x_axis + x + 8 - offset_, y + y_axis, int(b_[x]))  # 文字的下半部分

            offset_ += 16

    def draw_chinese_fast(self, ch_str, x_axis, y_axis):
        offset_ = 0
        y_axis = y_axis * 16  # 中文高度一行占8个
        x_axis = (x_axis * 16)  # 中文宽度占16个
        for k in ch_str:
            code = 0x00  # 将中文转成16进制编码
            data_code = k.encode("utf-8")
            code |= data_code[0] << 16
            code |= data_code[1] << 8
            code |= data_code[2]

            try:
                byte_data = font_new.byte2.get(code)
                byte = bytearray(byte_data)
                buf = framebuf.FrameBuffer(byte, 16, 16, framebuf.MONO_HLSB)
                self.blit(buf, x_axis + offset_, y_axis)
            except:
                print(code)

            offset_ += 16


class SSD1306_I2C(SSD1306):
    def __init__(self, width, height, i2c, addr=0x3c, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        self.write_list = [b'\x40', None]  # Co=0, D/C#=1
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.temp[0] = 0x80  # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_data(self, buf):
        self.write_list[1] = buf
        self.i2c.writevto(self.addr, self.write_list)


class SSD1306_SPI(SSD1306):
    def __init__(self, width, height, spi, dc, res, cs, external_vcc=False):
        self.rate = 10 * 1024 * 1024
        dc.init(dc.OUT, value=0)
        res.init(res.OUT, value=0)
        cs.init(cs.OUT, value=1)
        self.spi = spi
        self.dc = dc
        self.res = res
        self.cs = cs
        import time
        self.res(1)
        time.sleep_ms(1)
        self.res(0)
        time.sleep_ms(10)
        self.res(1)
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(buf)
        self.cs(1)


