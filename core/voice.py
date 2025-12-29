import speech_recognition as sr
import pyttsx3

# --- Configuración inicial de la voz ---
engine = pyttsx3.init()

# Intentamos poner una voz en español si el sistema tiene una
try:
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'spanish' in voice.name.lower() or 'es-es' in voice.id.lower():
            engine.setProperty('voice', voice.id)
            break
except:
    pass # Si falla, usa la voz por defecto

# --- Funciones Principales ---

def talk(text):
    """Hace que el asistente hable en voz alta"""
    if text:
        print(f"🤖 Asistente: {text}")
        engine.say(text)
        engine.runAndWait()

def listen():
    """Escucha el micrófono y devuelve el texto entendido"""
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("👂 Escuchando... (Habla ahora)")
            # Calibrar el ruido de fondo por 0.5 segundos
            listener.adjust_for_ambient_noise(source, duration=0.5)
            
            # Escuchar
            voice = listener.listen(source, timeout=5)
            
            # Convertir voz a texto usando Google
            command = listener.recognize_google(voice, language='es-ES')
            return command.lower()
            
    except sr.WaitTimeoutError:
        return None
    except sr.UnknownValueError:
        # No entendió lo que se dijo
        return None
    except sr.RequestError:
        print("🔴 Error: Sin conexión a internet para el reconocimiento de voz")
        return None
    except Exception as e:
        print(f"🔴 Error: {e}")
        return None
