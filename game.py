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


# Helper for detectBounce(). Return 0 if position 1 to position 2 is going down, return 1 if it is going up.
def downOrUp(pos1, pos2):
    delta = pos2[1] - pos1[1]
    if delta > 0:
        return 1
    elif delta == 0:
        return 0
    else:
        return -1


class GameState:
    def __init__(self, netX, serveHeight):
        self.netX = netX
        self.serveHeight = serveHeight

        self.currentState = GameStates.preServe

        self.ballPositions = deque(maxlen=7)

        self.leftIsServing = True
        self.leftIsAttacking = self.leftServesFirst
        self.ballIsLeftSide = self.leftServesFirst

        self.serveHeightCounter = 0
        self.timer = 0

        self.bounced = False
        self.hit = False

        self.leftScore = 0
        self.rightScore = 0

    # Take a tuple of size 2 with the x and y coordinates of the ball.
    def updateState(self, ballPosition):
        self.ballPositions.append(ballPosition)

        self.detectSide(ballPosition[0])
        self.detectBounce()
        self.detectHit()

        self.updateStateMachine(ballPosition[1])

    def updateStateMachine(self, y):
        if self.currentState is GameStates.preServe:
            # TODO detect if wrong server is serving
            # If a player has won, the game is finished.
            if self.leftScore >= constants.TARGET_SCORE or self.rightScore >= constants.TARGET_SCORE:
                soundeffects.playSoundGameEnds()
                self.currentState = GameStates.gameOver

            # Initiate the game once the ball is held above a certain position for a certain amount of time.
            if y >= self.serveHeight:
                self.serveHeightCounter += 1
            if self.serveHeightCounter >= constants.SERVE_SIGNAL_TIME * constants.CAMERA_FPS:
                self.serveHeightCounter = 0
                # Figure out who should be attacking based on the score, then initiate serve phase.
                if self.leftIsServing:
                    self.leftIsAttacking = True
                else:
                    self.leftIsAttacking = False
                self.currentState = GameStates.serve

        elif self.currentState is GameStates.serve:
            if self.bounced:
                self.currentState = GameStates.beforeNet

        elif self.currentState is GameStates.gameOver:
            pass
            # TODO add applause + text to speech congratulating the player

        elif self.currentState is GameStates.beforeNet:
            # While the ball is on the side of the attacker, look for a timeout or a bounce to determine if they missed.
            if self.leftIsAttacking == self.ballIsLeftSide:
                self.timer += 1
                if self.bounced or self.timer > constants.GAME_PHASE_TIMEOUT:
                    self.attackerLosesPoint()
            # If the ball crosses over the net proceed to over-net stage.
            else:
                self.timer = 0
                self.currentState = GameStates.overNet

        elif self.currentState is GameStates.overNet:
            if self.bounced:
                self.timer = 0
                self.leftIsAttacking = not self.leftIsAttacking
                self.currentState = GameStates.expectingHit

            self.timer += 1

            # If the ball is hit before being bounced, the attacker wins the point.
            if self.hit:
                self.attackerWinsPoint()

            # if the ball never bounces on the other side of the court, the attacker loses the point.
            if self.timer > constants.GAME_PHASE_TIMEOUT:
                self.attackerLosesPoint()

        elif self.currentState is GameStates.expectingHit:
            if self.hit:
                self.timer = 0
                self.currentState = GameStates.beforeNet

            self.timer += 1

            # If the ball bounces or is not hit in time, the new attacker loses the point.
            if self.bounced or self.timer > constants.GAME_PHASE_TIMEOUT:
                self.attackerLosesPoint()
        else:
            print("ERROR: Invalid game state!")
            exit()

    def determineServer(self):
        sum = self.leftScore + self.rightScore
        if sum % constants.POINTS_UNTIL_SWITCH == 0 and sum != 0:
            self.leftIsServing = not self.leftIsServing

            if self.leftIsServing:
                return "left to serve"
            else:
                return "right to serve"


    # Set bounced to true if ball has bounced, false if not.
    def detectBounce(self):
        numBallPositions = len(self.ballPositions)

        if numBallPositions < 7:
            return False

        down_up_array = []
        for i in range(numBallPositions)[0:-1]:
            down_up_array.append(downOrUp(self.ballPositions[i], self.ballPositions[i + 1]))

        self.bounced = down_up_array == [-1, -1, -1, 0, 0, 0]

        if self.bounced:
            print("ball bounced")

    # Set hit to true if ball has been hit, false if not.
    def detectHit(self):
        # TODO
        pass

    # Set ballSideLeft depending on the side the ball is on.
    def detectSide(self, x):
        if x <= self.netX:
            self.ballIsLeftSide = True
        else:
            self.ballIsLeftSide = False

    def attackerLosesPoint(self):
        self.__distributePoints(False)

    def attackerWinsPoint(self):
        self.__distributePoints(True)

    def __distributePoints(self, attackerWins):
        if self.leftIsAttacking == attackerWins:
            self.leftScore += 1
        else:
            self.rightScore += 1

        self.timer = 0
        self.currentState = GameStates.preServe
        toServeMessage = self.determineServer()

        # TODO if point was "Good", play good sound
        # soundeffects.playSoundAfterPoint()
        soundeffects.playSoundPreServe(self.leftScore, self.rightScore, toServeMessage)
