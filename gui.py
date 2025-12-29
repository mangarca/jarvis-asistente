import streamlit as st
import requests
import urllib.parse
from openai import OpenAI

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Jarvis Voz", page_icon="🎙️")
st.title("🎙️ J.A.R.V.I.S. | Módulo de Voz")

# --- FUNCIÓN HACKER DE VOZ (Sin usar gTTS) ---
def hablar_directo(texto):
    if texto:
        try:
            # Codificamos el texto para URL (ej: "hola mundo" -> "hola%20mundo")
            texto_safe = urllib.parse.quote(texto)
            # Usamos la API oculta de Google Translate directamente
            url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={texto_safe}&tl=es&client=tw-ob"
            
            # Descargamos el audio en memoria
            response = requests.get(url)
            
            # Lo reproducimos directamente
            st.audio(response.content, format="audio/mp3", autoplay=True)
        except Exception as e:
            st.error(f"Error de conexión: {e}")

# --- INTERFAZ DE PRUEBA ---
st.write("Escribe algo y presiona Enter. Jarvis lo dirá usando conexión directa.")

prompt = st.chat_input("Escribe aquí para que Jarvis hable...")

if prompt:
    # Mostrar mensaje usuario
    with st.chat_message("user"):
        st.write(prompt)
    
    # Respuesta de Jarvis
    respuesta = f"Dijiste: {prompt}"
    
    with st.chat_message("assistant"):
        st.write(respuesta)
        # ¡Aquí ocurre la magia!
        hablar_directo(respuesta)
