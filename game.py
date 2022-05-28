import math
from enum import Enum, auto
from collections import deque

import constants
import soundeffects


class GameStates(Enum):
    preServe = auto()
    serve = auto()
    gameOver = auto()
    beforeNet = auto()
    overNet = auto()
    expectingHit = auto()


# Helper for detectBounce(). Return -1 if position 1 to position 2 is going down, return 1 if it is going up.
def downOrUp(pos1, pos2):
    # Calculation is weird because for the y axis, 0 is the top and 1080 is the bottom
    delta = pos2[1] - pos1[1]
    if delta > 0:
        return -1
    elif delta < 0:
        return 1
    else:
        return 0

# Helper for detectHit(). Return -1 if position 1 to position 2 is going left, return 1 if it is going right.
def leftOrRight(pos1, pos2):
    delta = pos2[0] - pos1[0]
    if delta > 0:
        return 1
    elif delta < 0:
        return -1
    else:
        return -0

def distance(pos1, pos2):
    return math.sqrt((pos2[1]-pos1[1])**2 + (pos2[0]-pos1[0])**2)

class GameEngine:
    def __init__(self, netX, serveHeight, tableHeight, bounceCeiling, pixelsPerFeet):
        self.netX = netX
        self.serveHeight = serveHeight
        self.tableHeight = tableHeight
        self.bounceCeiling = bounceCeiling
        self.pixelsPerFeet = pixelsPerFeet

        self.currentState = GameStates.preServe

        self.ballPositions = deque(maxlen=constants.MAX_STORED_BALL_POSITIONS)
        self.downUpArray = deque(maxlen=constants.MAX_STORED_BALL_POSITIONS-1)
        self.leftRightArray = deque(maxlen=constants.MAX_STORED_BALL_POSITIONS-1)
        self.ftPerSecondArray = deque(maxlen=constants.MAX_STORED_BALL_POSITIONS-1)

        self.matchPoint = False

        self.leftIsServing = False
        self.leftIsAttacking = self.leftIsServing
        self.ballIsLeftSide = self.leftIsServing

        self.serveHeightCounter = 0
        self.timer = 0

        self.wasOffScreen = False
        self.bounced = False
        self.hit = False
        self.speed = 0 # feet per second

        self.pointHadFastShot = False
        self.fastSoundNotPlayedYet = True

        self.leftScore = 0
        self.rightScore = 0

        soundeffects.startBackgroundMusic()

    # This is the only function called by main. It takes a tuple of size 2 with the x and y coordinates of the ball.
    def updateState(self, ballPosition):
        # If ball isn't found, just don't update the ball position but still increment timers.
        if ballPosition is not None:
            self.ballPositions.append(ballPosition)
            self.detectSide(ballPosition[0])
            self.detectBounce()
            self.detectHit()
            self.detectSpeed()
            self.updateStateMachine(ballPosition[1])

            # Don't do comparisons between positions if the positions didn't immediately follow eachother.
            self.wasOffScreen = False
        else:
            self.updateStateMachine(None)
            self.wasOffScreen = True

    # Set ballSideLeft depending on the side the ball is on.
    def detectSide(self, x):
        if x <= self.netX:
            self.ballIsLeftSide = True
        else:
            self.ballIsLeftSide = False

    # Set bounced to true if ball has bounced, false if not.
    def detectBounce(self):
        if self.wasOffScreen:
            return
        elif len(self.ballPositions) > 1:
            self.downUpArray.append(downOrUp(self.ballPositions[-2], self.ballPositions[-1]))

        self.bounced = self.downUpArray == deque([-1, -1, 1, 1])

    # Returns true is ball is within the bounce zone.
    def inBounceZone(self):
        if self.bounceCeiling < self.ballPositions[-1][1] < self.tableHeight:
            return True

        return False

    # Set hit to true if ball has been hit, false if not.
    def detectHit(self):
        # TODO more accurate hit detection would look for the paddle, currently we could mess up if there's enough backspin
        if self.wasOffScreen:
            return
        elif len(self.ballPositions) > 1:
            print(self.ballPositions[-2])
            print(self.ballPositions[-1])
            self.leftRightArray.append(leftOrRight(self.ballPositions[-2], self.ballPositions[-1]))

        self.hit = self.leftRightArray == deque([-1, -1, 1, 1]) or self.leftRightArray == deque([1, 1, -1, -1])
        print(self.leftRightArray)
        print(self.hit)

    def detectSpeed(self):
        if self.wasOffScreen:
            return
        elif len(self.ballPositions) > 1:
            self.speed = distance(self.ballPositions[-2], self.ballPositions[-1]) / self.pixelsPerFeet * constants.CAMERA_FPS


    def updateStateMachine(self, y):
        if self.currentState is GameStates.gameOver:
            # TODO
            pass
        elif self.currentState is GameStates.preServe:
            # Turn on match point music if match point is triggered.
            if not self.matchPoint:
                if constants.TARGET_SCORE - self.leftScore == 1 or constants.TARGET_SCORE - self.rightScore == 1:
                    soundeffects.startMatchPointMusic()

            # If a player has won, the game is finished.
            elif self.leftScore >= constants.TARGET_SCORE or self.rightScore >= constants.TARGET_SCORE:
                soundeffects.startVictoryMusic()
                self.currentState = GameStates.gameOver

            # Initiate the game once the ball is held above a certain position for a certain amount of time.
            if y is not None and y <= self.serveHeight:
                # Play a warning if the wrong person is trying to initiate a serve.
                # if self.leftIsServing != self.ballIsLeftSide:
                #     soundeffects.playSoundServeWarning()
                # else:
                self.serveHeightCounter += 1
            if self.serveHeightCounter >= constants.SERVE_SIGNAL_TIME_FRAMES:
                self.serveHeightCounter = 0
                # Figure out who should be attacking based on the score, then initiate serve phase.
                self.leftIsAttacking = self.leftIsServing
                soundeffects.playSoundServeApproved()
                self.currentState = GameStates.serve

        elif self.currentState is GameStates.serve:
            if self.bounced:
                self.currentState = GameStates.beforeNet

        elif self.currentState is GameStates.beforeNet:
            if self.speed > constants.FAST_SPEED and self.fastSoundNotPlayedYet:
                soundeffects.playSoundFast()
                self.fastSoundNotPlayedYet = False

            # While the ball is on the side of the attacker, look for a timeout or a bounce to determine if they missed.if
            if self.leftIsAttacking == self.ballIsLeftSide:
                self.timer += 1
            else:
                self.timer = 0
                self.fastSoundNotPlayedYet = False
                self.currentState = GameStates.overNet
            if self.bounced or self.timer > constants.GAME_PHASE_TIMEOUT_FRAMES:
                self.attackerLosesPoint()


        elif self.currentState is GameStates.overNet:
            self.timer += 1

            # If the ball is hit before being bounced, the attacker wins the point.
            if self.hit:
                self.attackerWinsPoint()

            # If the ball never bounces on the other side of the court, the attacker loses the point.
            if self.timer > constants.GAME_PHASE_TIMEOUT_FRAMES:
                self.attackerLosesPoint()

            # If the ball bounces, the game continues.
            if self.bounced:
                self.timer = 0
                self.leftIsAttacking = not self.leftIsAttacking
                self.currentState = GameStates.expectingHit

        elif self.currentState is GameStates.expectingHit:
            self.timer += 1

            # If the ball bounces or is not hit in time, the new attacker loses the point.
            if self.bounced or self.timer > constants.GAME_PHASE_TIMEOUT_FRAMES:
                self.attackerLosesPoint()

            # If the ball is hit, the game continues.
            if self.hit:
                self.timer = 0
                self.currentState = GameStates.beforeNet
        else:
            print("ERROR: Invalid game state!")
            exit()

    def attackerLosesPoint(self):
        self.distributePoints(False)

    def attackerWinsPoint(self):
        self.distributePoints(True)

    def distributePoints(self, attackerWins):
        if self.pointHadFastShot:
            soundeffects.playSoundAfterGoodPoint()

        if self.leftIsAttacking == attackerWins:
            self.leftScore += 1
        else:
            self.rightScore += 1

        self.pointHadFastShot = False
        self.fastSoundNotPlayedYet = True
        self.timer = 0
        self.currentState = GameStates.preServe
        toServeMessage = self.determineServer()

        soundeffects.playSoundPreServe(self.leftScore, self.rightScore, toServeMessage)

    # Return who should serve only during serve switches.
    def determineServer(self):
        scoreSum = self.leftScore + self.rightScore
        if scoreSum % constants.POINTS_UNTIL_SWITCH == 0 and scoreSum != 0:
            self.leftIsServing = not self.leftIsServing

            if self.leftIsServing:
                return "left to serve"
            else:
                return "right to serve"
