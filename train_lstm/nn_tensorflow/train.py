import os
import numpy as np
import soundfile as sf
import tensorflow as tf
import pandas as pd
import MyDataLoader

lstm_hidden_size = 64
learning_rate = 5e-3
batch_size = 50
max_epochs = 10000

print("Create Dataset")

path_in = '/kaggle/input/input-fragments/train_input'
path_out = '/kaggle/input/output-fragments/train'
path_knobs = '/kaggle/input/big-muff/big_muff.csv'
dataset = MyDataLoader(path_in,path_out,path_knobs)