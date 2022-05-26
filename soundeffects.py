from gtts import gTTS
from playsound import playsound
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
    myObj = gTTS(text)
    file = path.join(soundEffectsFolder, text + "mp3")
    myObj.save(file)
    playsound(file)


def playSoundPreServe(leftScore, rightScore, toServe):
    global soundEffectsFolder

    score = str(leftScore) + "-" + str(rightScore)
    myObj = gTTS(score)
    file = path.join(soundEffectsFolder, score + ".mp3")
    myObj.save(file)
    playsound(file)

    if toServe is not None:
        myObj = gTTS(toServe)
        file = path.join(soundEffectsFolder, toServe + ".mp3")
        myObj.save(file)
        playsound(file)


def playSoundServeWarning():
    warning = "wrong server"
    myObj = gTTS(warning)
    file = path.join(soundEffectsFolder, warning + ".mp3")
    myObj.save(file)
    playsound(file)


def playSoundServeApproved():
    playsound(path.join(soundEffectsFolder, "ready.mp3"))


def playSoundAfterGoodPoint():
    global soundEffectsFolder
    playsound(path.join(soundEffectsFolder, "applause.mp3"))


def fastShot():
    pass

playSoundServeWarning()