import tensorflow as tf
import soundfile as sf
import numpy as np

#
data, samplerate = sf.read(r'C:\Users\Utente\OneDrive - Politecnico di Milano\Immagini\Documenti\Development\Python\PROJECT-STMAE\PROJECT-STMAE-2023\train_lstm\data\my_processed_audio\audacity_dist30.wav', dtype='float32') 
data = np.array(data) 
print(data)