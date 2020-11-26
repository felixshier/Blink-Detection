from functions import *

data_path = 'data\EEG-IO'
file_idx = 0
fs = 250.0

x, y, wt = create_dataset(data_path)

s = 11

plt.title(y[s])
plt.plot(wt[s], x[s])