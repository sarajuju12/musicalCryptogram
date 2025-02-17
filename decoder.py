import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
import sounddevice as sd
from scipy import fft


class Decoder:
    def __init__(self, file_path):
        self.file_path = file_path
        self.audio_data = None
        self.sample_rate = None

    def read_wav(self):
        audio_data, sample_rate = sf.read(self.file_path)
        # Convert to mono if stereo
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)

        # Remove DC offset
        audio_data -= np.mean(audio_data)
        self.audio_data = audio_data
        self.sample_rate = sample_rate

    def find_fund_freq(self):
        fft_data = fft.fft(self.audio_data)
        frequencies = fft.fftfreq(len(fft_data), 1 / self.sample_rate)

        plt.figure(figsize=(12, 6))
        plt.plot(frequencies[:len(frequencies) // 2], np.abs(fft_data[:len(fft_data) // 2]), color='royalblue',
                 label='Original Spectrum')
        plt.title('Original Spectrum')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.grid(True)
        plt.show()

    def play_note(self):
        sd.play(self.audio_data, self.sample_rate)


decoder = Decoder('assets/notes/A4.wav')
decoder.read_wav()
decoder.play_note()
decoder.find_fund_freq()

