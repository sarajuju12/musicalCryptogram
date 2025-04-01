import os

import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import soundfile as sf
from scipy import fft
from scipy.fft import ifft
from assets.key_mappings import key_mappings

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
THRESHOLD = 15


class Decoder:
    def __init__(self, file_path):
        self.file_path = file_path
        self.audio_data = None
        self.sample_rate = None

    def filter_low_magnitude(self):
        fft_data = fft.fft(self.audio_data)
        freqs = fft.fftfreq(len(self.audio_data), d=1 / self.sample_rate)
        magnitudes = np.abs(fft_data)

        # Find frequencies that go above threshold
        above_threshold_idx = np.where(magnitudes > THRESHOLD)[0]
        fundamental_freq_idx = above_threshold_idx[0]  # First frequency above threshold
        fundamental_freq = freqs[fundamental_freq_idx]

        # Zero out frequencies BELOW the fundamental frequency
        fft_data[freqs < fundamental_freq] = 0
        filtered_audio = np.real(ifft(fft_data))
        self.audio_data = filtered_audio

    def save_filtered_audio(self):
        filename = os.path.basename(self.file_path)
        new_path = os.path.join("assets/notes_flattened", filename)
        sf.write(new_path, self.audio_data, self.sample_rate)
        print(f"Filtered audio saved to {new_path}")

    def read_wav(self):
        audio_data, sample_rate = sf.read(self.file_path)

        # Convert from stereo to mono
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)

        # Remove DC offset
        audio_data -= np.mean(audio_data)
        self.audio_data = audio_data
        self.sample_rate = sample_rate

    def segment_audio(self, note_duration=0.5):
        # Find the number of segments, i.e. the number of characters, in the audio message
        samples_per_note = int(self.sample_rate * note_duration)
        num_segments = len(self.audio_data) // samples_per_note

        # Split the audio data into equal-length segments
        segments = np.array_split(self.audio_data, num_segments)
        return segments, samples_per_note

    def find_fund_freq(self, segment):
        fft_data = fft.fft(segment)
        freqs = fft.fftfreq(len(fft_data), 1 / self.sample_rate)

        # Ignore negative frequencies
        pos_freq = freqs[:len(freqs) // 2]
        pos_fft = np.abs(fft_data[:len(fft_data) // 2])

        # Get all frequencies that surpass the threshold
        above_threshold_idx = np.where(pos_fft > THRESHOLD)[0]
        peak_freqs = pos_freq[above_threshold_idx]
        #print(peak_freqs)

        fund_freq = " "
        if len(peak_freqs) > 0:
            fund_freq = min(piano_note_frequencies, key=lambda note: abs(piano_note_frequencies[note] - peak_freqs[0]))
            print(f"Detected note: {fund_freq}")

            #plt.figure(figsize=(12, 6))
            #plt.plot(freqs[:len(freqs) // 2], np.abs(fft_data[:len(fft_data) // 2]), color='royalblue',
            #         label='Original Spectrum')
            #plt.title('Original Spectrum')
            #plt.xlabel('Frequency (Hz)')
            #plt.ylabel('Magnitude')
            #plt.grid(True)
            #plt.show()

        return fund_freq

    def audio_to_notes(self, note_duration=0.5):
        segments, _ = self.segment_audio(note_duration)
        decoded_notes = []

        for segment in segments:
            note = self.find_fund_freq(segment)
            decoded_notes.append(note)

        # print(f"Decoded Notes: {decoded_notes}")
        return decoded_notes

    def notes_to_words(self, notes, key):

        mapping_dict = key_mappings[key]
        decoded_text = [] 

        for note in notes:
            letter_found = None
            for letter, note_values in mapping_dict.items():
                if note == note_values[0]:
                    letter_found = letter
                    break
                 
            decoded_text.append(letter_found if letter_found else "?")

        return "".join(decoded_text) 

    def play_note(self):
        sd.play(self.audio_data, self.sample_rate)

#for key in piano_note_frequencies:
#    decoder = Decoder(f'assets/notes/{key}.wav')
#    decoder.read_wav()
#    decoder.filter_low_magnitude()
#    decoder.save_filtered_audio()
# decoder = Decoder(f'assets/encoded_messages/test_C-F-G-E.wav')
# decoder.read_wav()
# decoded_notes = decoder.audio_to_notes(0.5)
# decoded_messages = decoder.notes_to_words(decoded_notes)
# print(decoded_messages)
# decoder.play_note()

