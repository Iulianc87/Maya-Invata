from gtts import gTTS
import os
import pygame
import time

def vorbeste(text):
    # Generăm vocea naturală de la Google
    # slow=True o face să vorbească mai rar, perfect pentru dictare
    tts = gTTS(text=text, lang='ro', slow=True)
    tts.save("dictare.mp3")
    
    # Inițializăm player-ul audio
    pygame.mixer.init()
    pygame.mixer.music.load("dictare.mp3")
    pygame.mixer.music.play()
    
    # Așteptăm până termină de citit
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
        
    # Eliberăm fișierul ca să îl putem suprascrie la următoarea dictare
    pygame.mixer.music.unload()
    os.remove("dictare.mp3")