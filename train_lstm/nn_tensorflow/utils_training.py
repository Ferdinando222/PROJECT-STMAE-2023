import numpy as np
import tensorflow as tf

def train_epoch_interval(model,
                         dataloader,
                         loss_function,
                         optimizer,
                         device='gpu',
                         warm_up_len=1000,
                         sub_batch_seq_len=2048):
    batch_losses = []

    for batch_idx, (inputs, targets) in enumerate(dataloader):

        # Warm up. Shape: [batch, sequence, feature]
        model.zero_on_next_forward()  # Assuming the model is an LSTM with stateful=True
        model(inputs[:, 0:warm_up_len, :])
        optimizer.apply_gradients([])

        available_sub_batches = int(np.floor(inputs.shape[1] / sub_batch_seq_len))
        start_sample = warm_up_len
        end_sample = warm_up_len + sub_batch_seq_len

        for sub_batch_ind in range(available_sub_batches):
            start_sample = sub_batch_ind * sub_batch_seq_len
            end_sample = start_sample + sub_batch_seq_len

            current_inputs = inputs[:, start_sample:end_sample, :]
            current_targets = targets[:, start_sample:end_sample, :]

            # WE USE GRADIENT TAPE FOR COMPUTE THE GRADIENT
            with tf.GradientTape() as tape:
                outputs = model(current_inputs, training=True)
                loss = loss_function(current_targets, outputs)

        # COMPUTE GRADIENTS
        gradients = tape.gradient(loss, model.trainable_variables)

        # UPDATE WEIGHTS
        optimizer.apply_gradients(zip(gradients, model.trainable_variables))

        batch_losses.append(loss.numpy())

    # Should probably reset the hidden layers on the LSTM here if stateful
    # model.reset_states()

    ep_loss = np.mean(batch_losses)

    return ep_loss


def compute_batch_loss(model,
                       dataloader,
                       loss_function,
                       optimizer,
                       device='gpu',
                       warm_up_len=200):
    batch_losses = []

    for batch_idx, (inputs, targets) in enumerate(dataloader):
        model.zero_on_next_forward()
        # Send in the inputs without gradients for warm-up
        model(inputs[:, 0:warm_up_len, :])
        # Clear gradients from the warm-up phase
        optimizer.apply_gradients([])

        # Send in the inputs again, this time computing gradients for the loss
        with tf.GradientTape() as tape:
            outputs = model(inputs[:, warm_up_len:, :])
            loss = loss_function(targets[:, warm_up_len:, :], outputs)

        gradients = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(zip(gradients, model.trainable_variables))

        batch_losses.append(loss.numpy())

    ep_loss = np.mean(batch_losses)
    return ep_loss


import soundfile as sf
import numpy as np

def run_test():
    data, samplerate = sf.read(r'/kaggle/input/test-audio-norm/guitar_wav_normalized.wav', dtype='float32') 
    data = np.array(data) 
    knobs_0 = np.array([0.3,0.3,0.3])
    knobs_1 = np.array([1,1,1])
    knobs_2 = np.array([0.75,0.75,0.75])
    data = data[:, np.newaxis]
    
    
    result_array1 = np.repeat([knobs_0], len(data), axis=0)

    result_array2 = np.repeat([knobs_1], len(data), axis=0)

    result_array3 = np.repeat([knobs_2], len(data), axis=0)

    # Concatenate the repeated signal and the array along the second axis (axis=1)
    new_signal1 = np.concatenate((data, result_array1), axis=-1)
    new_signal2 = np.concatenate((data, result_array2), axis=-1)

    new_signal3 = np.concatenate((data, result_array3), axis=-1)



    new_signal1 = new_signal1[np.newaxis, :, :]
    new_signal2 = new_signal2[np.newaxis, :, :]
    new_signal3 = new_signal3[np.newaxis, :, :]

    y1 = model(new_signal1)
    y1 = np.array(y1)
    y1 = np.squeeze(y1)
    
    y2 = model(new_signal2)
    y2= np.array(y2)
    y2 = np.squeeze(y2)
    
    y3 = model(new_signal3)
    y3 = np.array(y3)
    y3 = np.squeeze(y3)
    print("save")
    sf.write(r'/kaggle/working/predicted_0.3_0.3_0.3.wav', y1, samplerate)
    sf.write(r'/kaggle/working/predicted_1_1_1.wav', y2, samplerate)
    sf.write(r'/kaggle/working/predicted_0.75_0.75_0.75.wav', y3, samplerate)