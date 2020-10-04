from gtts import gTTS
import os

def drowsiness_alert():
    tts = gTTS(text='Usted acaba de bostezar, tiene  sueno?', lang='es')
    tts.save("good.mp3")
    os.system("mpg321 good.mp3")