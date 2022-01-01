import pandas as pd
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt


def stride_times(Accel,fs,plot=False):

    #split filt_signal in windows of 12.8s size, see Activity recognition using a single accelerometer placed at the wrist or ankle

    window_size = int(12.8 * fs)
    def windows_nonoverlap (lista,m):
        y = []
        a = m
        k=0
        for i in range (int(len(lista)/m)+1):
            x = lista[k:m]
            y.append(x)
            k = k + a
            m = m + a
        return y

    acc_windows = windows_nonoverlap(Accel,window_size)


    #detect peaks in each window based on walking velocity (slow,normal,fast)
    peaks = []

    for window in acc_windows:
        if np.mean(window) <= 1.7:
            peaks_slow, _  = find_peaks(window, distance = 14, prominence = 0.2)
            peaks.append(peaks_slow)


        elif 1.7 < np.mean(window) <= 2.2:
            peaks_normal, _ = find_peaks(window, distance = 12, prominence = 0.25)
            peaks.append(peaks_normal)

        else:
            peaks_fast, _ = find_peaks(window, distance = 10, prominence = 0.35)
            peaks.append(peaks_fast)

    #set the index of peaks in order to match the respective number of frame of the time-series
    k = 0
    index = len(acc_windows[k])
    for p in range(1,len(peaks)):
        peaks[p] = peaks[p] + index
        k = k + 1
        index = index + len(acc_windows[k])


    #concatenate arrays with peaks indexes in one array
    concat_peaks = np.empty_like(peaks[0])
          
    for p in range (len(peaks)):
       concat_peaks = np.concatenate((concat_peaks,peaks[p]))

    steps = concat_peaks[len(peaks[0]):]
    stride_times = []

    if len(steps)//2 != 0:
        for f in range(0,len(steps)-2,2):
            time_diff = (steps[f+2] - steps[f])/fs
            stride_times.append(time_diff)

    else:
        for f in range(0,len(steps)-3,2):
            time_diff = (steps[f+2] - steps[f])/fs
            stride_times.append(time_diff)

    if plot == True:
        plt.plot(np.array(range(len(stride_times))),np.array(stride_times))
        plt.title("Stride Time Variability")
        plt.xlabel("Stride Number")
        plt.ylabel("Stride Time (s)")
        plt.show()

    return len(steps),stride_times

if __name__ == "__main__":

    
    #import pilot data
    df = pd.read_csv(r"C:\Users\Σπύρος\Documents\ΣΠΥΡΟΣ\Pycharm Projects\Parkinson dfa app\Android-Sensor-Stride\code\python scripts\pilot data acc spyros.csv",sep = ",",usecols = [0,1,2,3],nrows = 8721)
    time = df["time"].values
    Ax = df["ax (m/s^2)"].values
    Ay = df["ay (m/s^2)"].values
    Az = df["az (m/s^2)"].values
    Atotal = (np.sqrt(Ax**2 + Ay**2 + Az**2))/9.81 #Atotal unit = 1g = 9.81
    
    print(stride_times(Atotal,fs=208,plot=True))
