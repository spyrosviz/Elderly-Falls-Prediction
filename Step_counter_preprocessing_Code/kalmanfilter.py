from pykalman import KalmanFilter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''Apply kalman filter on acceleration data'''

def Kalman_filter(Ax,Ay,Az,plot=False,time=0):
    #make an array with accel data from 3 axis
    
    df_accel = pd.DataFrame([Ax,Ay,Az]).T
    measurements_acc = df_accel.to_numpy()

    #build transition matrix (A) and observation matrix (C)
    A = [[1,0,0],[0,1,0],[0,0,1]]
    C = [[1,0,0],[0,1,0],[0,0,1]]

    #initiate kalman filter
    kf1 = KalmanFilter(transition_matrices = A,
                      observation_matrices = C,
                      initial_state_mean = [0,0,0])

    kf1 = kf1.em(measurements_acc, n_iter=5)
    (smoothed_state_means, smoothed_state_covariances) = kf1.smooth(measurements_acc)

    Ax_filt = smoothed_state_means[:, 0]
    Ay_filt = smoothed_state_means[:, 1]
    Az_filt = smoothed_state_means[:, 2]

    if plot == True:
        plt.figure(figsize = (15,15))
        plt.plot(time, measurements_acc[:, 0], 'b--',label = "Ax",alpha=0.5)
        plt.plot(time, measurements_acc[:, 1], 'r--',label = "Ay",alpha=0.5)
        plt.plot(time, measurements_acc[:, 2], 'g--',label = "Az",alpha=0.5)
        plt.plot(time, smoothed_state_means[:, 0], 'b')
        plt.plot(time, smoothed_state_means[:, 1], 'r')
        plt.plot(time,smoothed_state_means[:, 2], 'g')
        plt.legend()
        plt.show()

    return (Ax_filt, Ay_filt, Az_filt)

if __name__ == "__main__":
    
    #import pilot data
    df = pd.read_csv(r"C:\Users\Σπύρος\Documents\ΣΠΥΡΟΣ\Pycharm Projects\Parkinson dfa app\Android-Sensor-Stride\articles\pilot data acc spyros.csv",sep = ",",usecols = [0,1,2,3],nrows = 1000)
    time = df["time"].values
    Ax = df["ax (m/s^2)"].values
    Ay = df["ay (m/s^2)"].values
    Az = df["az (m/s^2)"].values

    filtered_signal = Kalman_filter(Ax,Ay,Az)
    print(filtered_signal)
    
