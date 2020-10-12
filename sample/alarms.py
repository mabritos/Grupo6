from gtts import gTTS
import os

class Alarms():

    def yawn_alert():
        tts = gTTS(text='Se han detectado sintmas de suenio', lang='es')
        tts.save("good.mp3")
        os.system("mpg321 good.mp3")