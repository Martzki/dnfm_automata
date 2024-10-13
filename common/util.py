import functools
import os
import signal
import time

from common.log import Logger

LOGGER = Logger(__name__).logger


def get_capture_file(prefix=''):
    path = "/workspace/training_data/" + time.strftime("%Y%m%d", time.localtime())
    if not os.path.isdir(path):
        os.mkdir(path)

    return path + "/{}_{}.png".format(prefix, time.strftime("%Y%m%d%H%M%S", time.localtime()))


def timeout_handler(signum, frame):
    raise TimeoutError()


def timeout(seconds):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            except TimeoutError as e:
                raise TimeoutError(f"Timeout for {seconds}s when exec {func.__name__}") from e
            finally:
                signal.alarm(0)  # Cancel the alarm
            return result
        return wrapper
    return decorator
