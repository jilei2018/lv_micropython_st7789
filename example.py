import usys as sys
sys.path.append('') # See: https://github.com/micropython/micropython/issues/6419

import lvgl as lv
import lv_utils

class Application:
    def __init__(self):
        # lvgl must be initialized before any lvgl function is called or object/struct is constructed!
        lv.init()

        # Identify platform and initialize it
        if not lv_utils.event_loop.is_running():
            try:
                self.init_gui_esp32()
            except ImportError:
                pass

            try:
                self.init_gui_SDL()
            except ImportError:
                pass

            # try:
            #     self.init_gui_stm32()
            # except ImportError:
            #     pass

    def init_gui_SDL(self):
        import SDL
        SDL.init(auto_refresh=False)
        self.event_loop = lv_utils.event_loop(refresh_cb = SDL.refresh)

        # Register SDL display driver.
        disp_buf1 = lv.disp_draw_buf_t()
        buf1_1 = bytes(240 * 240)
        disp_buf1.init(buf1_1, None, len(buf1_1)//4)
        disp_drv = lv.disp_drv_t()
        disp_drv.init()
        disp_drv.draw_buf = disp_buf1
        disp_drv.flush_cb = SDL.monitor_flush
        disp_drv.hor_res = 240
        disp_drv.ver_res = 240
        disp_drv.register()

        # Regsiter SDL mouse driver
        indev_drv = lv.indev_drv_t()
        indev_drv.init() 
        indev_drv.type = lv.INDEV_TYPE.POINTER
        indev_drv.read_cb = SDL.mouse_read
        indev_drv.register() 


    def init_gui_esp32(self):
        import st7789_lvgl

        st7789 = st7789_lvgl.st7789_lvgl()
        self.event_loop = lv_utils.event_loop()

        # Register SDL display driver.
        hres = 240
        vres = 240
        disp_buf1 = lv.disp_draw_buf_t()
        buf1_1 = bytearray(hres * vres * lv.color_t.__SIZE__)
        buf1_2 = bytearray(hres * vres * lv.color_t.__SIZE__)
        disp_buf1.init(buf1_1, buf1_2, len(buf1_1) // lv.color_t.__SIZE__)
        # disp_buf1.init(buf1_1, None, len(buf1_1) // lv.color_t.__SIZE__)
        disp_drv = lv.disp_drv_t()
        disp_drv.init()
        disp_drv.draw_buf = disp_buf1
        disp_drv.flush_cb = st7789.flush
        disp_drv.hor_res = hres
        disp_drv.ver_res = vres
        disp_drv.register()


app = Application()

scr = lv.obj()
btn = lv.btn(scr)
btn.align_to(lv.scr_act(), lv.ALIGN.CENTER, 0, 0)
label = lv.label(btn)
label.set_text("Hello World!")


# Load the screen

lv.scr_load(scr)

import time
while True:
    time.sleep(1)