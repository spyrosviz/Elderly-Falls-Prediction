import pandas as pd
import numpy as np
import glob
from Sample_Entropy import Sample_Entropy
from power_spectral_density import PSD
import sys
from datetime import datetime

# set input path
path = r"walkTxts"

# get all txts from folder named walkTxts
filenames = glob.glob(path + "/*.txt")

# dictionary to append timeseries data of each individual
dictionary = {}

# iterate over all txts to add subject's id as key and the corresponding stride times as value in the dictionary
for file in filenames:

    accel_data = pd.read_csv(file, delimiter="\t", header=None, names=["time", "v", "ml", "ap"])
    #t = accel_data["time"].values
    ap = accel_data["ap"].values
    ml = accel_data["ml"].values
    v = accel_data["v"].values

    variables = []

    currTime = datetime.now()
    sampen_ap = Sample_Entropy(ap, m=2, r=np.std(ap) * 0.10)
    sampen_ml = Sample_Entropy(ml, m=2, r=np.std(ml) * 0.10)
    sampen_v = Sample_Entropy(v, m=2, r=np.std(v) * 0.10)

    dom_freq_ap, dom_freq_ampl_ap, dom_freq_width_ap, dom_freq_slope_ap = PSD(ap,fs=100)
    dom_freq_ml, dom_freq_ampl_ml, dom_freq_width_ml, dom_freq_slope_ml = PSD(ml, fs=100)
    dom_freq_v, dom_freq_ampl_v, dom_freq_width_v, dom_freq_slope_v = PSD(v, fs=100)

    subjects_id = file.split(sep="\\")[-1].split(sep=".")[0]

    variables.extend([subjects_id, sampen_ap, sampen_ml, sampen_v,
                      dom_freq_ap, dom_freq_ampl_ap, dom_freq_width_ap[0], dom_freq_slope_ap[0],
                      dom_freq_ml, dom_freq_ampl_ml, dom_freq_width_ml[0], dom_freq_slope_ml[0],
                      dom_freq_v, dom_freq_ampl_v, dom_freq_width_v[0], dom_freq_slope_v[0]])


    dictionary[subjects_id] = variables
    print(subjects_id + ' done!')
    print('Time spent for this subj : ' + str(datetime.now() - currTime))
    print ("Size of dictionary in MB: " + str(sys.getsizeof(dictionary)/(1024**2)))

# save timeseries on excel
df = pd.DataFrame.from_dict(dictionary,orient="index")

df.to_excel(r"sampen_psd.xlsx",index=False,
            header=["subjects_id", "sampen_ap", "sampen_ml", "sampen_v",
                  "dom_freq_ap", "dom_freq_ampl_ap", "dom_freq_width_ap", "dom_freq_slope_ap",
                  "dom_freq_ml", "dom_freq_ampl_ml", "dom_freq_width_ml", "dom_freq_slope_ml",
                  "dom_freq_v", "dom_freq_ampl_v", "dom_freq_width_v", "dom_freq_slope_v"])
