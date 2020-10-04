import cv2
from face_detection import FaceDetection


face_detection = FaceDetection()
webcam = cv2.VideoCapture(0)

while True:
    # Obtenemos un nuevo frame
    _, frame = webcam.read()

    # Mandamos el frame a FaceDetection para analizarlo
    face_detection.refresh(frame)

    # Mostrar en el frame los landmarks
    face_detection.draw_landmarks()

    # Buscar sintomas de sueño
    face_detection.check_drowsiness()

    if not face_detection.face_detected:
        print("ALERTA: No se detecta ningún rostro")

    cv2.imshow("Frame", frame)
    
    if cv2.waitKey(1) == 27:
        break

