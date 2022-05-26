# tutorials:
# https://www.youtube.com/watch?v=RaCwLrKuS1w, basics of using opencv
# https://www.analyticsvidhya.com/blog/2020/03/ball-tracking-cricket-computer-vision/, segmenting a circle
# https://www.geeksforgeeks.org/filter-color-with-opencv/, process of color filtering
# http://people.ece.cornell.edu/land/courses/ece5760/FinalProjects/s2015/ttt/ttt/ttt/index.html, tracking game state
import cv2 as cv

from game import GameEngine
from graphics import GraphicsEngine
from findball import findBall

video = "1.mp4"
videoCapture = cv.VideoCapture(video)

# Establish video parameters
ret, frame = videoCapture.read()
height, width = frame.shape[:2]
print("height:", height, "width:", width)
netX = width // 2
tableHeight = height // 3 * 2
serveHeight = height // 4

# Initialize gamestate engine.
game = GameEngine(netX, serveHeight)
graphics = GraphicsEngine(height, tableHeight, width)

while True:
    ret, frame = videoCapture.read()
    if not ret:
        videoCapture = cv.VideoCapture(video)
        continue

    # Find the coordinates of the circle in the frame.
    ballPosition = findBall(frame, game.ballPositions)

    # TODO Figure out what to do with gamestate if ball is not found
    # If the ball is found, update the gamestate engine.
    # if ballPosition is None:
    #     print("no circle found")
    #     videoName = "no ball found"
    # else:
    #     game.updateState(ballPosition)
    #     videoName = "ball found"

    # Draw guidelines
    cv.line(frame, (netX, 0), (netX, height), (255, 0, 0), 3)
    cv.line(frame, (0, serveHeight), (width, serveHeight), (0, 255, 0), 3)
    cv.line(frame, (0, tableHeight), (width, tableHeight), (0, 0, 255), 3)

    # Draw scoreboard
    # graphics.drawScore(frame, game.leftScore, game.rightScore, game.leftIsServing)
    videoName = "test"
    cv.namedWindow(videoName, cv.WINDOW_NORMAL)
    cv.imshow(videoName, frame)
    cv.resizeWindow(videoName, int(1920 / 1.25), int(1080 / 1.25))

    if cv.waitKey() == ord('q'):
        break

videoCapture.release()
cv.destroyAllWindows()
