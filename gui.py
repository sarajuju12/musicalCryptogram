import streamlit as st
import numpy as np
import wave
import io
import os
from assets.key_mappings import key_mappings
from decoder import *
from llm import LLMScorer


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

        if char == " ":  # Space mapped to an eighth note rest
            audio_data.append(generate_pause(0.5, sample_rate))

        note_file = dict.get(char.lower())  # Convert to lowercase for consistency

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


# Function to decode WAV to text (basic implementation)
def wav_to_text(wav_data):
    with wave.open(io.BytesIO(wav_data), 'rb') as wav_file:
        raw_data = np.frombuffer(wav_file.readframes(wav_file.getnframes()), dtype=np.int16)
    # This is a placeholder function. In reality, you would implement signal analysis to extract text.
    return "Decoded text (actual decoding logic needed)"


# Streamlit UI
st.set_page_config(page_title="Musical Text Encoder/Decoder", layout="centered")

# ---- CUSTOM CSS ANIMATION ----
st.markdown("""
    <style>
        /* Background Color */
        html, body, .stApp {
            background-color: white;
            color: black;
            overflow: hidden;
        }
            
        .custom-title {
            font-size: 40px;
            font-weight: bold;
            text-align: center;
            margin-top: 50px;
            color: #333333;
            background: transparent;
            # transition: all 0.6s ease-in-out;
            transition: color 0.6s ease-out, transform 0.6s ease-in-out, text-shadow 0.6s ease-in-out, background 0.6s ease-in-out;
        }

        .custom-title:hover {
            background: linear-gradient(45deg, #FF6347, #FFD700); /* Gradient color on hover */
            -webkit-background-clip: text; /* Clip the background to the text */
            color: transparent; /* Make text color transparent to show the gradient */
            transform: scale(1.1); /* Slightly grow the title */
            text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2); /* Add shadow effect */
        }
            
        /* Floating Animation */
        @keyframes floatNotes {
            0% { transform: translateY(0) scale(1); opacity: 0; }    /* Start faded */
            20% { opacity: 0.75; }                                       /* Fade in */
            50% { transform: translateY(-80px) scale(1.2); opacity: 0.6; }  /* Float up */
            80% { transform: translateY(-50px) scale(1); opacity: 0.5; }                   
            100% { transform: translateY(-100px) scale(1.3); opacity: 0; } /* Fade out */
        }

        /* Notes Style */
        .note {
            bottom: 0;
            position: fixed;
            font-size: 65px;
            animation: floatNotes 7s ease-in-out infinite;
            opacity: 0;
        }

        /* Randomized Positions */
        .note:nth-child(1) { left: 5%; animation-delay: 0s; }
        .note:nth-child(2) { left: 20%; animation-delay: 1s; }
        .note:nth-child(3) { left: 35%; animation-delay: 2s; }
        .note:nth-child(4) { left: 50%; animation-delay: 1.5s; }
        .note:nth-child(5) { left: 65%; animation-delay: 2.5s; }
        .note:nth-child(6) { left: 80%; animation-delay: 0.5s; }
        .note:nth-child(7) { left: 90%; animation-delay: 3s; }

    </style>
            
    <div class="custom-title">
        🎵 CryptTunes: A Musical Text <br> Encoder & Decoder
    </div>

    <div class="music-notes">
        <div class="note">🎵</div>
        <div class="note">🎶</div>
        <div class="note">♫</div>
        <div class="note">♬</div>
        <div class="note">🎶</div>
        <div class="note">♫</div>
        <div class="note">🎵</div>
    </div>
""", unsafe_allow_html=True)

# st.title("🎵 CryptTunes: A Musical Text Encoder & Decoder")

mode = st.radio("Choose Mode:", ["Encode Text to WAV", "Decode WAV to Text"])

if mode == "Encode Text to WAV":
    key = st.selectbox("Choose Encryption Key:", ["C-G-Am-F", "C-F-G-E", "Cm-Gm-Dm-Am", "Chord_1", "Chord_2"])
    text = st.text_area("Enter text to encode:")
    filename = st.text_input("Enter filename:", placeholder="encoded_audio")

    if not filename:
        filename= "encoded_audio"

    if st.button("Generate WAV"):
        if text:
            dict = key_mappings.get(key)
            wav_data = text_to_wav(text, dict)
            st.audio(wav_data, format="audio/wav")
            st.download_button("Download WAV", wav_data, f"{filename}.wav", "audio/wav")
        else:
            st.warning("Please enter some text.")

elif mode == "Decode WAV to Text":
    llm_scorer = LLMScorer()
    keys = ["C-G-Am-F", "C-F-G-E", "Cm-Gm-Dm-Am", "Chord_1", "Chord_2"]
    # key = st.selectbox("Choose Decryption Key:", ["C-G-Am-F", "C-F-G-E", "Cm-Gm-Dm-Am", "Chord_1", "Chord_2"])
    uploaded_file = st.file_uploader("Upload WAV file", type=["wav"])
    if uploaded_file:
        decoder = Decoder(uploaded_file)
        decoder.read_wav()
        all_decoded_words = []
        for key in keys:
            decoded_notes = decoder.audio_to_notes(0.5)
            decoded_text = decoder.notes_to_words(decoded_notes, key)
            all_decoded_words.append(decoded_text)
        # Use LLM to get the best text
        best_text, scores = llm_scorer.get_best_text(all_decoded_words)
        sorted_words = [word for word, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)]
        # Format the output text
        output_text = "\n".join(sorted_words)
        # Display Results
        st.text_area("Ranked Decoded Text (Most Likely at Top):", output_text, height=150)

        # decoded_text = f"Best Decoded Text: {best_text}\n\nScores: {scores}"
        # st.text_area("Decoded Text: ", decoded_text, height=100)
        # print(decoded_messages)
        # decoder.play_note()
        # wav_data = uploaded_file.read()
        # decoded_text = wav_to_text(wav_data)
        # st.text_area("Decoded Text:", decoded_text, height=100)