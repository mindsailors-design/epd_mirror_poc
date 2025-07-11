
from time import sleep
import argparse

from test_functions import *

def parse_args():
    p = argparse.ArgumentParser(description='Test EPD functionality')
    p.add_argument('-v', '--virtual', action='store_true',
                   help='display using a Tkinter window instead of the '
                        'actual e-paper device (for testing without a '
                        'physical device)')
    p.add_argument('-r', '--rotate', default=None, choices=['CW', 'CCW', 'flip'],
                   help='run the tests with the display rotated by the specified value')
    p.add_argument('-m', '--mirror', action='store_true',
                   help='Mirror the display (use this if text appears backwards)')
    return p.parse_args()

def main():
    import cv2
    from test_screenshot import ScreenCapture
    screen_capture = ScreenCapture()

    args = parse_args()
    # args = []

    # tests = []

    if not args.virtual:
        from IT8951.display import AutoEPDDisplay

        print('Initializing EPD...')

        # here, spi_hz controls the rate of data transfer to the device, so a higher
        # value means faster display refreshes. the documentation for the IT8951 devicm
        # says the max is 24 MHz (24000000), but my device seems to still work as high as
        # 80 MHz (80000000)
        display = AutoEPDDisplay(vcom=-2.15, rotate=args.rotate, mirror=args.mirror, spi_hz=24000000)

        print('VCOM set to', display.epd.get_vcom())

        # tests += [print_system_info]

    else:
        from IT8951.display import VirtualEPDDisplay
        display = VirtualEPDDisplay(dims=(800, 600), rotate=args.rotate, mirror=args.mirror)

    # tests += [
    #     clear_display,
    #     # display_gradient,
    #     # partial_update,
    #     display_image_8bpp,
    # ]

    # for t in tests:
    #     t(display)
    #     sleep(1)

    print_system_info(display)

    clear_display(display)

    try:
        while True:
            # frame = screen_capture.capture_screen()
            frame = screen_capture.capture_rectangle(1448, 1072)

            grayscale_frame = cv2.cvtColor(frame[..., :3], cv2.COLOR_BGR2GRAY)
            display_image_8bpp(display, grayscale_frame)

            # cv2.imshow("Rectangle capture", grayscale_frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
                # break

            # cv2.destroyWindow("Rectangle capture")


    finally:
        screen_capture.release()
        cv2.destroyAllWindows()


    print('Done!')

if __name__ == '__main__':
    main()
