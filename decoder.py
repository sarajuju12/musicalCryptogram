import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
import sounddevice as sd
from scipy import fft

piano_note_frequencies = {'Db2': 69.2957, 'D2': 73.4162, 'Eb2': 77.7817, 'E2': 82.4069, 'F2': 87.3071, 'Gb2': 92.4986,
                          'G2': 97.9989, 'Ab2': 103.826, 'A2': 110.000, 'Bb2': 116.541, 'B2': 123.471, 'C3': 130.813,
                          'Db3': 138.591, 'D3': 146.832, 'Eb3': 155.563, 'E3': 164.814, 'F3': 174.614, 'Gb3': 184.997,
                          'G3': 195.998, 'Ab3': 207.652, 'A3': 220.000, 'Bb3': 233.082, 'B3': 246.942, 'C4': 261.626,
                          'Db4': 277.183, 'D4': 293.665, 'Eb4': 311.127, 'E4': 329.628, 'F4': 349.228, 'Gb4': 369.994,
                          'G4': 391.995, 'Ab4': 415.305, 'A4': 440.000, 'Bb4': 466.164, 'B4': 493.883, 'C5': 523.251,
                          'Db5': 554.365, 'D5': 587.330, 'Eb5': 622.254, 'E5': 659.255, 'F5': 698.456, 'Gb5': 739.989,
                          'G5': 783.991, 'Ab5': 830.609, 'A5': 880.000, 'Bb5': 932.328, 'B5': 987.767, 'C6': 1046.50,
                          'Db6': 1108.73, 'D6': 1174.66, 'Eb6': 1244.51, 'E6': 1318.51, 'F6': 1396.91, 'Gb6': 1479.98,
                          'G6': 1567.98, 'Ab6': 1661.22, 'A6': 1760.00, 'Bb6': 1864.66, 'B6': 1975.53, 'C7': 2093.00,
                          'Db7': 2217.46, 'D7': 2349.32, 'Eb7': 2489.02}


class Decoder:
    def __init__(self, file_path):
        self.file_path = file_path
        self.audio_data = None
        self.sample_rate = None
        self.fund_freq = None

    def read_wav(self):
        audio_data, sample_rate = sf.read(self.file_path)

        # Convert from stereo to mono
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
        magnitude_threshold = 65
        
        # Get all frequencies that surpass the threshold
        above_threshold_idx = np.where(pos_fft > magnitude_threshold)[0]
        peak_freqs = pos_freq[above_threshold_idx]
        print(peak_freqs)

        self.fund_freq = min(piano_note_frequencies, key=lambda note: abs(piano_note_frequencies[note] - peak_freqs[0]))
        print(f"Detected note: {self.fund_freq}")

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


#for key in piano_note_frequencies:
#    decoder = Decoder(f'assets/notes/{key}.wav')
#    decoder.read_wav()
    #decoder.play_note()
#    decoder.find_fund_freq()
decoder = Decoder(f'assets/notes/C5.wav')
decoder.read_wav()
decoder.play_note()
decoder.find_fund_freq()
