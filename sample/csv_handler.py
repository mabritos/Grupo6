import csv
import cv2
import base64
from datetime import datetime

class CsvHandler():

    def csv_input(car_id,event,location,speed, frame):
            cv2.imwrite("frame.jpg", frame)
            with open("frame.jpg", "rb") as imageFile:
                image = base64.b64encode(imageFile.read())
            with open('Datos.csv','a') as f:
                thewriter = csv.writer(f)
                thewriter.writerow([car_id,datetime.today().strftime('%Y-%m-%d %H:%M:%S'),event,image,location,speed])
                