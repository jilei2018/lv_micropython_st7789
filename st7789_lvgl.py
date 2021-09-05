import lvgl as lv

import machine
import st7789

class st7789_lvgl():
    def __init__(self):
        if lv.color_t.__SIZE__ != 2:
            raise RuntimeError('st7789 micropython driver requires defining LV_COLOR_DEPTH=16')
        # if  not hasattr(lv.color_t().ch, 'green_l'):
        #     raise RuntimeError('st7789 BGR color mode requires defining LV_COLOR_16_SWAP=1')
        spi = machine.SPI(2, baudrate=40000000, polarity=1, sck=machine.Pin(18), mosi=machine.Pin(23))
        self.display = st7789.ST7789(spi, 240, 240, reset=machine.Pin(4, machine.Pin.OUT), dc=machine.Pin(0, machine.Pin.OUT))
        self.display.init()

    def flush(self, disp_drv, area, color_p):
        size = (area.x2 - area.x1 + 1) * (area.y2 - area.y1 + 1)
        data_view = color_p.__dereference__(size * lv.color_t.__SIZE__)
        self.display.blit_buffer(
                    data_view,
                    area.x1,
                    area.y1,
                    area.x2-area.x1+1,
                    area.y2-area.y1+1)
        disp_drv.flush_ready()
    