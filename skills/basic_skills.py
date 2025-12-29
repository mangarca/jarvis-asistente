import pywhatkit
import datetime
import webbrowser
import os
import platform

def run_skill(command, talk_func):
    """
    Decide qué hacer basándose en lo que escuchó
    """
    # 1. Reproducir en YouTube
    if 'reproduce' in command:
        song = command.replace('reproduce', '')
        talk_func(f"Reproduciendo {song}")
        pywhatkit.playonyt(song)
        return True

    # 2. Buscar en Google
    elif 'busca' in command:
        search = command.replace('busca', '')
        talk_func(f"Buscando {search} en Google")
        pywhatkit.search(search)
        return True

    # 3. Decir la hora
    elif 'hora' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk_func(f"Son las {time}")
        return True

    # 4. Abrir Spotify
    elif 'abre spotify' in command:
        talk_func("Abriendo Spotify")
        if platform.system() == "Windows":
            os.system("start spotify")
        elif platform.system() == "Darwin": # Mac
            os.system("open -a Spotify")
        else:
            webbrowser.open("https://open.spotify.com")
        return True

    return False
