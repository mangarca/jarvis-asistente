import streamlit as st
from openai import OpenAI
import urllib.parse

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="J.A.R.V.I.S.",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS VISUALES (CSS) ---
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        color: white;
    }
    h1 {
        color: #00FFAA !important;
        font-family: 'Courier New', Courier, monospace;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=100)
    st.title("⚙️ Sistemas")
    st.markdown("---")
    
    # Selector de Modo
    modo = st.radio("Modo de Operación:", ["🧠 Inteligencia Artificial", "⚡ Comandos Rápidos"])
    
    st.markdown("---")
    st.write("Estado del servidor: **En línea 🟢**")
    if st.button("Borrar Historial"):
        st.session_state.messages = []
        st.rerun()

# --- TÍTULO PRINCIPAL ---
st.title("🧬 J.A.R.V.I.S. | Protocolo Web")
st.caption("Asistente Virtual Avanzado v2.0")

# --- GESTIÓN DE LA CLAVE DE OPENAI ---
# Intentamos buscar la clave en los secretos de Streamlit
api_key = st.secrets.get("OPENAI_API_KEY")
client = None

if api_key:
    client = OpenAI(api_key=api_key)
else:
    if modo == "🧠 Inteligencia Artificial":
        st.warning("⚠️ No se detectó API Key. Funcionando en modo limitado.")

# --- HISTORIAL DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🧬"):
        st.markdown(message["content"])

# --- LÓGICA PRINCIPAL ---
if prompt := st.chat_input("Escribe tu orden o pregunta..."):
    
    # 1. Guardar y mostrar mensaje usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # 2. PROCESAMIENTO
    response_text = ""
    link_action = None
    
    # >>> MODO IA (SI HAY CLAVE) <<<
    if modo == "🧠 Inteligencia Artificial" and client:
        try:
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres J.A.R.V.I.S., un asistente de IA útil, sarcástico y breve. Tus respuestas deben ser técnicas pero amigables."},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                stream=False
            )
            response_text = stream.choices[0].message.content
        except Exception as e:
            response_text = f"Error en el sistema neuronal: {e}"

    # >>> MODO COMANDOS (O FALLBACK) <<<
    else:
        # Lógica manual (la que ya tenías)
        prompt_lower = prompt.lower()
        
        if "reproduce" in prompt_lower:
            tema = prompt_lower.replace("reproduce", "").strip()
            query = urllib.parse.quote(tema)
            link_action = f"https://www.youtube.com/results?search_query={query}"
            response_text = f"Accediendo a la base de datos de YouTube para: **{tema}**"
        
        elif "busca" in prompt_lower:
            tema = prompt_lower.replace("busca", "").strip()
            query = urllib.parse.quote(tema)
            link_action = f"https://www.google.com/search?q={query}"
            response_text = f"Buscando información global sobre: **{tema}**"
            
        else:
            if modo == "🧠 Inteligencia Artificial":
                response_text = "Necesito la API Key para pensar. Por ahora solo puedo 'Reproducir' o 'Buscar'."
            else:
                response_text = "Comando no reconocido. Intenta: 'Reproduce [canción]' o 'Busca [algo]'."

    # 3. RESPONDER
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant", avatar="🧬"):
        st.markdown(response_text)
        if link_action:
            st.link_button("👉 Ejecutar Acción", link_action)
