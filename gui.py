import streamlit as st
import urllib.parse

st.set_page_config(page_title="Jarvis Web", page_icon="🤖")

st.title("🤖 Jarvis Web")
st.write("Versión segura para nube.")

# Entrada de chat
prompt = st.chat_input("Ej: 'reproduce rock' o 'busca gatos'")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt:
    # 1. Mostrar tu mensaje
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Procesar respuesta (Sin usar pywhatkit)
    response = ""
    link = ""
    
    texto_lower = prompt.lower()
    
    if "reproduce" in texto_lower:
        busqueda = texto_lower.replace("reproduce", "").strip()
        # Creamos el link manualmente
        query = urllib.parse.quote(busqueda)
        link = f"https://www.youtube.com/results?search_query={query}"
        response = f"Aquí tienes los resultados para **{busqueda}**:"
        
    elif "busca" in texto_lower:
        busqueda = texto_lower.replace("busca", "").strip()
        query = urllib.parse.quote(busqueda)
        link = f"https://www.google.com/search?q={query}"
        response = f"He buscado **{busqueda}** en Google:"
        
    else:
        response = "No entendí. Intenta 'reproduce [algo]' o 'busca [algo]'."

    # 3. Responder con Link
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
        if link:
            # Botón mágico para ir al sitio
            st.link_button("👉 Abrir Resultados", link)
