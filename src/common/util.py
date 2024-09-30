import os
import time


def get_capture_file(prefix=''):
    path = "/workspace/training_data/" + time.strftime("%Y%m%d", time.localtime())
    if not os.path.isdir(path):
        os.mkdir(path)

    return path + "/{}_{}.png".format(prefix, time.strftime("%Y%m%d%H%M%S", time.localtime()))
