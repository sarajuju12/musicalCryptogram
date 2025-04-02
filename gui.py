import streamlit as st
from assets.key_mappings import key_mappings
from encoder import *
from decoder import *
from llm import LLMScorer

# Streamlit UI
st.set_page_config(page_title="Musical Text Encoder/Decoder", layout="centered")

# Custom CSS
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

mode = st.radio("Choose Mode:", ["Encode Text to WAV", "Decode WAV to Text"])

if mode == "Encode Text to WAV":
    key = st.selectbox("Choose Encryption Key:", ["C-G-Am-F", "C-F-G-E", "Cm-Gm-Dm-Am", "Chord_1", "Chord_2", "Combo_1", "Combo_2"])
    effect = st.selectbox("Choose Effect:", ["None", "Legato"])
    text = st.text_area("Enter text to encode:")
    filename = st.text_input("Enter filename:", placeholder="encoded_audio")

    if not filename:
        filename= "encoded_audio"

    if st.button("Generate WAV"):
        if text:
            dict = key_mappings.get(key)
            encoder = Encoder(dict, text)
            if effect == "Legato":
                wav_data = encoder.text_to_wav_legato()
            else:
                wav_data = encoder.text_to_wav()
            st.audio(wav_data, format="audio/wav")
            st.download_button("Download WAV", wav_data, f"{filename}.wav", "audio/wav")
        else:
            st.warning("Please enter some text.")

elif mode == "Decode WAV to Text":
    llm_scorer = LLMScorer()
    keys = ["C-G-Am-F", "C-F-G-E", "Cm-Gm-Dm-Am", "Chord_1", "Chord_2", "Combo_1", "Combo_2"]
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