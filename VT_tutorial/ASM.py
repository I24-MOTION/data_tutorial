import numpy as np
import pandas as pd
smooth_x_window = 0.15
smooth_t_window = 36
def beta_free_flow(x,t,x_s,t_s,x_win,t_win,c_free=-70):
    dt = t-t_s- 3600*(x-x_s)/c_free
    dx = x-x_s
    return np.exp(-(np.abs(dx)/x_win + np.abs(dt)/t_win))

def beta_cong_flow(x,t,x_s,t_s,x_win,t_win,c_cong=13):
    dt = t-t_s- 3600*(x-x_s)/c_cong
    dx = x-x_s
    return np.exp(-(np.abs(dx)/x_win + np.abs(dt)/t_win))

def EGTF(x,t,smooth_x_window, smooth_t_window, speed_raw_df):
    speed = speed_raw_df[(np.abs(speed_raw_df.t - t)<=(smooth_t_window/2)) & (np.abs(speed_raw_df.x - x)<=(smooth_x_window/2))]
    speed = speed.copy()
    EGTF_v_free = 80
    EGTF_v_cong = 80
    # Now apply your functions
    speed['beta_free'] = speed.apply(lambda v: beta_free_flow(x, t, v.x, v.t, smooth_x_window, smooth_t_window), axis=1)
    speed['beta_cong'] = speed.apply(lambda v: beta_cong_flow(x, t, v.x, v.t, smooth_x_window, smooth_t_window), axis=1)
    if((sum(speed.beta_free)!=0) & (sum(speed.beta_cong)!=0)):
        EGTF_v_free = sum(speed.beta_free * speed.speed) / sum(speed.beta_free)
        EGTF_v_cong = sum(speed.beta_cong * speed.speed) / sum(speed.beta_cong)
#         print(EGTF_v_free,EGTF_v_cong)
    v = min(EGTF_v_free,EGTF_v_cong)
    tanh_term = np.tanh((36-v) / 3.1)
    w = 0.5*(1+tanh_term)
    return w*EGTF_v_cong + (1-w)*EGTF_v_free

def smooth_raw_data(speed_raw, dx, dt, smooth_x_window = 0.15, smooth_t_window = 36):
    EGTF_speed = pd.DataFrame(speed_raw)
    EGTF_speed.columns=['t_index','x_index','speed']
    EGTF_speed['t'] = dt*EGTF_speed['t_index']
    EGTF_speed['x'] = dx*EGTF_speed['x_index'] + 58.7
    speed_raw_df  = EGTF_speed.dropna().copy()
    EGTF_speed['EGTF'] = EGTF_speed.apply(lambda v: EGTF(v.x, v.t, smooth_x_window,smooth_t_window,speed_raw_df), axis=1)
    EGTF_speed.columns = ['t','x','raw_speed','time','milemarker','speed']
    return EGTF_speed