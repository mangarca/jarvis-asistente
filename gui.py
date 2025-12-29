import streamlit as st
import requests
import urllib.parse
from openai import OpenAI
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder

# --- 1. CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="J.A.R.V.I.S.", page_icon="🧬", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #00FF00; }
    .stTextInput > div > div > input { background-color: #262730; color: white; }
    h1 { color: #00FFAA !important; text-shadow: 0 0 10px #00FFAA; }
    .stChatMessage { background-color: #1E1E1E; border: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

# --- 2. FUNCIONES DE AUDIO (SIN ERRORES) ---

# Hablar (Salida) - Usando API Web
def hablar(texto):
    if texto:
        try:
            texto_safe = urllib.parse.quote(texto)
            url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={texto_safe}&tl=es&client=tw-ob"
            response = requests.get(url)
            st.audio(response.content, format="audio/mp3", autoplay=True)
        except:
            pass

# Escuchar (Entrada) - Procesando grabación
def transcribir_audio(audio_bytes):
    r = sr.Recognizer()
    try:
        # Guardamos temporalmente el archivo
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_bytes)
        
        # Leemos el archivo con SpeechRecognition
        with sr.AudioFile("temp_audio.wav") as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language="es-ES")
            return text
    except Exception as e:
        return None

# --- 3. BARRA LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=80)
    st.title("⚙️ SISTEMA")
    modo = st.radio("Protocolo:", ["🧠 Inteligencia Artificial", "⚡ Comandos Rápidos"])
    if st.button("🗑️ Borrar Memoria"):
        st.session_state.messages = []
        st.rerun()

# --- 4. INTERFAZ PRINCIPAL ---
st.title("🧬 J.A.R.V.I.S. | AUDIO ACTIVO")

# Historial
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🧬"):
        st.markdown(msg["content"])

# --- 5. ZONA DE ENTRADA (MICRÓFONO + TEXTO) ---
col1, col2 = st.columns([1, 4])

prompt = None
audio_bytes = None

with col1:
    st.write("🎙️ **Hablar:**")
    # El botón del micrófono
    audio_bytes = audio_recorder(
        text="",
        recording_color="#e8b62c",
        neutral_color="#00FFAA",
        icon_size="2x",
        key="recorder"
    )

with col2:
    # La barra de texto normal
    texto_input = st.chat_input("...o escribe tu orden aquí")

# Prioridad: Si hay audio, usamos audio. Si no, texto.
if audio_bytes:
    texto_transcrito = transcribir_audio(audio_bytes)
    if texto_transcrito:
        prompt = texto_transcrito
elif texto_input:
    prompt = texto_input

# --- 6. PROCESAMIENTO ---
if prompt:
    # Usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    response = ""
    link = None
    
    # API Check
    client = None
    api_key = st.secrets.get("OPENAI_API_KEY")
    if api_key: client = OpenAI(api_key=api_key)

    # Lógica
    if modo == "🧠 Inteligencia Artificial" and client:
        try:
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "Eres JARVIS. Breve y eficiente."}, *st.session_state.messages]
            )
            response = stream.choices[0].message.content
        except:
            response = "Error de conexión neuronal."
    else:
        # Modo Comandos
        prompt_lower = prompt.lower()
        if "reproduce" in prompt_lower:
            tema = prompt_lower.replace("reproduce", "").strip()
            link = f"https://www.youtube.com/results?search_query={urllib.parse.quote(tema)}"
            response = f"Reproduciendo: {tema}"
        elif "busca" in prompt_lower:
            tema = prompt_lower.replace("busca", "").strip()
            link = f"https://www.google.com/search?q={urllib.parse.quote(tema)}"
            response = f"Buscando: {tema}"
        else:
            response = "No entendí. Intenta hablar más claro o usa comandos simples."

    # Respuesta Asistente
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant", avatar="🧬"):
        st.markdown(response)
        if link:
            st.link_button("👉 EJECUTAR", link)
        
        hablar(response)
