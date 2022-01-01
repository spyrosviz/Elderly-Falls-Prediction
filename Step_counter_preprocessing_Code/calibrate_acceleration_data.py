import pandas as pd
import numpy as np

'''Acceleration data calibration'''

def Calibrate_accel_data(Ax,Ay,Az):
    

    #calibrate data on x axis
    Kx = 2/np.sum((Ax[Ax>0])-np.sum(Ax[Ax<0]))
    offset_x = np.sum(((Kx*Ax[Ax>0]))+np.sum((Kx*Ax[Ax<0])))/2
    Ax_calib = np.array([x-offset_x for x in Ax])

    #calibrate data on y axis
    Ky = 2/np.sum((Ay[Ay>0])-np.sum(Ay[Ay<0]))
    offset_y = np.sum(((Ky*Ay[Ay>0]))+np.sum((Ky*Ay[Ay<0])))/2
    Ay_calib = np.array([y-offset_y for y in Ay])

    #calibrate data on z axis
    Kz = 2/np.sum((Az[Az>0])-np.sum(Az[Az<0]))
    offset_z = np.sum(((Kz*Az[Az>0]))+ np.sum((Kz*Az[Az<0])))/2
    Az_calib = np.array([z-offset_z for z in Az])

    return (Ax_calib, Ay_calib, Az_calib)

if __name__ == "__main__":
    
    #import pilot data
    df = pd.read_csv(r"C:\Users\Σπύρος\Documents\ΣΠΥΡΟΣ\Pycharm Projects\Parkinson dfa app\Android-Sensor-Stride\articles\pilot data acc spyros.csv",sep = ",",usecols = [0,1,2,3],nrows = 1000)
    time = df["time"].values
    Ax = df["ax (m/s^2)"].values
    Ay = df["ay (m/s^2)"].values
    Az = df["az (m/s^2)"].values
    
    print(Calibrate_accel_data(Ax, Ay, Az))

