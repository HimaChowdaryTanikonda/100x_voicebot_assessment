import streamlit as st
from openai import OpenAI
from audio_recorder_streamlit import audio_recorder
import os

# 1. Page Configuration
st.set_page_config(page_title="AI Voice Bot - 100x Assessment", page_icon="🎙️")

# 2. Initialize OpenAI Client (Secrets will be handled in Phase 4)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 3. Define the Persona (The "System Prompt")
PERSONA_PROMPT = """
You are the AI representative for a final-year Integrated M.Tech student at IIT Dhanbad. 
Graduating in May. Experience in Web Dev (TalentTrack), UI/UX (Figma), and AI projects (Expense Tracker, Sentiment Analysis).
Thesis focus: Speech emotion recognition in noisy environments.

TONE & STYLE:
- Clear, confident, and human. Not robotic.
- Thoughtful but concise.
- Professional interview style: reflective, grounded, and realistic.
- NEVER boast. Sound supportive but maintain high standards.

CORE VALUES:
- You believe unused potential is a missed opportunity.
- You push boundaries through discipline and accountability.
- Growth areas: Full-stack dev, Applied ML, and Scaling Startups.

Answer the user's questions as if YOU are this person.
"""

st.title("🎙️ 100x Gen AI Assessment")
st.write("Speak to the bot to learn about my journey and skills.")

# 4. Audio Recording UI
audio_bytes = audio_recorder(text="Click to speak...", icon_size="2x")

if audio_bytes:
    # Save audio temporarily
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_bytes)

    # A. STT: Speech-to-Text (Whisper)
    with st.spinner("Transcribing..."):
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=open("temp_audio.wav", "rb")
        )
        user_text = transcript.text
        st.chat_message("user").write(user_text)

    # B. Thinking: Chat Completion (GPT-4o)
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": PERSONA_PROMPT},
                {"role": "user", "content": user_text}
            ]
        )
        ai_response = response.choices[0].message.content
        st.chat_message("assistant").write(ai_response)

    # C. TTS: Text-to-Speech (OpenAI TTS)
    with st.spinner("Generating voice..."):
        speech_response = client.audio.speech.create(
            model="tts-1",
            voice="alloy", # 'alloy' is professional and balanced
            input=ai_response
        )
        speech_response.stream_to_file("response_audio.mp3")
        st.audio("response_audio.mp3", autoplay=True)

    # Cleanup temporary files
    os.remove("temp_audio.wav")