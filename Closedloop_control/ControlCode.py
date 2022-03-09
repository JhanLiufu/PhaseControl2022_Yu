"""""""""
Written by Mengzhan Liufu at Yu Lab, University of Chicago
"""""""""
import trodes_connection as tc
from phase_detection import detect_phase
from data_buffering import data_buffering
# from determine_threshold import determine_threshold
from collections import deque
import threading
import time

# Connect to trodes
trodes_client, trodes_hardware, trodes_info, sampling_rate = tc.connect_to_trodes("tcp://127.0.0.1:49152", 20, 'lfp')

# Parameters
stimulation_num_wait = 3 # previously 15, but no decision made. Maybe 15 * (~20ms) might be too long?
buffer_size = 150
frequency_lowcut = 10  # low bound of target frequency range
frequency_highcut = 30  # high bound of target frequency range
noise_lowcut = 500  # low bound of noise range (usually a high freq band)
noise_highcut = 600  # high bound of noise range
stimulation_num_std = 3
noise_num_std = 6  # make this value high; filtered data is spiky on the edges
target_threshold = 300  # default target range detection threshold (refer to offline analysis!)
noise_threshold = 1000  # default noise range detection threshold

data_buffer = deque()

# Start data buffering
buffering_thread = threading.Thread(target=data_buffering, args=(trodes_client, data_buffer, buffer_size, sampling_rate, \
                                                                noise_lowcut, noise_highcut, noise_threshold))
buffering_thread.start()

time.sleep(2)

# Start detecting

# stimulation_status = False
# decision_list = [False] * stimulation_num_wait

while True:

    current_phase = detect_phase(data_buffer, sampling_rate, frequency_lowcut, frequency_highcut)
    print(current_phase)

    # current_decision = detect_with_rms(data_buffer, sampling_rate, frequency_lowcut, frequency_highcut)

    # decision_list.append(current_decision)
    # decision_list.pop(0)
    # stimulation = all(decision_list)

    # if (stimulation_status is False) and (stimulation is True):
    #     tc.call_statescript(trodes_hardware, 3)
    #     stimulation_status = True
    #
    # if (stimulation_status is True) and (stimulation is False):
    #     tc.call_statescript(trodes_hardware, 4)
    #     stimulation_status = False
