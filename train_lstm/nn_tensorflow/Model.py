##MODELLO
import tensorflow as tf
class SimpleLSTM(tf.keras.Model):
    def __init__(self, hidden_size=32):
        super(SimpleLSTM, self).__init__()

         # Primo layer LSTM
        self.lstm = tf.keras.layers.LSTM(hidden_size, return_sequences=True, batch_input_shape=(None, None, 4))
        
        self.dense = tf.keras.layers.Dense(1)

        self.drop_hidden = True

    def zero_on_next_forward(self):
        self.drop_hidden = True
        
    def call(self, inputs):
        if self.drop_hidden:
            batch_size = tf.shape(inputs)[0]
            h_shape = (batch_size, self.lstm.units)
            hidden = tf.zeros(h_shape)
            cell = tf.zeros(h_shape)
            x = self.lstm(inputs, initial_state=[hidden, cell])
            self.drop_hidden = False
        else:
            x = self.lstm(inputs)

        return self.dense(x)

    def save_for_rtneural(self, outfile):
        self.save_weights(outfile)