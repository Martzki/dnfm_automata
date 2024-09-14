import logging
import time

import scrcpy

from src.common.log import Logger
from src.lib.device.device import Device

LOGGER = Logger(__name__).logger
LOGGER.setLevel(logging.INFO)


class ScrcpyDevice(Device):
    def __init__(self, adb_device):
        self.client = scrcpy.Client(device=adb_device)

    def register_init_handler(self, func):
        self.client.add_listener(scrcpy.EVENT_INIT, func)

    def register_frame_handler(self, func):
        self.client.add_listener(scrcpy.EVENT_FRAME, func)

    def touch(self, coordinate, duration=0.1):
        LOGGER.debug("touch {} with duration: {}".format(coordinate, duration))
        self.client.control.touch(coordinate[0], coordinate[1], scrcpy.ACTION_DOWN)
        time.sleep(duration)
        self.client.control.touch(coordinate[0], coordinate[1], scrcpy.ACTION_UP)

    def raw_touch(self, coordinate, press=True):
        LOGGER.debug("touch {} with press: {}".format(coordinate, press))
        if press:
            self.client.control.touch(coordinate[0], coordinate[1], scrcpy.ACTION_DOWN)
        else:
            self.client.control.touch(coordinate[0], coordinate[1], scrcpy.ACTION_UP)

    def swipe(self, start, end, move_step_length=50, move_steps_delay=0.051):
        LOGGER.debug(
            "swipe from {} to {} with move_step_length: {}, move_steps_delay: {}".format(start, end, move_step_length,
                                                                                         move_steps_delay))
        self.client.control.swipe(start[0], start[1], end[0], end[1], move_step_length, move_steps_delay)

    def last_frame(self):
        while True:
            frame = self.client.last_frame
            if frame is not None:
                return frame

            LOGGER.debug("Get empty frame, retry.")

    def start(self, threaded=True):
        self.client.start(threaded)
