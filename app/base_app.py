class BaseApp(object):
    def __init__(self, device):
        self.device = device

    def init(self):
        self.device.register_init_handler(self.init_handler)
        self.device.register_frame_handler(self.frame_handler)
        self.device.start()

    def init_handler(self):
        pass

    def frame_handler(self, frame):
        pass
