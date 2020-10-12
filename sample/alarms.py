from gtts import gTTS
import os
import time

class Alarms():

    def __init__(self):
        self.last_timestamp = 0
        self.initial_timestamp = 0

    def lost_face(self):
        actual_timestamp = time.time()
        if (actual_timestamp - self.last_timestamp > 2): #si del ultimo timestamp hasta ahora paso 1 segundo, entonces reinicio el timer
            self.initial_timestamp = actual_timestamp
            print('Reset timer alarma')
            
        elif (actual_timestamp - self.initial_timestamp > 5): #si del timestamp inicial hasta ahora pasaron mas de 5 segundos. Osea, paso 5 segundos distraido
            self.initial_timestamp = actual_timestamp
            self.text_to_speech('Por favor, no se distraiga al volante')
        
        self.last_timestamp = actual_timestamp


    def yawn_alert(self):
        tts = gTTS(text='Se han detectado sintomas de suenio', lang='es')
        tts.save("good.mp3")
        os.system("mpg321 good.mp3")

    

    def text_to_speech(self, text):
        tts = gTTS(text=text, lang='es')
        tts.save("good.mp3")
        os.system("mpg321 good.mp3")
