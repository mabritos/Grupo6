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
        self.t_end_alarm = 0
        
        
        
    def lost_face(self):
        actual_timestamp = time.time()
        distraction_detected = False
        if (actual_timestamp - self.last_timestamp > 1): #si del ultimo timestamp hasta ahora paso 3 segundo, entonces reinicio el timer
            self.initial_timestamp = actual_timestamp
            print('Reset timer alarma')
            
        elif (actual_timestamp - self.initial_timestamp > 1.5): # si del timestamp inicial hasta ahora pasaron mas de 5 segundos. Osea, paso 5 segundos distraido
            self.initial_timestamp = actual_timestamp
            
            if (self.t_end_alarm == 0):
                self.t_end_alarm = time.time() + 5
                distraction_detected = True
                self.text_to_speech('distraction_alert')
        
        self.last_timestamp = actual_timestamp
        if (time.time() > self.t_end_alarm):
            self.t_end_alarm = 0
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
