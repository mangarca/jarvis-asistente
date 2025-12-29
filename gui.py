import streamlit as st
import pywhatkit
import datetime

st.set_page_config(page_title="Jarvis Mobile", page_icon="📱")

st.title("📱 Jarvis Móvil")
st.write("Controla tu asistente desde la nube.")

# Entrada de texto (simula la voz)
comando = st.chat_input("Escribe una orden (ej: 'reproduce rock')")

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Mostrar historial
for m in st.session_state.mensajes:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if comando:
    # 1. Mostrar lo que dijiste
    st.session_state.mensajes.append({"role": "user", "content": comando})
    with st.chat_message("user"):
        st.write(comando)

    # 2. Procesar respuesta
    respuesta = ""
    
    if "reproduce" in comando.lower():
        tema = comando.lower().replace("reproduce", "")
        respuesta = f"Abriendo {tema} en YouTube..."
        pywhatkit.playonyt(tema) # Esto intentará abrirlo en el servidor, pero confirmamos la acción
    
    elif "hora" in comando.lower():
        hora = datetime.datetime.now().strftime("%H:%M")
        respuesta = f"Son las {hora}"
        
    elif "busca" in comando.lower():
        busqueda = comando.lower().replace("busca", "")
        respuesta = f"Buscando '{busqueda}' en Google..."
        pywhatkit.search(busqueda)
        
    else:
        respuesta = "No entendí ese comando. Intenta 'reproduce [canción]'."

    # 3. Mostrar respuesta del asistente
    st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
    with st.chat_message("assistant"):
        st.write(respuesta)
