
class CsvHandler():

    def csv_input(car_id,event,location,speed):
            cv2.imwrite("frame.jpg", self.frame)
            with open("frame.jpg", "rb") as imageFile:
                image_aux = base64.b64encode(imageFile.read())
                image = image_aux[2:]
            with open('Datos.csv','a') as f:
                thewriter = csv.writer(f)
                location = ''+str(self.gps.get_lat()) +', '+ str(self.gps.get_lon())
                thewriter.writerow([car_id,datetime.today().strftime('%Y-%m-%d %H:%M:%S'),event,image,location,self.gps.get_speed()])
