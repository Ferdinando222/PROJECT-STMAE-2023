import tensorflow as tf
import soundfile as sf
import numpy as np
import MyDataLoader
import Model
import Loss
import utils_training as utils
import Save

lstm_hidden_size = 8
learning_rate = 5e-3
batch_size = 50
max_epochs = 10000


path_out = "/kaggle/input/ouput-fragments-v6/train_output"
path_in =  "/kaggle/input/input-fragments-v6/train_input"
path_knobs = "/kaggle/input/big-muff/big_muff.csv"
run_name = 'big_muff'

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


if __name__=="__main__":
    print("Create Dataset")
    dataset = MyDataLoader.MyDataLoader(path_in,path_out,path_knobs)

    print("Create Model")
    model = Model.SimpleLSTM(hidden_size = lstm_hidden_size)

    print("Creating loss functions")
    custom_loss = Loss.CombinedLoss(dc_weight=0.25, esr_weight=0.75)

    # CREATION OPTIMIZER
    optimizer = tf.keras.optimizers.Adam(
        learning_rate=learning_rate,
        weight_decay=1e-4  
    )

    #CREATION CALLBACK
    scheduler = tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',  
        factor=0.5,          
        patience=5,          
        verbose=True         
    )



    #Training
    
    #VERIFY GPU
    if tf.test.gpu_device_name():
        print('GPU found:')
        print(tf.config.list_physical_devices('GPU'))
    else:
        print("No GPU found.")

    lowest_val_loss = 0
    best_loss = False
    for epochs in range(max_epochs):
        ep_loss = utils.train_epoch_interval(model, dataset.train_ds, custom_loss, optimizer)
        val_loss = utils.compute_batch_loss(model, dataset.val_ds, custom_loss, optimizer)

       
        if lowest_val_loss == 0:  # Primo run
            lowest_val_loss = val_loss
        elif val_loss < lowest_val_loss:  # Nuovo record
            lowest_val_loss = val_loss
            best_loss = True
        else:  # Nessun miglioramento
            best_loss = False

        if best_loss:# save best model so far
            print("Record loss - saving at ", epochs)
            Save.save_model(model,"model.json")

        # SAVE RUN TEST
        if epochs % 50 == 0:# save an example processed audio file
            run_test()
            
        # PRINT INFORMATION ON LOSS
        print("epoca, addestramento, validazione ", epochs, ep_loss, val_loss)