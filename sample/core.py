import cv2
from api import Api
from face_detection import FaceDetection
from gps_data import GpsData


gps = GpsData()
face_detection = FaceDetection()
face_detection.set_gps(gps)
api = Api()


webcam = cv2.VideoCapture(0)


while face_detection.face_detected == False:
    _, frame = webcam.read()
    
    frame = cv2.resize(frame, (511,288))

    face_detection.refresh(frame)

face_detection.initial_setup()

while True:
    print(gps.get_speed())
    if (gps.get_speed() > 0):
    # Obtenemos un nuevo frame
        _, frame = webcam.read()
    
        frame = cv2.resize(frame, (511,288))
    
    # Mandamos el frame a FaceDetection para analizarlo
        face_detection.refresh(frame)

    # Mostrar en el frame los landmarks
        face_detection.draw_landmarks()

    # Buscar sintomas de sueño
        if face_detection.face_detected:
            face_detection.check_drowsiness()
            face_detection.head_pose_estimation()
            face_detection.check_distraction()

        cv2.imshow("Frame", frame)

    api.send_csv()

    if cv2.waitKey(1) == 27:
        break

