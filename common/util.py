import inspect
import os
import time
from pathlib import Path

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
            cv2.imwrite(f"{frame.filename}_{frame.lineno}_timeout_{i}.png", last_frame())
            time.sleep(1)
    except Exception as e:
        LOGGER.error(e)


def get_file_key(file_name):
    return file_name.split('.')[0]


def to_camel_case(camel_case):
    elements = camel_case.split("_")
    return "".join(elem.title() for elem in elements)


def get_resource_base_dir(config_path, base_dir):
    return Path(os.path.dirname(config_path)) / base_dir
