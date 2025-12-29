import streamlit as st
from openai import OpenAI
from gTTS import gTTS
import os

st.set_page_config(page_title="J.A.R.V.I.S.", page_icon="🔊")

st.title("🔊 Prueba de Voz")

def hablar(texto):
    try:
        tts = gTTS(text=texto, lang='es')
        tts.save("audio_prueba.mp3")
        st.audio("audio_prueba.mp3", autoplay=True)
    except Exception as e:
        st.error(f"Error de audio: {e}")

prompt = st.chat_input("Escribe algo para que yo lo diga...")

if prompt:
    st.write(f"Dijiste: {prompt}")
    hablar(prompt)
