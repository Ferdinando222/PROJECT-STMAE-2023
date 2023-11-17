#%%
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import spectrogram

#%%
#INPUT
# Load the WAV audio file
sampling_rate, audio_data = wavfile.read(r'C:\Users\Utente\OneDrive - Politecnico di Milano\Immagini\Documenti\Development\Python\PROJECT-STMAE\PROJECT-STMAE-2023\train_lstm\data\archive\test\test_input\guitar.wav')
# Calculate the spectrogram
frequencies, times, Sxx = spectrogram(audio_data, fs=sampling_rate)

# Display the spectrogram
plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='auto')
plt.ylabel('Frequency (Hz)')
plt.xlabel('Time (s)')
plt.title('Spectrogram')
plt.colorbar(label='Intensity (dB)')
plt.ylim(0, 5000)  # Limit the displayed frequencies in the plot
plt.savefig(r'C:\Users\Utente\OneDrive - Politecnico di Milano\Immagini\Documenti\Development\Python\PROJECT-STMAE\PROJECT-STMAE-2023\train_lstm\data\plot\plot_input\spectrogram_input.jpg')
plt.show()

# %%
#OUTPUT

# Load the WAV audio file
sampling_rate, audio_data = wavfile.read(r'C:\Users\Utente\OneDrive - Politecnico di Milano\Immagini\Documenti\Development\Python\PROJECT-STMAE\PROJECT-STMAE-2023\train_lstm\data\archive\test\test_output\0.3-0.3-0.3.wav')
# Calculate the spectrogram
frequencies, times, Sxx = spectrogram(audio_data, fs=sampling_rate)

# Display the spectrogram
plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='auto')
plt.ylabel('Frequency (Hz)')
plt.xlabel('Time (s)')
plt.title('Spectrogram')
plt.colorbar(label='Intensity (dB)')
plt.ylim(0, 5000)  # Limit the displayed frequencies in the plot
plt.savefig(r'C:\Users\Utente\OneDrive - Politecnico di Milano\Immagini\Documenti\Development\Python\PROJECT-STMAE\PROJECT-STMAE-2023\train_lstm\data\plot\plot_output\spectrogram_0.3-0.3-0.3.jpg')
plt.show()
# %%

#MODEL
# Load the WAV audio file
sampling_rate, audio_data = wavfile.read(r'C:\Users\Utente\OneDrive - Politecnico di Milano\Immagini\Documenti\Development\Python\PROJECT-STMAE\PROJECT-STMAE-2023\train_lstm\data\archive\test\test_model\0.75-0.75-0.75(lstm8preAmp).wav')
# Calculate the spectrogram
frequencies, times, Sxx = spectrogram(audio_data, fs=sampling_rate)

# Display the spectrogram
plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='auto')
plt.ylabel('Frequency (Hz)')
plt.xlabel('Time (s)')
plt.title('Spectrogram')
plt.colorbar(label='Intensity (dB)')
plt.ylim(0, 5000)  # Limit the displayed frequencies in the plot
plt.savefig(r'C:\Users\Utente\OneDrive - Politecnico di Milano\Immagini\Documenti\Development\Python\PROJECT-STMAE\PROJECT-STMAE-2023\train_lstm\data\plot\plot_model\spectrogram_0.75-0.75-0.75(lstm8preAmp).jpg')
plt.show()

# %%
