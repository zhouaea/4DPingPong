# tutorials:
# https://www.youtube.com/watch?v=RaCwLrKuS1w, basics of using opencv
# https://www.analyticsvidhya.com/blog/2020/03/ball-tracking-cricket-computer-vision/, segmenting a circle
# https://www.geeksforgeeks.org/filter-color-with-opencv/, process of color filtering
# http://people.ece.cornell.edu/land/courses/ece5760/FinalProjects/s2015/ttt/ttt/ttt/index.html, tracking game state
import cv2 as cv
import numpy as np

from game import GameEngine
from graphics import GraphicsEngine
from findball import findBall

video = 1
videoCapture = cv.VideoCapture(video, apiPreference=cv.CAP_ANY, params=[
    cv.CAP_PROP_FRAME_WIDTH, 1280,
    cv.CAP_PROP_FRAME_HEIGHT, 1024])

# Establish video parameters
ret, frame = videoCapture.read()
height, width = frame.shape[:2]
print("height:", height, "width:", width)
netX = width // 2
tableHeight = height // 3 * 2
bounceCeiling = tableHeight - 200
serveHeight = height // 4
pixelsPerFeet = width / 9 # A ping pong table is 9 feet long

# Initialize gamestate engine.
game = GameEngine(netX, serveHeight, tableHeight, bounceCeiling, pixelsPerFeet)
graphics = GraphicsEngine(height, tableHeight, width)

time = 1

while True:
    ret, frame = videoCapture.read()
    frame = cv.flip(frame, 1)

    # if not ret:
    #     videoCapture = cv.VideoCapture(video)
    #     continue

    # If recording position is messed up
    # M = np.float32([
    #     [1, 0, 0],
    #     [0, 1, -175]
    # ])
    # frame = cv.warpAffine(frame, M, (frame.shape[1], frame.shape[0]))

    # Find the coordinates of the circle in the frame.
    ballPosition = findBall(frame, tableHeight, width)

    # TODO Figure out what to do with gamestate if ball is not found
    # If the ball is found, update the gamestate engine.
    game.updateState(ballPosition)

    # Draw guidelines
    cv.line(frame, (netX, 0), (netX, height), (255, 0, 0), 3)
    cv.line(frame, (0, serveHeight), (width, serveHeight), (0, 255, 0), 3)
    cv.line(frame, (0, tableHeight), (width, tableHeight), (0, 0, 255), 3)
    cv.line(frame, (0, bounceCeiling), (width, bounceCeiling), (0, 0, 255), 3)

    # Test
    graphics.drawState(frame, game.currentState.name, game.bounced, game.hit, game.ballIsLeftSide, game.leftIsAttacking, game.speed, game.offscreen, game.timer)

    # Draw scoreboard
    graphics.drawScore(frame, game.leftScore, game.rightScore, game.leftIsServing)
    videoName = "test"
    # cv.namedWindow(videoName, cv.WINDOW_NORMAL)
    cv.imshow(videoName, frame)
    # cv.resizeWindow(videoName, int(1920 / 2), int(1080 / 2))

    key = cv.waitKey(time)
    if key == ord('q'):
        break
    elif key == ord('p'):
        if time == 1:
            time = 1
        else:
            time = 1

videoCapture.release()
cv.destroyAllWindows()
