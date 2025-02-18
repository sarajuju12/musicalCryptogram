import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
import sounddevice as sd
from scipy import fft
from scipy.signal import find_peaks


class Decoder:
    def __init__(self, file_path):
        self.file_path = file_path
        self.audio_data = None
        self.sample_rate = None
        self.fund_freq = None

    def read_wav(self):
        audio_data, sample_rate = sf.read(self.file_path)

        # Convert from stereo to mono
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)

        # Remove DC offset
        audio_data -= np.mean(audio_data)
        self.audio_data = audio_data
        self.sample_rate = sample_rate

    def find_fund_freq(self):
        fft_data = fft.fft(self.audio_data)
        freqs = fft.fftfreq(len(fft_data), 1 / self.sample_rate)

        # Ignore negative frequencies
        pos_freq = freqs[:len(freqs) // 2]
        pos_fft = np.abs(fft_data[:len(fft_data) // 2])

        # Compute the average magnitude of frequencies above a set magnitude
        filtered_magnitudes_first = pos_fft[pos_fft > 1] # first pass
        avg_magnitude = np.mean(filtered_magnitudes_first)
        print(f"Average Magnitude: {avg_magnitude:.2f}")

        filtered_magnitudes_second = pos_fft[pos_fft > avg_magnitude * 2] # second pass
        avg_magnitude = np.mean(filtered_magnitudes_second)
        print(f"Average Magnitude: {avg_magnitude:.2f}")
        
        # Get all frequencies that surpass the threshold
        above_threshold_idx = np.where(pos_fft > avg_magnitude)[0]
        peak_freqs = pos_freq[above_threshold_idx]
        print(peak_freqs)

        plt.figure(figsize=(12, 6))
        plt.plot(freqs[:len(freqs) // 2], np.abs(fft_data[:len(fft_data) // 2]), color='royalblue',
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

