from tensorflow.keras.regularizers import l2
from tensorflow import keras

def create_model():
    model = keras.Sequential()
    model.add(keras.layers.InputLayer(input_shape=(None, 1)))
    model.add(keras.layers.Conv1D(6, 3, dilation_rate=2, activation='tanh', padding='causal', kernel_initializer='glorot_uniform',kernel_regularizer=l2(0.0001), bias_initializer='random_normal'))
    model.add(keras.layers.LSTM (8, activation="tanh", return_sequences=True, recurrent_activation="sigmoid", use_bias=True, kernel_initializer="glorot_uniform", recurrent_initializer="orthogonal", bias_initializer="random_normal", unit_forget_bias=False))
    model.add(keras.layers.Dense(1, kernel_initializer="orthogonal", bias_initializer='random_normal'))
    return model