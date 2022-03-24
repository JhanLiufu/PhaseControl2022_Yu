from collections import deque


class Detector:

    def __init__(self, target_channel, trigger_dio, num_to_wait, regr_buffer_size, fltr_buffer_size, target_lowcut,
                 target_highcut):
        self.target_channel = target_channel
        self.trigger_dio = trigger_dio
        self.num_to_wait = num_to_wait
        self.regr_buffer_size = regr_buffer_size
        self.fltr_buffer_size = fltr_buffer_size
        self.target_lowcut = target_lowcut
        self.target_highcut = target_highcut
        self.trigger = False
        self.data_buffer = deque([], maxlen=fltr_buffer_size)
        self.sign_buffer = None
        self.curr_sign = None

    def flip_curr_sign(self):
        self.curr_sign = not self.curr_sign

    def check_sign_buffer(self):
        rtn = True
        for sign in self.sign_buffer:
            if self.curr_sign == sign:
                rtn = False
        return rtn

    def initialize_sign_buffer(self):
        self.sign_buffer = deque([self.curr_sign]*self.num_to_wait, maxlen=self.num_to_wait)