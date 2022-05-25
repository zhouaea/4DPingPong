from gtts import gTTS
from playsound import playsound
from os import path

myobj = gTTS("left to serve")
myobj.save("music/test/lefttoserve.mp3")
