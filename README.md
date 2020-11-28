# Blink-Detection

Blink-Detection is a repository designed to classify blinks in raw EEG signals using a 1D Convolutional Neural Network (CNN). 

## Data

The dataset used was obtained from: https://github.com/meagmohit/BLINK

Citation:

Mohit Agarwal, Raghupathy Sivakumar
BLINK: A Fully Automated Unsupervised Algorithm for Eye-Blink Detection in EEG Signals
57th Annual Allerton Conference on Communication, Control, and Computing (Allerton). IEEE, 2019.

## Pre-Processing

The file functions.py contains all functions used to process the data prior to modelling. These functions can be used to split and label the original raw EEG signals into filtered two second intervals with binary classifications.

<p align="center">
  <img src="images/raw-eeg-signal.png" width="600" title="Raw EEG Signal">
</p>

<p float = "left">
  <img src="images/blink-processed.png" width="300" title="Signal Interval with Blink Classification Post Processing"/>
  <img src="images/non-blink-processed.png" width="300" title="Classified Non-Blink Interval Post Processing"/>
</p>

## Model

<p align="center">
  <img src="images/model-architecture.png" width="600" title="Model Architecture">
</p>

## Results

The model designed achieved a peak accuracy of 95%.

<p float = "left">
  <img src="images/blink-prediction.png" width="300" title="Signal Interval with Blink Classification Post Processing"/>
  <img src="images/non-blink-prediction.png" width="300" title="Classified Non-Blink Interval Post Processing"/>
</p>