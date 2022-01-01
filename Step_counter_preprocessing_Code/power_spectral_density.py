import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import welch,find_peaks,peak_widths
import pandas as pd

''' From power spectrum analysis find signal's dominant frequency, 
dominant frequency's amplitude, dominant frequency's width 
and dominant frequency's slope 

timeseries: the timeseries array input
fs: sampling frequency of the signal
plot: a plot showing dominant frequency's parameters
'''

def PSD(timeseries,fs,plot=False):

    # store frequencies under 10Hz
    freqs_all, power_all = welch(timeseries,fs)
    freqs = freqs_all[freqs_all<=10]
    power = power_all[freqs_all<=10]

    # find dominant frequency's power
    dom_freq_power = np.max(power)
    dom_freq = freqs[np.argmax(power)]

    # find peaks and their corresponding width in psd
    peaks,_ = find_peaks(power)
    widths = peak_widths(power,peaks,rel_height=0.5)

    # find dominant frequency's width in units of freqs indices
    dom_freq_index_width = widths[0][np.where(peaks==np.argmax(power))]

    # transform width unit into Hz (frequency bands increase by 0.390625)
    dom_freq_width = dom_freq_index_width * (freqs[1]-freqs[0])
    dom_freq_slope = dom_freq_power/dom_freq_width

    if plot==True:

        plt.plot(power)
        plt.plot(peaks, power[peaks], "x")
        plt.hlines(*widths[1:], color="g")
        plt.hlines(*widths[1:], color="r")
        plt.title("Power Spectral Density")
        plt.xlabel("Index of Frequency")
        plt.ylabel("Power")
        plt.show()

    return dom_freq,dom_freq_power,dom_freq_width,dom_freq_slope

if __name__ == "__main__":
    # import pilot data
    path = r"C:\Users\spyro\OneDrive\Documents\ΣΠΥΡΟΣ\Pycharm Projects\Github\Fallers-prediction\walkTxts\co009_base.txt"
    df = pd.read_csv(path, delimiter="\t", header=None, names=["time", "v", "ml", "ap"])
    time = df["time"].values
    v = df["v"].values
    ml = df["ml"].values
    ap = df["ap"].values

    print(PSD(ap,100))

