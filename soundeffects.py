from gtts import gTTS
from playsound import playsound #TODO use version 1.2.2 since it has less errors
from os import path
from pygame import mixer

import constants

soundEffectsFolder = path.join("soundeffects", constants.SOUND_EFFECT_FOLDER)
musicFolder = path.join("music", constants.MUSIC_FOLDER)

mixer.init()
mixer.music.load(path.join(musicFolder, "matchpoint.mp3"))
mixer.music.load(path.join(musicFolder, "victorymusic.mp3"))


def startBackgroundMusic():
    # TODO loop the background music when it stops
    mixer.music.stop()
    mixer.music.load(path.join(musicFolder, "background.mp3"))
    mixer.music.play()


def startMatchPointMusic():
    mixer.music.stop()
    mixer.music.load(path.join(musicFolder, "matchpoint.mp3"))
    mixer.music.play()


def startVictoryMusic():
    mixer.music.stop()
    mixer.music.load(path.join(musicFolder, "victorymusic.mp3"))
    mixer.music.play()


def playSoundGameEnds():
    global soundEffectsFolder

    text = "game set match"
    file = path.join(soundEffectsFolder, text + ".mp3")

    if not path.exists(file):
        myObj = gTTS(text)
        myObj.save(file)
    playsound(file)


def playSoundPreServe(leftScore, rightScore, toServe):
    global soundEffectsFolder

    score = str(leftScore) + "-" + str(rightScore)
    file = path.join(soundEffectsFolder, score + ".mp3")
    if not path.exists(file):
        myObj = gTTS(score)
        myObj.save(file)
    playsound(file, block=False)

    if toServe is not None:
        file = path.join(soundEffectsFolder, toServe + ".mp3")
        if not path.exists(file):
            myObj = gTTS(toServe)
            myObj.save(file)
        playsound(file, block=False)


def playSoundServeWarning():
    text = "wrong server"
    file = path.join(soundEffectsFolder, text + ".mp3")

    if not path.exists(file):
        myObj = gTTS(text)
        myObj.save(file)
    playsound(file)


def playSoundServeApproved():
    text = "nice serve"
    file = path.join(soundEffectsFolder, text + ".mp3")
    if not path.exists(file):
        myObj = gTTS(text)
        myObj.save(file)
    playsound(file, block=False)


def playSoundFast():
    playsound(path.join(soundEffectsFolder, "bassdrop.mp3"), block=False)

def playSoundAfterGoodPoint():
    global soundEffectsFolder
    playsound(path.join(soundEffectsFolder, "applause.mp3"), block=False)
