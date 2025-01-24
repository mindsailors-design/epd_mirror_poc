import mss 
import mss.tools
import numpy as np

class ScreenCapture:
    def __init__(self):
        self.sct = mss.mss()
    
    def capture_screen(self, monitor_index=1):
        monitor = self.sct.monitors[monitor_index]        
        screenshot = self.sct.grab(monitor)
        image_buffer = np.array(screenshot)

        return image_buffer
    
    def capture_rectangle(self, width, height, monitor_index=1):
        monitor = self.sct.monitors[monitor_index]
        screen_width = monitor['width']
        screen_height = monitor['height']

        left = (screen_width - width) // 2
        top = (screen_height - height) // 2

        bbox = {
            'left': left,
            'top' : top,
            'width': width,
            'height': height
        }

        screenshot = self.sct.grab(bbox)

        # debug, saving screenshot to a file
        # mss.tools.to_png(screenshot.rgb, screenshot.size, output="screenshot_1072x1448.png")

        image_buffer = np.array(screenshot)

        return image_buffer

    def release(self):
        self.sct.close()
