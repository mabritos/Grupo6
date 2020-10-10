from gtts import gTTS
import os

class Alarms():

    def yawn_alert():
        tts = gTTS(text='Usted acaba de bostezar, tiene  sueno?', lang='es')
        tts.save("good.mp3")
        os.system("mpg321 good.mp3")

    def text_to_speech(text):
        tts = gTTS(text=text, lang='es')
        tts.save("good.mp3")
        os.system("mpg321 good.mp3")