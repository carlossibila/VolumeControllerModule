import serial
import pyautogui
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume


# Configuração Turbo
APPS = {
    0: "spotify.exe",
    1: "discord.exe",
    2: "brave.exe"
}

arduino = serial.Serial('COM3', 250000, timeout=0.001) # Timeout mínimo
last_volumes = [-1, -1, -1] # Cache de volumes

def set_volume(app_idx, volume):
    sessions = AudioUtilities.GetAllSessions()
    target_app = APPS[app_idx].lower()
    
    for session in sessions:
        if session.Process and target_app in session.Process.name().lower():
            # Filtra por sessão de chamada (prioriza a ativa)
            if session.State == 1:  # 1 = Ativa
                volume_control = session.SimpleAudioVolume
                volume_control.SetMasterVolume(volume / 100, None)
                print(f"{target_app} (ativo): {volume}%", end='\r')
                return
    
    print(f"Sessão de audio não encontrada para {target_app}", end='\r')


print("Controle Ativo...")

while True:
    try:
        # Lê todas as mensagens acumuladas
        while arduino.in_waiting > 0:
            line = arduino.readline().decode().strip()
            
            if ":" in line:
                app_idx, volume = line.split(":")
                set_volume(int(app_idx), int(volume))
            elif line == "SCROLL":
                pyautogui.press('scrolllock')
                print("\nSCROLL!")
    
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Erro: {str(e)[:50]}")

arduino.close()