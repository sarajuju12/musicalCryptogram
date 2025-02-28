import streamlit as st
import numpy as np
import wave
import io

# Function to encode text into musical notes
def text_to_wav(text):
    sample_rate = 44100  
    duration = 0.5  # seconds per character
    freq_map = {chr(i): 220 + (i % 26) * 20 for i in range(32, 127)}  # ASCII mapped to frequencies
    signal = np.concatenate([
        np.sin(2 * np.pi * freq_map[char] * np.linspace(0, duration, int(sample_rate * duration))) for char in text
    ])

    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes((signal * 32767).astype(np.int16).tobytes())

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
    text = st.text_area("Enter text to encode:")
    if st.button("Generate WAV"):
        if text:
            wav_data = text_to_wav(text)
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
