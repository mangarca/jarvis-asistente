import streamlit as st
import sys
import subprocess

st.title("🛠️ Diagnóstico de Voz")

# 1. Intentamos importar la librería
try:
    from gTTS import gTTS
    st.success("✅ La librería gTTS se instaló correctamente.")
    
    # Prueba de audio
    texto = st.text_input("Escribe algo para hablar:", "Hola, soy Jarvis.")
    if st.button("🔊 Probar Voz"):
        tts = gTTS(text=texto, lang='es')
        tts.save("prueba.mp3")
        st.audio("prueba.mp3", autoplay=True)
        
except ImportError as e:
    st.error(f"❌ ERROR CRÍTICO: {e}")
    st.warning("Esto significa que la instalación falló.")

# 2. Ver qué hay instalado realmente (Chismoso)
st.markdown("---")
if st.checkbox("Ver lista de instalados"):
    result = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True)
    st.code(result.stdout)
