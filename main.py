# tutorials:
# https://www.youtube.com/watch?v=RaCwLrKuS1w, basics of using opencv
# https://www.analyticsvidhya.com/blog/2020/03/ball-tracking-cricket-computer-vision/, segmenting a circle
# https://www.geeksforgeeks.org/filter-color-with-opencv/, process of color filtering
# http://people.ece.cornell.edu/land/courses/ece5760/FinalProjects/s2015/ttt/ttt/ttt/index.html, tracking game state


import cv2 as cv
import numpy as np
from pynput.keyboard import Listener, Key
from collections import deque
from enum import Enum, auto
from math import pi

videoCapture = cv.VideoCapture(0)


# Constants
TARGET_SCORE = 21


# State of the game.
class GameStates(Enum):
    preServe = auto()
    serve = auto()
    gameOver = auto()
    beforeNet = auto()
    overNet = auto()
    expectingHit = auto()


gameState = GameStates.preServe

ballPositions = deque(maxlen=7)
ballSideLeft = True
bounced = False

serveHeightCounter = 0 # assuming 30fps

p1Score = 0
p2Score = 0


# Establish video parameters
ret, frame = videoCapture.read()
height, width = frame.shape[:2]
print("height:", height, "width:", width)
netX = width // 2
serveHeight = height // 4 * 3


# Extra functions
def manhattanDistance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


# Return stats about the ball.
def ballCheck(contour):
    perimeter = cv.arcLength(contour, True)
    if perimeter == 0: # avoid division by 0
        return 10000, False

    area = cv.contourArea(contour)
    circularity = 4 * pi * (area / (perimeter * perimeter))

    if area <= 100 or area >= 400:
        rightSize = False
    else:
        rightSize = True

    return circularity, rightSize


# Set ballSideLeft depending on the side the ball is on.
def detectSide(x):
    global ballSideLeft
    global netX
    if x <= netX:
        ballSideLeft = True
    else:
        ballSideLeft = False


# Return 0 if position 1 to position 2 is going down, return 1 if it is going up.
def downOrUp(pos1, pos2):
    delta = pos2[1] - pos1[1]
    if delta > 0:
        return 1
    elif delta == 0:
        return 0
    else:
        return -1


# Set bounced to true if ball has bounced, false if not.
def detectBounce():
    global bounced
    global ballPositions
    numBallPositions = len(ballPositions)

    if numBallPositions < 7:
        return False

    down_up_array = []
    for i in range(numBallPositions)[0:-1]:
        down_up_array.append(downOrUp(ballPositions[i], ballPositions[i + 1]))

    bounced = down_up_array == [-1, -1, -1, 0, 0, 0]

    if bounced:
        print("ball bounced")


# Read arrow keys in background to adjust the net.
def onPress(key):
    global netX
    global serveHeight
    if key == Key.right:  # If space was pressed, write a space
        netX += 1
    elif key == Key.left:  # If enter was pressed, write a new line
        netX -= 1
    elif key == Key.up:
        serveHeight += 1
    elif key == Key.down:
        serveHeight -= 1


listener = Listener(on_press=onPress)
listener.start()

while True:
    ret, frame = videoCapture.read()
    cv.line(frame, (netX, 0), (netX, height), (255, 0, 255), 3)
    cv.line(frame, (0, serveHeight), (width, serveHeight), (255, 255, 0), 3)
    if not ret: break

    # Gaussian blur, the larger the kernel size the more blurred, not sure what sigma x is.
    blurFrame = cv.GaussianBlur(frame, (17, 17), 0)

    # Filter by orange
    hsv = cv.cvtColor(blurFrame, cv.COLOR_BGR2HSV)
    lower_orange = np.array([11, 119, 226])
    upper_orange = np.array([25, 255, 255])
    mask = cv.inRange(hsv, lower_orange, upper_orange)

    # Get contours of mask.
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # Figure out which contour is the ball if contours are found.
    if len(contours) > 0:
        # If the ball hasn't been found yet, choose the contour that is most circular and within a certain area.
        if len(ballPositions) == 0:
            ball_contour = None
            closest_circularity = None
            for contour in contours:
                circularity, rightSize = ballCheck(contour)

                if not rightSize:
                    continue

                if ball_contour is None:
                    ball_contour = contour
                    closest_circularity = circularity
                elif abs(1 - circularity) < abs(1 - closest_circularity):
                    closest_circularity = circularity
                    ball_contour = contour

            # If no ball fits the criteria wait for the next frame.
            if ball_contour is None:
                continue

            # Convert chosen contour into circle.
            (x, y), radius = cv.minEnclosingCircle(ball_contour)
            ballPosition = (int(x), int(y))
            radius = int(radius)
            cv.circle(frame, ballPosition, radius, (0, 255, 0), 10)
        # If the ball has been found previously, choose contour that is closest to that previous location
        else:
            ballPosition = None
            closest_distance = None
            likelyContour = None
            for contour in contours:
                (x, y), radius = cv.minEnclosingCircle(contour)
                if ballPosition is None:
                    ballPosition = (int(x), int(y))
                    closest_distance = manhattanDistance(ballPositions[-1], ballPosition)
                    likelyContour = contour
                else:
                    tempDistance = manhattanDistance(ballPosition, ballPositions[-1])
                    if tempDistance < closest_distance:
                        ballPosition = (int(x), int(y))
                        closest_distance = tempDistance
                        likelyContour = contour

            # Make sure this contour is likely the ping pong ball.
            circularity, rightSize = ballCheck(likelyContour)
            print("circularity", circularity)
            if not rightSize:
                continue
            if not (0.6 <= circularity <= 1.4):
                continue
            cv.circle(frame, ballPosition, int(radius), (0, 255, 0), 10)

        # Store position of circle and update states.
        ballPositions.append(ballPosition)
        detectBounce()
        detectSide(ballPosition[0])

    cv.imshow("circle", frame)


    # With circle information, determine game state.
    # if gameState is GameStates.preServe:
    #     if p1Score >= TARGET_SCORE or p2Score >= TARGET_SCORE:
    #         gameState = GameStates.gameOver
    #
    #     if y >= serveHeight:
    #         serveHeightCounter += 1
    #     if serveHeightCounter >= 90:
    #         serveHeightCounter = 0
    #         gameState = GameStates.serve
    #
    # elif gameState is GameStates.serve:
    #     if bounced:
    #         gameState = GameStates.beforeNet
    #
    # elif gameState is GameStates.gameOver:
    #     if
    #
    # elif gameState is GameStates.beforeNet:
    #
    # elif gameState is GameStates.overNet:
    #
    # elif gameState is GameStates.expectingHit:
    #
    # elif gameState is GameStates.preServe:
    #
    # else:
    #     print("ERROR: Invalid game state!")
    #     exit()

    if cv.waitKey(1) == ord('q'): break

videoCapture.release()
cv.destroyAllWindows()
