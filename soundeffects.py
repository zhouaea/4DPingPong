from gtts import gTTS
from playsound import playsound #TODO use version 1.2.2 since it has less errors
from os import path
from pygame import mixer

import constants
import time

soundEffectsFolder = path.join("soundeffects", constants.SOUND_EFFECT_FOLDER)
ttsFolder = path.join("soundeffects", "tts")
musicFolder = path.join("music", constants.MUSIC_FOLDER)


mixer.init()

# Plays before ball is found on screen.
def startMenuMusic():
    mixer.music.stop()
    mixer.music.load(path.join(musicFolder, "menu.mp3"))
    mixer.music.play()


# Plays once ball is found on screen
def startBackgroundMusic():
    # TODO loop the background music when it stops
    mixer.music.stop()
    mixer.music.load(path.join(musicFolder, "background.mp3"))
    mixer.music.play()


# Plays once at match point.
def startMatchPointMusic():
    mixer.music.stop()
    mixer.music.load(path.join(musicFolder, "matchpoint.mp3"))
    mixer.music.play()

# Plays after match is finished.
def startVictoryMusic():
    mixer.music.stop()
    mixer.music.load(path.join(musicFolder, "victory.mp3"))
    mixer.music.play()

# Plays once match is finished.
def playSoundGameEnds():
    global soundEffectsFolder

    playsound(path.join(soundEffectsFolder, "Sample_0023.wav"), block=False)
    playsound(path.join(soundEffectsFolder, "Slow Clap.wav"), block=False)

    text = "game set match"
    file = path.join(ttsFolder, text + ".mp3")

    if not path.exists(file):
        myObj = gTTS(text)
        myObj.save(file)
    playsound(file)


# Plays before next point.
def playSoundPreServe(leftScore, rightScore, toServe):
    global soundEffectsFolder

    score = str(leftScore) + "-" + str(rightScore)
    file = path.join(ttsFolder, score + ".mp3")
    if not path.exists(file):
        myObj = gTTS(score)
        myObj.save(file)
    playsound(file, block=False)

    if toServe is not None:
        file = path.join(ttsFolder, toServe + ".mp3")
        if not path.exists(file):
            myObj = gTTS(toServe)
            myObj.save(file)
        playsound(file, block=False)


# Plays when ball is on wrong side during the serve phase.
def playSoundServeWarning():
    text = "wrong server"
    file = path.join(ttsFolder, text + ".mp3")

    if not path.exists(file):
        myObj = gTTS(text)
        myObj.save(file)
    playsound(file)


# Plays when the serve is hit
def playSoundServeApproved():
    playsound(path.join(soundEffectsFolder, "Sample_0047.wav"), block=False)


# Plays when the ball is served fast
def playSoundFast():
    playsound(path.join(soundEffectsFolder, "NiceShot1.wav"), block=False)


# Plays after a point with at least one fast shot.
def playSoundAfterGoodPoint():
    global soundEffectsFolder
    playsound(path.join(soundEffectsFolder, "CrowdWyay.wav"), block=False)

def testMusic():
    startMenuMusic()
    time.sleep(5)
    startBackgroundMusic()
    time.sleep(5)
    startMatchPointMusic()
    time.sleep(5)
    startVictoryMusic()
    time.sleep(5)

def testSounds():
    playSoundGameEnds()
    time.sleep(1)
    playSoundPreServe(0, 2, "left to serve")
    time.sleep(1)
    playSoundServeWarning()
    time.sleep(1)
    playSoundServeApproved()
    time.sleep(1)
    playSoundFast()
    time.sleep(1)
    playSoundAfterGoodPoint()

# testMusic()
