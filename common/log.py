import logging


class Logger(object):
    def __init__(self, module):
        self.logger = logging.getLogger(module)
        self.logger.setLevel(logging.INFO)
        sh = logging.StreamHandler()
        sh.setFormatter(logging.Formatter('%(asctime)s|%(levelname)s|%(filename)s:%(lineno)d|%(message)s'))
        self.logger.addHandler(sh)
