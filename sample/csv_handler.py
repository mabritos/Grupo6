import csv
import cv2
import base64
from datetime import datetime
import os

path = os.path.dirname(os.path.realpath(__file__))

class CsvHandler():

    def csv_input(car_id,event,location,speed, frame):
            cv2.imwrite(path+"/frame.jpg", frame)
            with open(path+"/frame.jpg", "rb") as imageFile:
                image = base64.b64encode(imageFile.read())
            with open(path+'/Datos.csv','a') as f:
                thewriter = csv.writer(f)
                thewriter.writerow([car_id,datetime.today().strftime('%Y-%m-%d %H:%M:%S'),event,image,location,speed])
                