'''
Written by Mengzhan Liufu at Yu Lab, the University of Chicago
'''
import trodes_connection as tc
import phase_detection as pd
from data_buffering import data_buffering
from detector import Detector
from scipy.signal import butter, sosfiltfilt
import threading
import numpy as np

# ------------------------- trodes connection -------------------------
server_address = "tcp://127.0.0.1:49152"
lfp_client, trodes_hardware, trodes_info, sampling_rate = tc.connect_to_trodes(server_address, 20, 'lfp')
dio_client = tc.subscribe_to_data('digital', server_address)

# ------------------------- Parameters -------------------------
myDetc = Detector(3, 1, 3, 50, 400, 4, 10, 0.012)
'''
target_channel, trigger_dio, num_to_wait, regr_buffer_size, fltr_buffer_size, target_lowcut, target_highcut
default_slope
'''

# ------------------------- Initialize data_buffer -------------------------
for i in range(myDetc.fltr_buffer_size):
    current_sample = lfp_client.receive()
    current_data = current_sample['lfpData']
    myDetc.data_buffer.append(current_data[myDetc.target_channel])

buffering_thread = threading.Thread(target=data_buffering, args=(lfp_client, dio_client, myDetc))
buffering_thread.start()

# ------------------------- Initialize filter -------------------------
butter_filter = butter(1, [myDetc.target_lowcut, myDetc.target_highcut], 'bp', fs=sampling_rate, output='sos')

# ------------------------- Initialize sign buffer -------------------------
A = pd.generate_matrix(myDetc.regr_buffer_size)
curr_derv = pd.calculate_derv(A, butter_filter, myDetc)
myDetc.curr_sign = curr_derv > 0
myDetc.initialize_sign_buffer()

# ------------------------- Start detection -------------------------
target_phase = 3*np.pi/2
curr_phase = None
error_bound = 0.005  # can't be too big or too small

while True:

    try:
        curr_phase = myDetc.sample_count*myDetc.slope  # linear phase interpolation
    except TypeError:
        # sample count is None initially
        pass

    pd.update_signbuffer(A, butter_filter, myDetc)

    if myDetc.check_sign_buffer():
        curr_phase = myDetc.curr_sign*np.pi  # correct phase at critical point
        myDetc.update_slope()
        myDetc.flip_curr_sign()

    # UNTESTED
    try:
        if 0 <= (curr_phase - target_phase) <= error_bound:
            tc.call_statescript(trodes_hardware, 3)
    except TypeError:
        # curr_phase is None initially
        pass
