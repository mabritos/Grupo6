from __future__ import division
from imutils import face_utils
from scipy.spatial import distance as dist
import cv2
import dlib
import numpy as np
import os
import time
from alarms import Alarms

class FaceDetection(object):
    """Esta clase detecta un rostro y sus landmarks"""

    def __init__(self):
        """Constructor, esto es lo que se ejecuta cuando se crea un objeto de la clase FaceDetection."""
        
        self.frame = None
        self.counter = 0
        self.EYE_AR_THRESH = 0.2
        self.EYE_AR_CONSEC_FRAMES = 30
        self.YAWN_THRESH = 20
        self.face_detected = False
        self.yawn_counter = 0
        self.blink_verification = False
        self.blink_counter = 0
        self.t_end = 0 #Variable para controlar el tiempo de un bostezo
        self.BLINK_TIME_CLOSED = 1 # Tiempo en segundos para que se considere un parpadeo largo
        self.BLINK_TIME_GAP = 60 # el tiempo por el cuazl quedan guardado los parpadeos largos en el array
        self.BLINK_TIME_ALERT = 2 # cantidad de veces que se produscan pestaneos largos antes de que se dispare una alerta
        self.blink_time_alert_counter_a = [] # se guardan los moentos en que se detectaron los parpadeos largos
        self.blink_counter_verification = False #veriable que permite verificar el momento de trasiciondes de estado del ojo(de abierto a cerrado)
        self.blink_eye_closed = 0 # momento en el que se detecto que el ojo se cerro


        #_face_detector detecta rostros
        self._face_detector = dlib.get_frontal_face_detector()

        #_predictor es usado para obtener los landmarks de una cara
        self._predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    def _analyze(self):
        """Detecta un rostro y todos sus landmarks"""

        frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = self._face_detector(frame)
        self.face_detected = True if faces else False

        if self.face_detected:
            landmarks = self._predictor(frame, faces[0])
            self.landmarks = face_utils.shape_to_np(landmarks)
            self.final_ear(self.landmarks)
            self.lips_distance = self.lip_distance(self.landmarks)
        else:
            print("ALERTA: No se detecta ningún rostro")
            self.left_eye = None
            self.right_eye = None


    def refresh(self, frame):
        """Refresca el frame y lo analiza."""

        self.frame = frame
        self._analyze()
        
        
    
    def final_ear(self, shape):
        """ Setea los ojos y las orejas """

        (l_start, l_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (r_start, r_end) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

        self.left_eye = shape[l_start:l_end]
        self.right_eye = shape[r_start:r_end]

        self.left_ear = self.eye_aspect_ratio(self.left_eye)
        self.right_ear = self.eye_aspect_ratio(self.right_eye)

        self.ear = (self.left_ear + self.right_ear) / 2.0

    def eye_aspect_ratio(self, eye):
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        C = dist.euclidean(eye[0], eye[3])

        ear = (A + B) / (2.0 * C)
        return ear


    def lip_distance(self, shape):
        """Calcula la distancia entre el labio superior e inferior"""

        top_lip = shape[50:53]
        top_lip = np.concatenate((top_lip, shape[61:64]))

        low_lip = shape[56:59]
        low_lip = np.concatenate((low_lip, shape[65:68]))

        top_mean = np.mean(top_lip, axis=0)
        low_mean = np.mean(low_lip, axis=0)

        distance = abs(top_mean[1] - low_mean[1])
        return distance


    def draw_landmarks(self):
        """Dibuja en el frame los landmarks"""
        if self.face_detected:
            left_eye_hull = cv2.convexHull(self.left_eye)
            right_eye_hull = cv2.convexHull(self.right_eye)
            cv2.drawContours(self.frame, [left_eye_hull], -1, (0, 255, 0), 1)
            cv2.drawContours(self.frame, [right_eye_hull], -1, (0, 255, 0), 1)
            lip = self.landmarks[48:60]
            cv2.drawContours(self.frame, [lip], -1, (0, 255, 0), 1)

    def check_drowsiness(self):
        """Conteo de pestaneos, bostezos y detección de sueño"""

       
        self.blink_drowsiness_symptoms = 8
       
    
        if self.ear < self.EYE_AR_THRESH:
            self.counter += 1

            if self.counter >= self.EYE_AR_CONSEC_FRAMES:
                cv2.putText(self.frame, "DROWSINESS ALERT!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        else:
            self.counter = 0

        # conteo de pestaneos    

        if self.ear < self.EYE_AR_THRESH:
            self.blink_verification = True  
        else:
            if self.blink_verification == True:
                self.blink_verification = False
                self.blink_counter += 1
                print("Cantidad de pestaneos: ",self.blink_counter)
                

        # control de pestaneos largos en un tiempo a definir
        if self.ear < self.EYE_AR_THRESH:
            if self.blink_counter_verification == True :
                self.blink_counter_verification = False
                self.blink_eye_closed = time.time() + self.BLINK_TIME_CLOSED
            if time.time() >= self.blink_eye_closed and self.blink_eye_closed != 0  :
                self.blink_time_alert_counter_a.append(time.time())
                self.blink_eye_closed = 0
                print("Se subio el contador de sintomas en 1", self.blink_time_alert_counter_a)
                if len(self.blink_time_alert_counter_a) == self.BLINK_TIME_ALERT  :
                    print("usted presenta sintomas de sueno!!!")
                    self.blink_time_alert_counter_a = []
        else:
            self.blink_counter_verification = True
            self.blink_eye_closed = 0

        
        # solamente mantiene los pestaneos que se relaizaron en el intervalod de un minuto hacia atras, el resto los elimina    
        if len(self.blink_time_alert_counter_a) > 0 :
            if self.blink_time_alert_counter_a [0]  <= (time.time() - self.BLINK_TIME_GAP) :
                self.blink_time_alert_counter_a.pop(0)
                print("elimine un elemento porque paso un min", self.blink_time_alert_counter_a)


        # bostezos
        if (self.lips_distance > self.YAWN_THRESH and self.t_end == 0):
                self.t_end = time.time() + 3
                self.yawn_counter += 1
                cv2.putText(self.frame, "Yawn Alert", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                print("Cantidad de bostezos: ", self.yawn_counter)
                Alarms.yawn_alert()
               
       
        if(time.time() > self.t_end):
            self.t_end = 0