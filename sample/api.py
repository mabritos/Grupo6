import time
import requests
import os

path = os.path.dirname(os.path.realpath(__file__))

class Api:

    def __init__(self):
        self.initial_timestamp = 0

    def send_csv(self):
        actual_timestamp = time.time()
        if (actual_timestamp - self.initial_timestamp > 600):
            self.initial_timestamp = actual_timestamp
            
            with open(path+'/Datos.csv') as f:
                csv = f.read()
            
            data = {"csv": csv}
            url = "https://fer.demos.oxusmedia.com/ticv/api/sendCSV"
            response = requests.post(url, data)
            # print(response.text)
