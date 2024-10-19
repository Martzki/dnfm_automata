import inspect
import os
import time

import cv2

from common.log import Logger

LOGGER = Logger(__name__).logger


def get_capture_file(prefix=''):
    path = "/workspace/training_data/" + time.strftime("%Y%m%d", time.localtime())
    if not os.path.isdir(path):
        os.mkdir(path)

    return path + "/{}_{}.png".format(prefix, time.strftime("%Y%m%d%H%M%S", time.localtime()))


def timeout_handler(exception, log, last_frame):
    log(exception)
    try:
        frame = inspect.stack()[1]
        for i in range(5):
            cv2.imwrite(f"{frame.filename}:{frame.lineno}_timeout_{i}.png", last_frame())
            time.sleep(1)
    except Exception:
        pass
