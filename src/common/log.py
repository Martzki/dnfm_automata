import logging


class Logger(object):
    def __init__(self, module):
        self.logger = logging.getLogger(module)
        self.logger.setLevel(logging.INFO)
        # sh = logging.StreamHandler()
    # self.logger.addHandler(sh)
