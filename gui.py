import streamlit as st
import os

# Configuración de la página
st.set_page_config(page_title="Jarvis Control", page_icon="🤖", layout="centered")

st.title("🤖 Panel de Control Jarvis")
st.write("Interfaz de mando para tu asistente personal.")

# Sección de Estado
st.info("Estado: El núcleo de voz debe ejecutarse en la terminal del PC.")

# Sección de Comandos Manuales
st.subheader("📝 Enviar Orden Manual")
comando = st.text_input("Escribe una orden (ej: 'reproduce rock', 'hora'):")

if st.button("Ejecutar Orden"):
    if comando:
        st.success(f"Enviando orden: {comando}")
        # Aquí simulamos la ejecución. En una versión avanzada, 
        # esto guardaría el comando en un archivo que main.py leería.
        st.write("✅ Comando procesado (Simulación web)")
    else:
        st.warning("Escribe algo primero.")

st.markdown("---")
st.subheader("📚 Habilidades Disponibles")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Multimedia**")
    st.markdown("- 📺 YouTube")
    st.markdown("- 🎵 Spotify")

with col2:
    st.markdown("**Utilidades**")
    st.markdown("- 🔍 Google Search")
    st.markdown("- ⏰ Hora actual")
