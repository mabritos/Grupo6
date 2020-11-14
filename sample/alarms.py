import os
import time
import threading
import queue

alarm_queue = queue.Queue()
path = os.path.dirname(os.path.realpath(__file__))

class Alarms():

    def __init__(self):
        self.last_timestamp = 0
        self.initial_timestamp = 0
        self.thread = MyThread()
        self.thread.daemon = True
        self.thread.start()
        
        
        
    def lost_face(self):
        actual_timestamp = time.time()
        distraction_detected = False
        if (actual_timestamp - self.last_timestamp > 2): #si del ultimo timestamp hasta ahora paso 1 segundo, entonces reinicio el timer
            self.initial_timestamp = actual_timestamp
            print('Reset timer alarma')
            
        elif (actual_timestamp - self.initial_timestamp > 3): #si del timestamp inicial hasta ahora pasaron mas de 5 segundos. Osea, paso 5 segundos distraido
            self.initial_timestamp = actual_timestamp
            distraction_detected = True
            self.text_to_speech('distraction_alert')
        
        self.last_timestamp = actual_timestamp
        return distraction_detected


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
        try:
            os.system("mpg321 "+path+"/"+text+".mp3")
        except:
            print("Alarma salteada") 
