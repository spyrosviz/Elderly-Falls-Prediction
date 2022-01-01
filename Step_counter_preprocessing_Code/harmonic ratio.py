import numpy as np
from scipy.fft import rfft, rfftfreq
import pandas as pd

def HarmonicRatio(data,ml=False):
    # calculate fft for each axis
    ampl = rfft(data)
    freq = rfftfreq(len(data),1/100) # 100 is the sampling frequency

    # find dominant frequency
    dom_freq = freq[np.argmax(ampl)]

    # compute first 10 even and first 10 odd harmonics
    even = np.arange(2,21,2)*dom_freq
    even_round = np.array([round(i,2) for i in even])
    odd = np.arange(3,22,2)*dom_freq
    odd_round = np.array([round(i,2) for i in odd])

    # find the corresponding amplitudes of the even harmonics
    # harmonics amplitude is calculated from complex number output as np.sqrt(real**2 + imag**2)
    indices_even = []
    for e in even_round:
        if e in list(round(f,2) for f in freq):
            indices_even.append(list(round(f,2) for f in freq).index(e))
        else:
            continue

    even_harmonics = [np.sqrt((ampl[i].real)**2 + (ampl[i].imag)**2) for i in indices_even]

    # find the corresponding amplitudes of the odd harmonics
    indices_odd = []
    for o in odd_round:
        if o in list(round(f,2) for f in freq):
            indices_odd.append(list(round(f,2) for f in freq).index(o))
        else:
            continue

    odd_harmonics = [np.sqrt((ampl[i].real)**2 + (ampl[i].imag)**2) for i in indices_odd]

    # ml stands for mediolateral axis on gait
    if ml == False:
        # compute harmonics ratio, which is sum of evens divided by sum of odds
        harmonic_ratio = np.sum(np.array(even_harmonics)/np.sum(np.array(odd_harmonics)))
        return harmonic_ratio
    else:
        # compute harmonics ratio, which is sum of odds divided by sum of evens
        harmonic_ratio_ml = np.sum(np.array(odd_harmonics) / np.sum(np.array(even_harmonics)))
        return harmonic_ratio_ml


if __name__ == '__main__':
    # import pilot data
    path = r"C:\Users\spyro\OneDrive\Documents\ΣΠΥΡΟΣ\Pycharm Projects\Github\Fallers-prediction\walkTxts\co017_base.txt"
    df = pd.read_csv(path, delimiter="\t", header=None, names=["time", "v", "ml", "ap"])
    time = df["time"].values
    v = df["v"].values
    ml = df["ml"].values
    ap = df["ap"].values

    print(HarmonicRatio(v))
