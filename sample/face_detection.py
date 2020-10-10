from __future__ import division
from imutils import face_utils
from scipy.spatial import distance as dist
import cv2
import dlib
import numpy as np
import os
import time
import math
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
        self.face_angle_vertical = 0.0
        self.face_angle_horizontal = 0.0
        self.accumulator_yaw = 0.0


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
            self.raw_landmarks = self._predictor(frame, faces[0])
            self.landmarks = face_utils.shape_to_np(self.raw_landmarks)
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
    
        if self.ear < self.EYE_AR_THRESH:
            self.counter += 1

            if self.counter >= self.EYE_AR_CONSEC_FRAMES:
                cv2.putText(self.frame, "DROWSINESS ALERT!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        else:
            self.counter = 0

        if self.ear < self.EYE_AR_THRESH:
            self.blink_verification = True  
        else:
            if self.blink_verification == True:
                self.blink_verification = False
                self.blink_counter += 1
                print("Cantidad de pestaneos: ",self.blink_counter)
        
        if (self.lips_distance > self.YAWN_THRESH and self.t_end == 0):
                self.t_end = time.time() + 3
                self.yawn_counter += 1
                cv2.putText(self.frame, "Yawn Alert", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                print("Cantidad de bostezos: ", self.yawn_counter)
                Alarms.yawn_alert()
                
       
        if(time.time() > self.t_end):
            self.t_end = 0

    def head_pose_estimation(self):

        landmark_coords = np.zeros((self.raw_landmarks.num_parts, 2), dtype="int")

        # 2D model points
        image_points = np.float32([
            (self.raw_landmarks.part(30).x, self.raw_landmarks.part(30).y),  # nose
            (self.raw_landmarks.part(8).x, self.raw_landmarks.part(8).y),  # Chin
            (self.raw_landmarks.part(36).x, self.raw_landmarks.part(36).y),  # Left eye left corner
            (self.raw_landmarks.part(45).x, self.raw_landmarks.part(45).y),  # Right eye right corner
            (self.raw_landmarks.part(48).x, self.raw_landmarks.part(48).y),  # Left Mouth corner
            (self.raw_landmarks.part(54).x, self.raw_landmarks.part(54).y),  # Right mouth corner
            (self.raw_landmarks.part(27).x, self.raw_landmarks.part(27).y)
        ])

        # print(image_points)

        # 3D model points
        model_points = np.float32([
            (0.0, 0.0, 0.0),  # Nose tip
            (0.0, -330.0, -65.0),  # Chin
            (225.0, 170.0, -135.0),  # Left eye left corner
            (-225.0, 170.0, -135.0),  # Right eye right corner
            (150.0, -150.0, -125.0),  # Left Mouth corner
            (-150.0, -150.0, -125.0),  # Right mouth corner
            (0.0, 140.0, 0.0)
        ])

        frame = self.frame

        # image properties. channels is not needed so _ is to drop the value
        height, width, _ = frame.shape

        # Camera internals double
        focal_length = width
        center = np.float32([width / 2, height / 2])
        camera_matrix = np.float32([[focal_length, 0.0, center[0]],
                                        [0.0, focal_length, center[1]],
                                        [0.0, 0.0, 1.0]])
        dist_coeffs = np.zeros((4, 1), dtype="float32") #Assuming no lens distortion

        retval, rvec, tvec = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs)

        nose_end_point3D = np.float32([[50, 0, 0],
                                    [0, 50, 0],
                                    [0, 0, 50]])

        nose_end_point2D, jacobian = cv2.projectPoints(nose_end_point3D, rvec, tvec, camera_matrix, dist_coeffs)

        rotCamerMatrix, _ = cv2.Rodrigues(rvec)

        euler_angles = self.get_euler_angles(rotCamerMatrix)

        # Filter angle
        self.face_angle_vertical = (0.5 * euler_angles[0]) + (1.0 - 0.5) * self.face_angle_vertical
        self.accumulator_yaw = (0.5 * euler_angles[1]) + (1.0 - 0.5) * self.accumulator_yaw
        self.face_angle_horizontal = (0.5 * euler_angles[2]) + (1.0 - 0.5) * self.face_angle_horizontal

        euler_angles[0] = self.face_angle_vertical
        euler_angles[1] = self.accumulator_yaw
        euler_angles[2] = self.face_angle_horizontal
        
        # TODO: Draw head angles
        # renderHeadAngles(frame, rvec, tvec, camera_matrix)

        # Draw used points for head pose estimation
        # for point in image_points:
        #     print(point[0])
        #     cv2.circle(frame, (point[0], point[1]), 3, (255, 0, 255), -1)

        # Draw face angles
        pitch = "Vertical: {}".format(self.face_angle_vertical)
        yaw = "Horizontal: {}".format(self.accumulator_yaw)

        cv2.putText(self.frame, pitch, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 255), 2)
        cv2.putText(self.frame, yaw, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)

    def get_euler_angles(self, camera_rot_matrix):
        rt = cv2.transpose(camera_rot_matrix)
        shouldBeIdentity = np.matmul(rt, camera_rot_matrix)
        identity_mat = np.eye(3,3, dtype="float32")

        isSingularMatrix = cv2.norm(identity_mat, shouldBeIdentity) < 1e-6

        euler_angles = np.float32([0.0, 0.0, 0.0])
        if not isSingularMatrix:
            return euler_angles

        sy = math.sqrt(camera_rot_matrix[0,0] * camera_rot_matrix[0,0] +  camera_rot_matrix[1,0] * camera_rot_matrix[1,0]);

        singular = sy < 1e-6

        if not singular:
            x = math.atan2(camera_rot_matrix[2,1] , camera_rot_matrix[2,2])
            y = math.atan2(-camera_rot_matrix[2,0], sy)
            z = math.atan2(camera_rot_matrix[1,0], camera_rot_matrix[0,0])
        else:
            x = math.atan2(-camera_rot_matrix[1,2], camera_rot_matrix[1,1])
            y = math.atan2(-camera_rot_matrix[2,0], sy)
            z = 0

        x = x * 180.0 / math.pi
        y = y * 180.0 / math.pi
        z = z * 180.0 / math.pi

        euler_angles[0] = -x
        euler_angles[1] = y
        euler_angles[2] = z

        return euler_angles
    
    def initial_setup(self):
        Alarms.text_to_speech("Bienvenido al asistente de conducción de UNASEV, Por favor póngase en una posición cómoda de manejo y espere 5 segundos")
        time.sleep(5)
        self.head_pose_estimation()
        self.initial_face_angle_vertical = self.face_angle_vertical
        self.initial_face_angle_horizontal = self.face_angle_horizontal
        Alarms.text_to_speech("Proceso de configuración finalizado, que tenga un buen viaje")
