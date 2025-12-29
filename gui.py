import streamlit as st
from openai import OpenAI
import urllib.parse
from gTTS import gTTS
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder
import os

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="J.A.R.V.I.S.", page_icon="🎙️", layout="wide")

# Estilos CSS
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #00FF00; }
    h1 { color: #00FFAA !important; text-shadow: 0 0 10px #00FFAA; }
</style>
""", unsafe_allow_html=True)

# Función para hablar (Texto a Voz)
def hablar(texto):
    if texto:
        try:
            tts = gTTS(text=texto, lang='es')
            tts.save("respuesta.mp3")
            st.audio("respuesta.mp3", format="audio/mp3", autoplay=True)
        except:
            st.warning("No pude generar el audio.")

# Función para escuchar (Audio a Texto)
def escuchar_audio(audio_bytes):
    r = sr.Recognizer()
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_bytes)
    
    with sr.AudioFile("temp_audio.wav") as source:
        audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data, language="es-ES")
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None

# --- 2. BARRA LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=80)
    st.title("SISTEMA")
    modo = st.radio("Modo:", ["⚡ Comandos Rápidos", "🧠 IA (Requiere Saldo)"])
    if st.button("🗑️ Reiniciar"):
        st.session_state.messages = []
        st.rerun()

# --- 3. INTERFAZ PRINCIPAL ---
st.title("🎙️ J.A.R.V.I.S. | VOZ ACTIVADA")

# Historial
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])

# --- 4. ENTRADA DE DATOS (TEXTO O VOZ) ---
prompt = st.chat_input("Escribe aquí...")
audio_bytes = None

# Solo mostramos el micrófono en Comandos Rápidos (o en ambos si quieres)
if modo == "⚡ Comandos Rápidos":
    st.write("🎤 **Presiona para hablar:**")
    audio_bytes = audio_recorder(text="", recording_color="#e8b62c", neutral_color="#00FFAA", icon_size="2x")

# Procesar Voz
if audio_bytes:
    texto_voz = escuchar_audio(audio_bytes)
    if texto_voz:
        prompt = texto_voz  # Convertimos lo que hablaste en el comando

# --- 5. LÓGICA DEL ASISTENTE ---
if prompt:
    # Mostrar usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    response = ""
    link = None
    usar_voz = False

    # >>> MODO COMANDOS RÁPIDOS <<<
    if modo == "⚡ Comandos Rápidos":
        prompt_lower = prompt.lower()
        usar_voz = True # Queremos que hable en este modo
        
        if "reproduce" in prompt_lower:
            tema = prompt_lower.replace("reproduce", "").strip()
            query = urllib.parse.quote(tema)
            link = f"https://www.youtube.com/results?search_query={query}"
            response = f"Entendido. Reproduciendo {tema} en YouTube."
        
        elif "busca" in prompt_lower:
            tema = prompt_lower.replace("busca", "").strip()
            query = urllib.parse.quote(tema)
            link = f"https://www.google.com/search?q={query}"
            response = f"Buscando {tema} en Google."
            
        elif "hora" in prompt_lower:
            import datetime
            hora = datetime.datetime.now().strftime("%I:%M %p")
            response = f"Son las {hora}."
            
        else:
            response = "No entendí. Intenta decir: 'Reproduce rock' o 'Busca gatos'."

    # >>> MODO IA (Necesita saldo) <<<
    else:
        # Aquí iría tu código de OpenAI si tuvieras saldo
        response = "Modo IA desactivado por falta de saldo. Usa Comandos Rápidos."

    # Responder
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(response)
        if link:
            st.link_button("👉 ABRIR RESULTADOS", link)
        
        # ACTIVA LA VOZ AQUÍ
        if usar_voz:
            hablar(response)
