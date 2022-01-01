from scipy.signal import butter,filtfilt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#apply butterwoth lowpass filter - cutoff = desired freq, fs = sampling freq, order = polynomial order
def butter_lowpass(data, cutoff, fs, order,plot=False,time=0):
    wn = cutoff/(0.5 * fs)
    # Get the filter coefficients
    b, a = butter(order, wn, btype='low', analog=False)
    y = filtfilt(b, a, data)

    if plot == True:
        plt.plot(time,data,'y',label='unfiltered')
        plt.plot(time,y,'g',label='butterworth lowpass 3Hz')
        plt.legend()
        plt.show()
        
    return y

if __name__ == "__main__":

    #import pilot data
    df = pd.read_csv(r"C:\Users\Σπύρος\Documents\ΣΠΥΡΟΣ\Pycharm Projects\Parkinson dfa app\Android-Sensor-Stride\articles\pilot data acc spyros.csv",sep = ",",usecols = [0,1,2,3],nrows = 1000)
    time = df["time"].values
    Ax = df["ax (m/s^2)"].values
    Ay = df["ay (m/s^2)"].values
    Az = df["az (m/s^2)"].values
    #total acceleration
    Atotal = np.sqrt(Ax**2 + Ay**2 + Az**2)

    filt_signal = butter_lowpass(Atotal, 3, 208, 4)
    print(filt_signal)
