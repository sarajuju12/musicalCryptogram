import streamlit as st
import numpy as np
import wave
import io
import os
from assets.key_mappings import key_mappings

# Generate a silent waveform (pause) for the given duration
def generate_pause(duration, sample_rate):
    num_samples = int(sample_rate * duration)
    return np.zeros(num_samples, dtype=np.int16)

# Function to encode text into musical notes, given a mapping dict
def text_to_wav(text, dict):
    
    sample_rate = 44100
    buffer = io.BytesIO()

    audio_data = []

    for char in text:
        
        if char == " ":  # Space mapped to a quarter note rest
            audio_data.append(generate_pause(0.5, sample_rate))

        note_file = dict.get(char.lower())  # Convert to lowercase for consistency

        if note_file:
            chord_audio = None
    
            for note in note_file:
                # Path to .wav file
                file_path = os.path.join("assets/notes", note + ".wav")
                try:
                    with wave.open(file_path, 'rb') as wav_file:
                        frame_count = int(sample_rate * 0.25) # duration of 16th note
                        frames = wav_file.readframes(frame_count)
                        #audio_data.append(np.frombuffer(frames, dtype=np.int16))
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

# Function to decode WAV to text (basic implementation)
def wav_to_text(wav_data):
    with wave.open(io.BytesIO(wav_data), 'rb') as wav_file:
        raw_data = np.frombuffer(wav_file.readframes(wav_file.getnframes()), dtype=np.int16)
    # This is a placeholder function. In reality, you would implement signal analysis to extract text.
    return "Decoded text (actual decoding logic needed)"

# Streamlit UI
st.set_page_config(page_title="Musical Text Encoder/Decoder", layout="centered")

st.title("🎵 Musical Text Encoder & Decoder")

mode = st.radio("Choose Mode:", ["Encode Text to WAV", "Decode WAV to Text"])

if mode == "Encode Text to WAV":
    key = st.selectbox("Choose Encryption Key:", ["C-G-Am-F", "C-F-G-E", "Cm-Gm-Dm-Am", "Chord_1", "Chord_2"])
    text = st.text_area("Enter text to encode:")
    if st.button("Generate WAV"):
        if text:
            dict = key_mappings.get(key)
            wav_data = text_to_wav(text, dict)
            st.audio(wav_data, format="audio/wav")
            st.download_button("Download WAV", wav_data, "encoded_audio.wav", "audio/wav")
        else:
            st.warning("Please enter some text.")

elif mode == "Decode WAV to Text":
    uploaded_file = st.file_uploader("Upload WAV file", type=["wav"])
    if uploaded_file:
        wav_data = uploaded_file.read()
        decoded_text = wav_to_text(wav_data)
        st.text_area("Decoded Text:", decoded_text, height=100)


# troubles so far
# combining notes to make a chord lead to a high-pitched shrill sound
# used + instead of np.sum, works but believe experiencing clipping noise (may need to normalize)
# idea: lower decibel levels of each note, once everything is combined, normalize it

# Need to do
# create two other chords
# lower decibel levels + normalize