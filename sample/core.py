import cv2
from face_detection import FaceDetection


face_detection = FaceDetection()

webcam = cv2.VideoCapture(0)

while face_detection.face_detected == False:
    _, frame = webcam.read()

    face_detection.refresh(frame)

face_detection.initial_setup()

while True:
    # Obtenemos un nuevo frame
    _, frame = webcam.read()

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

    if cv2.waitKey(1) == 27:
        break

