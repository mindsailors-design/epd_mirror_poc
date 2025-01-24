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
        mss.tools.to_png(screenshot.rgb, screenshot.size, output="screenshot_1072x1448.png")

        image_buffer = np.array(screenshot)

        return image_buffer

    def release(self):
        self.sct.close()

if __name__ == "__main__":
    # dodac wyswietlanie pojedynczej klatki na wyswietlaczu epapierowym
    import cv2
    screen_capture = ScreenCapture()

    try:
        while True:
            # frame = screen_capture.capture_screen()
            frame = screen_capture.capture_rectangle(1072, 1080)

            grayscale_frame = cv2.cvtColor(frame[..., :3], cv2.COLOR_BGR2GRAY)

            cv2.imshow("Rectangle capture", grayscale_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        screen_capture.release()
        cv2.destroyAllWindows()


