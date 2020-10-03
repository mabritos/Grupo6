from gtts import gTTS
import os
tts = gTTS(text='Hola  padre,que paso?  Se lleno la vecindad, esta es una prueba de voz en python', lang='es')
tts.save("good.mp3")
os.system("mpg321 good.mp3")