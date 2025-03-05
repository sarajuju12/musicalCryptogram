import streamlit as st
import numpy as np
import wave
import io
import os

def generate_silence(duration, sample_rate):
    """Generate a silent waveform for the given duration."""
    num_samples = int(sample_rate * duration)
    return np.zeros(num_samples, dtype=np.int16)


# Function to encode text into musical notes (mapping #1)
def text_to_wav(text, dict):
    
    sample_rate = 44100
    buffer = io.BytesIO()

    audio_data = []

    for char in text:
        
        if char == " ":  # Space should be a quarter note rest
            audio_data.append(generate_silence(0.5, sample_rate))

        note_file = dict.get(char.lower())  # Convert to lowercase for consistency
        if note_file:
            file_path = os.path.join("assets/notes", note_file + ".wav")
            try:
                with wave.open(file_path, 'rb') as wav_file:
                    # frames = wav_file.readframes(wav_file.getnframes())
                    frame_count = int(sample_rate * 0.25) # duration of 8th note
                    frames = wav_file.readframes(frame_count)
                    audio_data.append(np.frombuffer(frames, dtype=np.int16))
            except FileNotFoundError:
                print(f"Warning: Missing file {file_path}, skipping {char}")

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
    key = st.selectbox("Choose Encryption Key:", ["C-G-Am-F", "C-F-G-E", "Cm-Gm-Dm-Am"])
    text = st.text_area("Enter text to encode:")
    if st.button("Generate WAV"):
        if text:
            if key == "C-G-Am-F":
                dict = {"a": "C3", "b": "D3", "c": "E3", "d": "F3", "e": "G3", "f": "A3", "g": "B3", "h": "C4",
                        "i": "D4", "j": "E4", "k": "F4", "l": "G4", "m": "A4", "n": "B4", "o": "C5", "p": "D5",
                        "q": "E5", "r": "F5", "s": "G5", "t": "A5", "u": "B5", "v": "C6", "w": "D6", "x": "E6", "y": "F6", "z": "G6"}
            elif key == "C-F-G-E":
                dict = {"a": "C4", "b": "E5", "c": "A5", "d": "G3", "e": "D4", "f": "E3", "g": "Ab4", "h": "B4",
                        "i": "F3", "j": "C3", "k": "D3", "l": "B5", "m": "Ab5", "n": "F4", "o": "G5", "p": "B6",
                        "q": "G6", "r": "C5", "s": "E4", "t": "F5", "u": "D5", "v": "A4", "w": "E6", "x": "F6", "y": "C6", "z": "G4"}
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
