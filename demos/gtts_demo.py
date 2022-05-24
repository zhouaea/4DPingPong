from gtts import gTTS
from playsound import playsound
import os

# The text that you want to convert to audio
mytext = 'Welcome to geeksforgeeks!'

myobj = gTTS("switch serve")

# Saving the converted audio in a mp3 file named
# welcome
myobj.save("welcome.mp3")

# Playing the converted file
playsound("../welcome.mp3")