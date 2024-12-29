class Device(object):
    def start(self):
        pass

    def stop(self):
        pass

    def last_frame(self):
        pass

    def touch(self, coordinate, duration):
        pass

    def back(self):
        pass

    def swipe(self, start, end, move_step_length=50, move_steps_delay=0.05):
        pass
