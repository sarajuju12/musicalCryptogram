import numpy as np
import wave
import io
import os

class Encoder:

    def __init__(self, dict, text):
        self.dict = dict
        self.text = text
        #self.effect = effect

    # Generate a silent waveform (pause) for the given duration
    def generate_pause(self, duration, sample_rate):
        num_samples = int(sample_rate * duration)
        return np.zeros(num_samples, dtype=np.int16)
    
    def text_to_wav_enhance(self):

        sample_rate = 44100
        buffer = io.BytesIO()

        audio_data = []

        for char in self.text:

            if char == " ":  # Space mapped to an eighth note rest
                audio_data.append(self.generate_pause(0.5, sample_rate))

            note_file = self.dict.get(char.lower())  # Convert to lowercase for consistency

            if note_file:
                chord_audio = None

                for note in note_file:
                    # Path to .wav file
                    file_path = os.path.join("assets/notes_flattened", note + ".wav")
                    try:
                        with wave.open(file_path, 'rb') as wav_file:
                            frame_count = int(sample_rate * 0.5)  # duration of 16th note
                            frames = wav_file.readframes(frame_count)
                            note_audio = np.frombuffer(frames, dtype=np.int16)

                            if chord_audio is None:
                                chord_audio = note_audio
                            else:
                                chord_audio += note_audio

                            chord_audio = np.clip(chord_audio, -32768, 32767)

                    except FileNotFoundError:
                        print(f"Warning: Missing file {file_path}, skipping {char}")

                    # Immediately add the 7th note
                    seventh_note = get_7th(note, "major")  # Function to get the 7th note
                    seventh_path = os.path.join("assets/notes_flattened", seventh_note + ".wav")
                    seventh_audio = None

                    try:
                        with wave.open(seventh_path, 'rb') as seventh_wav:
                            frames = seventh_wav.readframes(frame_count)
                            seventh_audio = np.frombuffer(frames, dtype=np.int16)


                    except FileNotFoundError:
                        print(f"Warning: Missing 7th note file {seventh_path}, skipping enhancement")

                    if chord_audio is not None:
                        audio_data.append(chord_audio)
                    
                    if seventh_audio is not None:
                        audio_data.append(seventh_audio)

        if not audio_data:
            raise ValueError("No valid audio data found.")

        # Concatenate all loaded sounds
        final_audio = np.concatenate(audio_data)

        # Write to a new WAV file
        with wave.open(buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)  # 16-bit audio
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(final_audio.tobytes())

        return buffer.getvalue()

    # Function to encode text into musical notes, given a mapping dict
    def text_to_wav(self):
        sample_rate = 44100
        buffer = io.BytesIO()

        audio_data = []

        for char in self.text:

            if char == " ":  # Space mapped to an eighth note rest
                audio_data.append(self.generate_pause(0.5, sample_rate))

            note_file = self.dict.get(char.lower())  # Convert to lowercase for consistency

            if note_file:
                chord_audio = None

                for note in note_file:
                    # Path to .wav file
                    file_path = os.path.join("assets/notes_flattened", note + ".wav")
                    try:
                        with wave.open(file_path, 'rb') as wav_file:
                            frame_count = int(sample_rate * 0.5)  # duration of 16th note
                            frames = wav_file.readframes(frame_count)
                            note_audio = np.frombuffer(frames, dtype=np.int16)

                            if chord_audio is None:
                                chord_audio = note_audio
                            else:
                                chord_audio += note_audio

                            chord_audio = np.clip(chord_audio, -32768, 32767)

                    except FileNotFoundError:
                        print(f"Warning: Missing file {file_path}, skipping {char}")

                if chord_audio is not None:
                    audio_data.append(chord_audio)

        if not audio_data:
            raise ValueError("No valid audio data found.")

        # Concatenate all loaded sounds
        final_audio = np.concatenate(audio_data)

        # Write to a new WAV file
        with wave.open(buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)  # 16-bit audio
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(final_audio.tobytes())

        return buffer.getvalue()
    
    
notes = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

def get_7th(note, interval="major"):
    """Find the 7th (major or minor) of a given note like 'B3'."""
    n = note[:-1]  # Extract note (e.g., "B" from "B3")
    octave = int(note[-1])  # Extract octave (e.g., 3 from "B3")

    index = notes.index(n)  # Find index of note
    semitone_shift = 11 if interval == "major" else 10  # Shift by 11 (M7) or 10 (m7)
    
    new_index = (index + semitone_shift) % 12  # Wrap around if needed
    new_octave = octave + ((index + semitone_shift) // 12)  # Adjust octave
    
    return f"{notes[new_index]}{new_octave}"

# NOTES
# add special characters
# add legato
# add chords/notes in-between
