import numpy as np
import pandas as pd
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
def get_bi_cubic(target_time, target_space,data):
# Extract necessary columns
    data_small = data[(np.abs(data.t - target_time) <=8) & (np.abs(data.x - target_space) <=0.04)]
    time = data_small['t']
    space = data_small['x']
    speed = data_small['speed']
    interpolated_value = griddata((time, space), speed, (target_time, target_space), method='cubic')
#         error_message = None
    return interpolated_value

def gen_VT(t0,v_id,large_speed_field,x0=0.32):
    start_time = t0 - 30
    end_time = t0 + 900 -30
#     print(t0,x0)
    ranged_speed_field = large_speed_field[(large_speed_field.t<=end_time) & (large_speed_field.t>start_time)]
    v0 = float(get_bi_cubic(t0,x0,ranged_speed_field))
#     print(t0,x0)
    traj = [(t0,x0,v0,v_id)]
    t = t0
    x = x0
    while (x<4.3):
        speed = float(get_bi_cubic(t,x,ranged_speed_field))
        x = x + 0.1*speed/3600
        t = round(t + 0.1,1)
        traj.append((t,x,speed,v_id))
    return traj

def gen_VT_k(smooth_speed, k = 1):
    smooth = smooth_speed.copy()
    smooth.columns = ['t_index', 'x_index', 'raw_speed', 't', 'x', 'speed']
    smooth_vt = smooth.copy()
    smooth_vt['x'] = 63 - smooth_vt['x']
    vt = pd.DataFrame(gen_VT(0, k, smooth_vt))
    vt.columns = ['time', 'space', 'speed', 'v_id']
    vt['space'] = 63 - vt['space']
    return vt
