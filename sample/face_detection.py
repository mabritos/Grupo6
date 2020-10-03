from imutils import face_utils
from scipy.spatial import distance as dist
import cv2
import dlib

class FaceDetection(object):
    """Esta clase detecta un rostro y sus landmarks"""

    def __init__(self):
        """Constructor, esto es lo que se ejecuta cuando se crea un objeto de la clase FaceDetection.
            Se crean todos sus atributos y se setean en None por default"""
        self.frame = None

        #_face_detector detecta rostros
        self._face_detector = dlib.get_frontal_face_detector()

        #_predictor es usado para obtener los landmarks de una cara
        self._predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    def _analyze(self):
        """Detecta un rostro"""

        frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = self._face_detector(frame)
        
        try:
            landmarks = self._predictor(frame, faces[0])
            self.landmarks = face_utils.shape_to_np(landmarks)

        except IndexError:
            self.eye_left = None
            self.eye_right = None


    def refresh(self, frame):
        """Refresca el frame y lo analiza."""

        self.frame = frame
        self._analyze()


    def final_ear(self, shape):
        (l_start, l_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (r_start, r_end) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

        self.left_eye = shape[l_start:l_end]
        self.right_eye = shape[r_start:r_end]

        self.left_ear = eye_aspect_ratio(self.left_eye)
        self.right_ear = eye_aspect_ratio(self.right_eye)

        self.ear = (self.left_ear + self.right_ear) / 2.0

    def eye_aspect_ratio(self, eye):
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        C = dist.euclidean(eye[0], eye[3])

        ear = (A + B) / (2.0 * C)
        return ear

        