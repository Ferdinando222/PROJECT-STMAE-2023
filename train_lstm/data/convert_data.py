# This script is used to convert the audio in frames of 0.5 seconds
# with a total length of 45 seconds

#%%
import librosa
import os
import numpy as np
import pandas as pd
import soundfile as sf
import random

DATA_AUDIO_DIR = r'C:\Users\Utente\OneDrive - Politecnico di Milano\Immagini\Documenti\Development\Python\PROJECT-STMAE\PROJECT-STMAE-2023\train_lstm\data\archive\input'
TARGET_SR = 44100
AUDIO_LENGTH = 22050
OUTPUT_DIR = r'C:\Users\Utente\OneDrive - Politecnico di Milano\Immagini\Documenti\Development\Python\PROJECT-STMAE\PROJECT-STMAE-2023\train_lstm\data\archive\output'
OUTPUT_DIR_TRAIN = os.path.join(OUTPUT_DIR, 'train_input')
OUTPUT_DIR_TEST = os.path.join(OUTPUT_DIR, 'test')


def read_audio_from_filename(filename):
    """Read audio from the specified path and .

    **Args:**

    `filename`: Path of the audio to read.

    `shift`: Argument used only if we want perform data augumentation. Shift the song with the selected number of semitones.

    **Returns:**
    Audio is a matrix composed by 22050 columns and 60 rows. Each row contains the samples of 0.5 seconds
    of the track from 15.0s to 45.0s.

    """
    audio = []
    for i in range(380):
        line,_ = librosa.load(filename,
                            offset=i/2, duration=0.5, sr=TARGET_SR)
        audio.append(librosa.util.normalize(line))
    return audio

def convert_data():
    """Reads audio from the specified path and converts it to WAV format in PCM 16 bit format.

    **Args:**

    `data_augmentation`: Flag indicating whether to perform data augmentation. Default is 0 (no data augmentation).
    """

    path = extract_input_target()
    for x_i in range(1):
        print(x_i)
        audio_buf = read_audio_from_filename(
            os.path.join(DATA_AUDIO_DIR, ('clean_signal'+'.wav')))
        
        print(len(audio_buf))
        for k, (audio_sample) in enumerate(audio_buf):
            
            # Zero padding if the sample is short

            if len(audio_sample) < AUDIO_LENGTH:
                audio_sample = np.concatenate((audio_sample, np.zeros(
                    shape=(AUDIO_LENGTH - len(audio_sample)))))
            
            output_folder = OUTPUT_DIR_TRAIN
            output_filename = os.path.join(
                output_folder, str(x_i) + str('_') + str(k)+'.wav')
            sf.write(output_filename,
                     audio_sample, TARGET_SR, subtype='PCM_16')
        
def extract_input_target():
    """Extract the path of each songs.

    **Returns:**

    A list of song paths
    """
    path_knobs = r'C:\Users\Utente\OneDrive - Politecnico di Milano\Immagini\Documenti\Development\Python\PROJECT-STMAE\PROJECT-STMAE-2023\train_lstm\data\archive\big_muff.csv'

    data_knobs = pd.read_csv(path_knobs)


    paths = data_knobs['path'].str.replace(".wav", "")
    return paths


#%%
convert_data()
# %%
