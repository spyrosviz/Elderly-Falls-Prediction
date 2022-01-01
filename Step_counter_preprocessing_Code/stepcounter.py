from calibrate_acceleration_data import Calibrate_accel_data
from kalmanfilter import Kalman_filter
from butterworth_lowpass_filter import butter_lowpass
from peak_detection_alg_stridetimes import stride_times
import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt


def acc_to_stridetimes(path, samp_freq):
    #import pilot data
    df = pd.read_csv(path,delimiter="\t",header=None,names=["time","ax","ay","az"])
    time = df["time"].values
    Ax = df["ax"].values
    Ay = df["ay"].values
    Az = df["az"].values
    
    #calibrate acceleration data
    Ax_calib, Ay_calib, Az_calib = Calibrate_accel_data(Ax, Ay, Az)
              
    #apply kalman filter
    Ax_filt, Ay_filt, Az_filt = Kalman_filter(Ax_calib, Ay_calib, Az_calib)
    
    #total acceleration
    Atotal = (np.sqrt(Ax_filt**2 + Ay_filt**2 + Az_filt**2))

    #apply butterwoth lowpass filter at 3Hz
    filt_signal = butter_lowpass(data=Atotal, cutoff=3, fs=samp_freq, order=4)

    #detect number of steps and stride times
    no_steps,stride_time = stride_times(filt_signal,samp_freq)

    return no_steps,stride_time

if __name__ == "__main__":
    # set input path
    path = r"Walks"

    # get all txts from folder named Walks
    filenames = glob.glob(path + "/*.txt")

    # dictionary to append timeseries data of each individual
    timeseries = {}

    # iterate over all txts to add subject's id as key and the corresponding stride times as value in the dictionary
    for file in filenames:
        steps, stride_time = acc_to_stridetimes(path=file,samp_freq=100)
        timeseries[file.split(sep="\\")[-1].split(sep=".")[0]] = stride_time

    # save timeseries on excel
    df = pd.DataFrame.from_dict(timeseries,orient="index")
    df = df.transpose()
    df.to_excel(r"stride_times.xlsx",index=False,header=df.columns)









    

