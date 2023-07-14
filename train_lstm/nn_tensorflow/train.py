## This script trains an LSTM according
## to the method described in 
## A. Wright, E.-P. Damskägg, and V. Välimäki, ‘Real-time black-box modelling with recurrent neural networks’, in 22nd international conference on digital audio effects (DAFx-19), 2019, pp. 1–8.
import os
import model as md
import data as dt
import tensorflow as tf

# used for the writing of example outputs
run_name="BigMuff"
# dataset : need an input and output folder in this folder
#audio_folder = "../../data/audio_audacity_dist"
audio_folder = "/kaggle/input"
assert os.path.exists(audio_folder), "Audio folder  not found. Looked for " + audio_folder
# used to render example output during training
test_file = "/kaggle/input/test-audio/guitar.wav"
assert os.path.exists(test_file), "Test file not found. Looked for " + test_file
lstm_hidden_size = 8
learning_rate = 5e-3
batch_size = 32
max_epochs = 10000

# create the logger for tensorboard
#writer = SummaryWriter()

print("Loading dataset from folder ", audio_folder)

dataset = dt.generate_dataset(audio_folder + "/input-audio-2/", audio_folder + "/output-audio-2/", frag_len_seconds=0.5)
print(dataset)

print("Splitting dataset")
train_ds, val_ds, test_ds = dt.get_train_valid_test_datasets(dataset)


print("Creating model")
model = md.create_model()
print(model)

print("Creating data loaders")
train_ds = train_ds.map(lambda x, y: (x, y))
train_ds = train_ds.batch(batch_size).shuffle(buffer_size=len(train_ds))

val_ds = val_ds.map(lambda x, y: (x, y))
val_ds = val_ds.batch(batch_size).shuffle(buffer_size=len(val_ds))

test_ds = test_ds.map(lambda x, y: (x, y))
test_ds = test_ds.batch(batch_size).shuffle(buffer_size=len(test_ds))




# Compile the model with the optimizer
optimizer = tf.keras.optimizers.legacy.Adam()


model.compile(optimizer=optimizer, loss='mean_squared_error', metrics=['mse', tf.keras.metrics.RootMeanSquaredError(), md.R_squared])


model.fit(train_ds,epochs=1000,validation_data=val_ds, verbose='auto')