from functions import *

data_path = 'data\EEG-IO'
file_idx = 0
fs = 250.0

signal_files, label_files = get_files(data_path)
signals = get_signals(signal_files, data_path, file_idx)
interval_corrupt, blinks = get_blinks(label_files, data_path, file_idx, signals)

time = signals[:,0]
unfiltered_signal = signals[:,1]
filtered_signal = butter_filter(unfiltered_signal, fs, fc = 1)

unfiltered_windows, unfiltered_windows_times = get_windows(unfiltered_signal, time, 500, 250)
unfiltered_cleaned_windows, unfiltered_cleaned_windows_times = clean_windows(unfiltered_windows, unfiltered_windows_times, interval_corrupt)

filtered_windows, filtered_windows_times = get_windows(filtered_signal, time, 500, 250)
filtered_cleaned_windows, filtered_cleaned_windows_times = clean_windows(filtered_windows, filtered_windows_times, interval_corrupt)

labels = get_labels(filtered_cleaned_windows_times, blinks)

plt.title(labels[4])
plt.plot(unfiltered_cleaned_windows_times[4], unfiltered_cleaned_windows[4])
plt.plot(filtered_cleaned_windows_times[4], filtered_cleaned_windows[4])