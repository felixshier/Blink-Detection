import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
import keras.layers as layers
from keras.optimizers import SGD
from keras.initializers import random_uniform
from keras.callbacks import EarlyStopping

from functions import *

X, Y, Wt = create_dataset(data_path)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, test_size=0.2, random_state=42)

X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_val = X_val.reshape(X_val.shape[0], X_val.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

early_stopping = EarlyStopping(
    min_delta=0.001, # minimium amount of change to count as an improvement
    patience=20, # how many epochs to wait before stopping
    restore_best_weights=True,
)

model = Sequential([
    
    # first convolution block
    layers.Conv1D(nb_filter=16, filter_length=5, activation='relu', input_shape = X_train[0].shape),
    layers.MaxPool1D(),
    
    # second convolution block
    layers.Conv1D(nb_filter=32, filter_length=3, activation='relu'),
    layers.MaxPool1D(),
    
    # third convolution block
    layers.Conv1D(nb_filter=64, filter_length=1, activation='relu'),
    layers.MaxPool1D(),
    
    # fourth convolution block
    layers.Conv1D(nb_filter=128, filter_length=3, activation='relu'),
    layers.MaxPool1D(),
    
    # fifth convolution block
    layers.Conv1D(nb_filter=256, filter_length=5, activation='relu'),
    layers.MaxPool1D(),
    
    # classifier head 
    layers.Flatten(),
    layers.Dense(16, activation='relu', input_shape = (500,)),
    layers.Dense(32, activation='relu'),
    layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid'),
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['binary_accuracy'],
)

history = model.fit(
    X_train,
    Y_train,
    validation_data = (X_val, Y_val),
    epochs = 64,
    batch_size = 256,
    callbacks = [early_stopping]
)

history_frame = pd.DataFrame(history.history)
history_frame.loc[:, ['loss', 'val_loss']].plot()
history_frame.loc[:, ['binary_accuracy', 'val_binary_accuracy']].plot()

scores = model.evaluate(X_test, Y_test)
print("test loss, test acc:", scores)

preds = model.predict(X_test)
s=12
plt.title("actual:{}, predicted:{}".format(Y_test[s], preds[s]))
plt.plot(range(len(X_test[s])), X_test[s])
