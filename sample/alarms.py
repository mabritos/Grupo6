from gtts import gTTS
import os
import time
import threading
import queue

alarm_queue = queue.Queue()

class Alarms():

    def __init__(self):
        self.last_timestamp = 0
        self.initial_timestamp = 0
        self.thread = MyThread()
        self.thread.daemon = True
        self.thread.start()
        
        
        
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
        print( "se a detectado un sintoma de sueno (Bostezo)" )
        self.text_to_speech("Es probable que se este durmiendo, tengan cuidado")
        
        """tts = gTTS(text='Se han detectado sintomas de suenio', lang='es')
        tts.save("good.mp3")
        os.system("mpg321 good.mp3") """

    def blink_alert(self):
        print("Se a detectado un sintoma se sueno (pestaneo)")
        self.text_to_speech("Es probable que se este durmiendo, tengan cuidado")

    def sleeping_alert(self):
        print("el conductor se ah dormido!!!!!!!")
        self.text_to_speech("Cuidado el conductor se a dormido")

    def text_to_speech(self, text):
        alarm_queue.put(text)
        
        
            
        
        
        

class MyThread(threading.Thread):
    def __init__(self):
        super(MyThread, self).__init__()

    def run(self):
        print('Thread alarma iniciado')
        while(True):
            if (alarm_queue.empty() == False):
                self.text_threaded(alarm_queue.get())

    def text_threaded(self, text):
        tts = gTTS(text=text, lang='es')
        tts.save("good.mp3")
        os.system("mpg321 good.mp3")
