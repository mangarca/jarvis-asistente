from core.voice import listen, talk
from skills.basic_skills import run_skill

def main():
    # Saludo inicial
    talk("Sistema iniciado. Estoy escuchando.")
    print("🟢 Sistema en línea. Di 'Terminar' para salir.")
    
    while True:
        # 1. Escuchar
        command = listen()
        
        if command:
            print(f"🎤 Usuario dijo: {command}")
            
            # 2. Comando de apagado de emergencia
            if 'terminar' in command or 'apágate' in command or 'descansa' in command:
                talk("Desconectando sistemas. Hasta luego.")
                break
            
            # 3. Buscar una habilidad que coincida
            executed = run_skill(command, talk)
            
            # 4. Si no entendió ninguna orden
            if not executed:
                talk("Lo siento, no entendí esa orden.")
        
if __name__ == "__main__":
    main()
