import streamlit as st
import requests
import urllib.parse
from openai import OpenAI

# --- 1. CONFIGURACIÓN VISUAL (ESTILO FUTURISTA) ---
st.set_page_config(page_title="J.A.R.V.I.S.", page_icon="🧬", layout="wide")

# CSS Hacker/Matrix
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #00FF00;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        color: white;
    }
    h1 {
        color: #00FFAA !important;
        font-family: 'Courier New', Courier, monospace;
        text-shadow: 0 0 10px #00FFAA;
    }
    .stChatMessage {
        border: 1px solid #333;
        background-color: #1E1E1E;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. FUNCIÓN DE VOZ "HACKER" (INFALIBLE) ---
def hablar(texto):
    if texto:
        try:
            # Truco: Usar API web directa para evitar errores de librerías
            texto_safe = urllib.parse.quote(texto)
            url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={texto_safe}&tl=es&client=tw-ob"
            response = requests.get(url)
            # Reproductor invisible (autoplay)
            st.audio(response.content, format="audio/mp3", autoplay=True)
        except:
            pass # Si falla el audio, no rompemos la app

# --- 3. BARRA LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=80)
    st.title("⚙️ SISTEMA")
    st.write("Estado Audio: **ACTIVO** 🔊")
    
    modo = st.radio("Protocolo:", ["🧠 Inteligencia Artificial", "⚡ Comandos Rápidos"])
    
    st.markdown("---")
    if st.button("🗑️ Borrar Memoria"):
        st.session_state.messages = []
        st.rerun()

# --- 4. CEREBRO CENTRAL ---
st.title("🧬 J.A.R.V.I.S. | PRO")
st.caption("Sistema de Asistencia Avanzada v3.0")

# API Key check
api_key = st.secrets.get("OPENAI_API_KEY")
client = None
if api_key:
    client = OpenAI(api_key=api_key)

# Historial
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🧬"):
        st.markdown(msg["content"])

# --- 5. PROCESAMIENTO ---
if prompt := st.chat_input("Escribe una orden..."):
    
    # Usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    response = ""
    link = None
    
    # Lógica
    if modo == "🧠 Inteligencia Artificial" and client:
        try:
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "Eres JARVIS. Responde breve y técnico."}, *st.session_state.messages]
            )
            response = stream.choices[0].message.content
        except Exception as e:
            response = f"Error neuronal: {e}"
            
    else:
        # Modo Comandos (Gratis)
        prompt_lower = prompt.lower()
        if "reproduce" in prompt_lower:
            tema = prompt_lower.replace("reproduce", "").strip()
            link = f"https://www.youtube.com/results?search_query={urllib.parse.quote(tema)}"
            response = f"Entendido. Iniciando reproducción de: {tema}"
        elif "busca" in prompt_lower:
            tema = prompt_lower.replace("busca", "").strip()
            link = f"https://www.google.com/search?q={urllib.parse.quote(tema)}"
            response = f"Buscando información sobre: {tema}"
        else:
            response = "Comando no reconocido. Intenta 'Reproduce rock'."

    # Respuesta Asistente
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant", avatar="🧬"):
        st.markdown(response)
        if link:
            st.link_button("👉 EJECUTAR", link)
        
        # ¡AQUÍ JARVIS HABLA!
        hablar(response)
