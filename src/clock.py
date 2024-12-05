import time

class Clock:
    def __init__(self, start_elapsed_time=0.0):
        self.start = time.time() - start_elapsed_time

    def reset(self):
        self.start = time.time()

    def get_elapsed_time(self):
        return time.time() - self.start
