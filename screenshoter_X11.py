import numpy as np
from threading import Thread, Lock
import Xlib
import Xlib.display
from Xlib import X

class WindowCapture:
    stopped = True
    lock = None
    screenshot = None
    windowID = None

    def __init__(self, window_name='Firefox'):
        self.lock = Lock()
        self.screenshot = None
        display = Xlib.display.Display()
        try:
            root = display.screen().root
            windowIDs = root.get_full_property(display.intern_atom('_NET_CLIENT_LIST'), X.AnyPropertyType).value
            
            for windowID in windowIDs:
                window = display.create_resource_object('window', windowID)
                window_title_property = window.get_full_property(display.intern_atom('_NET_WM_NAME'), 0)
                # if not window_title_property:
                #     window_title_property = window.get_full_property(display.intern_atom('_NET_WM_NAME'), 0)
                if window_title_property and window_name.lower() in window_title_property.value.decode('utf-8').lower():
                    self.windowID = windowID

            if not self.windowID:
                raise Exception('Window not found: {}', format(window_name))

        finally:
            display.close()

    def get_screenshot(self):
        print("In get_screenshot")
        display = Xlib.display.Display()
        window = display.create_resource_object('window', self.windowID)

        geometry = window.get_geometry()
        width, height = geometry.width, geometry.height

        pixmap = window.get_image(0, 0, width, height, X.ZPixmap, 0xffffffff)
        data = pixmap.data
        image = np.frombuffer(data, dtype='uint8').reshape((height, width, 4))
        display.close()
        return image
    
    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()
        print("Started!")

    def stop(self):
        self.stopped = True
        print("Stopped!")

    def run(self):
        while not self.stopped:
            # print("Taking a screenshot!")
            screenshot = self.get_screenshot()
            self.lock.acquire()
            self.screenshot = screenshot
            self.lock.release()

if __name__ == "__main__":
    import cv2 as cv
    from screenshoter_X11 import WindowCapture
    
    wincap = WindowCapture('galculator')
    wincap.start()

    # image = wincap.get_screenshot()
    # cv.imshow("Screenshot", image)
    # print("wincap screenshot taken")

    run = True

    # if wincap.screenshot is not None:
    #     image = wincap.screenshot
    #     print("Screenshot taken!")

    while run:
        if wincap.screenshot is not None:
            image = wincap.screenshot
            print("Screenshot taken!")
            # run = False
            # wincap.stop()
            cv.imshow("Screenshot", image)
            key = cv.waitKey(1)
            if key == ord('q'):
                run = False
                wincap.stop()
            

