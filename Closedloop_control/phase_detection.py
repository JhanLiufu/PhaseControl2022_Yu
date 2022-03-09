"""""""""
Written by Mengzhan Liufu at Yu Lab, University of Chicago
"""""""""

import math
from bandpass_filter import bandpass_filter
import numpy as np
from scipy.signal import hilbert


# def calculate_rms(buffer):
#     """
#     return the root mean-squared of a given array
#     :param buffer: any array or list of number
#
#     :return: the root mean-squared value of the array as a proxy for its power
#     :rtype: float
#     """
#     square_summed = 0
#     for k in buffer:
#         square_summed += (k**2)
#
#     return math.sqrt(square_summed/len(buffer))


def detect_phase(buffer, sampling_freq, target_lowcut, target_highcut):
    filter_buffer = bandpass_filter('butterworth', buffer, sampling_freq, 1, target_highcut, target_lowcut)
    analytic = hilbert(filter_buffer)
    inst_phase = np.unwrap(np.angle(analytic))
    return inst_phase[-1]