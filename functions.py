import os
import numpy as np
from scipy.signal import *
import matplotlib
import matplotlib.pyplot as plt
import csv

data_path = "data\EEG-IO"
file_idx = 0
fs = 250.0

def get_files(data_path):
    
    # inputs:
    # outputs:
    
    # reading signal files
    signal_files = [f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f)) and '_data' in f]
    label_files = [f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f)) and '_labels' in f]
    
    return signal_files, label_files

def get_signals(signal_files, data_path, file_idx):
    
    # inputs:
    # outputs:
    
    # reading signals file
    signals = signal_files[file_idx]
    signals = np.loadtxt(open(os.path.join(data_path,signals), "rb"), delimiter=";", skiprows=1, usecols=(0,1,2))
    
    return signals

def get_blinks(labSel_files, data_path, file_idx, signals):
    
    # inputs:
    # ouputs:
    
    # reading labels file
    labels = label_files[file_idx]
    
    # parsing labels file
    interval_corrupt = []
    blinks = []
    n_corrupt = 0
    with open(os.path.join(data_path,labels)) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if row[0]=="corrupt":
                n_corrupt = int(row[1])
            elif n_corrupt > 0:
                if float(row[1]) == -1:
                    t_end = signals[-1,0]
                else:
                    t_end = float(row[1])
                interval_corrupt.append([float(row[0]), t_end])
                n_corrupt = n_corrupt - 1
            elif row[0]=="blinks":
                if not n_corrupt==0:
                    print("!Error in parsing")
            else:
                blinks.append([float(row[0]), int(row[1])])
    blinks = np.array(blinks)

    return interval_corrupt, blinks 

def get_windows(signal, time, window_size, window_stride):
    
    # inputs:
    # outputs:
    
    windows = []
    windows_times = []
    
    if len(signal) == len(time):
        for i in range(0, len(signal)-window_size-window_stride, window_stride):
            window = signal[i:i+window_size]
            window_time = time[i:i+window_size]
            windows.append(window)
            windows_times.append(window_time)    
    windows = np.array(windows)
    windows_times = np.array(windows_times)
    return windows, windows_times

def clean_windows(windows, windows_times, interval_corrupt):
    
    # inputs:
    # outputs:
    
    cleaned_windows = []
    cleaned_windows_times = []
    
    if len(interval_corrupt) == 0:
        cleaned_windows = windows
        cleaned_windows_times = windows_times
    else:
        for i in range(len(interval_corrupt)):
            for j in range(len(windows_times)):
                if not(interval_corrupt[i][0] <= windows_times[j][-1] and windows_times[j][0] <= interval_corrupt[i][-1]):
                    cleaned_windows.append(windows[j])
                    cleaned_windows_times.append(windows_times[j])
    cleaned_windows = np.array(cleaned_windows)
    cleaned_windows_times = np.array(cleaned_windows_times)
    return cleaned_windows, cleaned_windows_times

def butter_filter(signal, fs, fc):
    
    # inputs:
    # outputs:
    
    w = fc / (fs / 2) # Normalize the frequency
    b, a = butter(5, w, 'low')
    filtered_signal = filtfilt(b, a, signal)
    
    return np.array(filtered_signal)

def get_labels(windows_times, blinks):
    
    # inputs:
    # outputs:
    
    labels = [0 for _ in range(len(windows_times))]
    
    for i in range(len(windows_times)):
        w_start = windows_times[i][0]
        w_end = windows_times[i][-1]
        for j in range(len(blinks)):
            if (blinks[j][0] >= w_start and blinks[j][0] <= w_end):
                labels[i] = 1
    labels = np.array(labels)       
    return labels

def create_dataset(data_path, fs = 250.0):
    
    # inputs:
    # outputs:
    
    x = []
    y = []
    
    signal_files, label_files = get_files(data_path)
    
    for i in range(len(signal_files)):
        file_idx = i
        signals = get_signals(signal_files, data_path, file_idx)
        interval_corrupt, blinks = get_blinks(label_files, data_path, file_idx, signals)
        time = signals[:,0]
        signal = signals[:,1]
        filtered_signal = butter_filter(signal, fs, fc = 1)
        windows, windows_times = get_windows(signal, time, 500, 250)
        cleaned_windows, cleaned_windows_times = clean_windows(windows, windows_times, interval_corrupt)
        labels = get_labels(cleaned_windows_times, blinks)
        
        for j in range(len(cleaned_windows)):
            x.append(cleaned_windows[j])
            y.append(labels[j])
        
    x = np.array(x)
    y = np.array(y)
        
    return x, y