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
    
    def text_to_wav_legato(self):
            sample_rate = 44100
            buffer = io.BytesIO()
            
            # Parameters for sustain effect
            note_duration = 0.5 
            sustain_overlap = 2  
            
            audio_data = []
            total_length = 0
            
            # First pass: calculate total length needed and prepare samples
            for char in self.text:
                if char == " ":
                    pause_samples = self.generate_pause(note_duration, sample_rate)
                    total_length += len(pause_samples)
                else:
                    note_file = self.dict.get(char.lower())
                    if note_file:
                        total_length += int(sample_rate * note_duration)
            
            # Create a single array for the entire audio
            final_audio = np.zeros(total_length, dtype=np.int16)
            
            current_pos = 0
            
            # Second pass: actually add the audio samples
            for char in self.text:
                if char == " ":
                    pause_samples = self.generate_pause(note_duration, sample_rate)
                    final_audio[current_pos:current_pos + len(pause_samples)] = pause_samples
                    current_pos += len(pause_samples)
                else:
                    note_file = self.dict.get(char.lower())
                    if note_file:
                        # For chord: load and mix all notes
                        chord_audio = None
                        
                        for note in note_file:
                            file_path = os.path.join("assets/notes_flattened", note + ".wav")
                            try:
                                with wave.open(file_path, 'rb') as wav_file:
                                   
                                    frames = wav_file.readframes(wav_file.getnframes())
                                    note_audio = np.frombuffer(frames, dtype=np.int16)
                                    
                                    # Take only the attack portion needed based on note_duration
                                    # but keep the full sustain for overlapping/legato effect
                                    attack_portion = int(sample_rate * note_duration)
                                    
                                  
                                    if len(note_audio) < attack_portion:
                                        # Pad with zeros if the sample is too short
                                        padded_audio = np.zeros(attack_portion, dtype=np.int16)
                                        padded_audio[:len(note_audio)] = note_audio
                                        note_audio = padded_audio
                                    else:
                                        # If the note is long enough, we can use the beginning portion
                                        sustain_portion = min(len(note_audio), int(sample_rate * (note_duration + sustain_overlap)))
                                        full_note = np.zeros(attack_portion, dtype=np.int16)
                                        full_note[:attack_portion] = note_audio[:attack_portion]
                                        
                                        # Apply a gradual fade to the sustain portion if it exists
                                        if sustain_portion > attack_portion:
                                            # Fading out the sustain portion
                                            fade_length = sustain_portion - attack_portion
                                            fade_curve = np.linspace(1.0, 0.0, fade_length)
                                            
                                            # Convert to float for the multiplication, then back to int16
                                            sustain_tail = (note_audio[attack_portion:sustain_portion].astype(np.float64) * fade_curve).astype(np.int16)
                                            
                                            # Add the sustain tail to the final audio (will overlap with next notes)
                                            sustain_end = min(current_pos + attack_portion + fade_length, len(final_audio))
                                            if current_pos + attack_portion < len(final_audio):
                                                add_length = sustain_end - (current_pos + attack_portion)
                                                final_audio[current_pos + attack_portion:sustain_end] += sustain_tail[:add_length]
                                        
                                        note_audio = full_note
                                    
                                    if chord_audio is None:
                                        chord_audio = note_audio
                                    else:
                                        # Ensure both arrays are the same length
                                        max_len = max(len(chord_audio), len(note_audio))
                                        if len(chord_audio) < max_len:
                                            chord_audio = np.pad(chord_audio, (0, max_len - len(chord_audio)))
                                        if len(note_audio) < max_len:
                                            note_audio = np.pad(note_audio, (0, max_len - len(note_audio)))
                                        
                                        chord_audio = chord_audio + note_audio
                                        
                                    chord_audio = np.clip(chord_audio, -32768, 32767)
                                    
                            except FileNotFoundError:
                                print(f"Warning: Missing file {file_path}, skipping {char}")
                        
                        if chord_audio is not None:
                            # Add the chord audio to the final audio at the current position
                            end_pos = min(current_pos + len(chord_audio), len(final_audio))
                            final_audio[current_pos:end_pos] += chord_audio[:end_pos - current_pos]
                            
                            # Move position forward by the regular note duration
                            current_pos += int(sample_rate * note_duration)
            
            # Clip the final audio to avoid distortion
            final_audio = np.clip(final_audio, -32768, 32767)
            
            # Write to WAV file
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
