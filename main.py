# tutorials:
# https://www.youtube.com/watch?v=RaCwLrKuS1w, basics of using opencv
# https://www.analyticsvidhya.com/blog/2020/03/ball-tracking-cricket-computer-vision/, segmenting a circle
# https://www.geeksforgeeks.org/filter-color-with-opencv/, process of color filtering
# http://people.ece.cornell.edu/land/courses/ece5760/FinalProjects/s2015/ttt/ttt/ttt/index.html, tracking game state
import cv2 as cv

from gamestate import GameState
from findball import findBall

videoCapture = cv.VideoCapture(0)

# Establish video parameters
ret, frame = videoCapture.read()
height, width = frame.shape[:2]
print("height:", height, "width:", width)
netX = width // 2
serveHeight = height // 4 * 3

# TODO Add serveheight calibration step. User can change line and then submit.

# Initialize gamestate engine.
gamestate = GameState(netX, serveHeight)

while True:
    ret, frame = videoCapture.read()
    if not ret: break

    # Draw guidelines
    cv.line(frame, (netX, 0), (netX, height), (255, 0, 255), 3)
    cv.line(frame, (0, serveHeight), (width, serveHeight), (255, 255, 0), 3)

    # Draw graphics based on game state.

    # Find the coordinates of the circle in the frame.
    ballPosition = findBall(frame, gamestate)

    # TODO Figure out what to do with gamestate if ball is not found
    # If the ball is found, update the gamestate engine.
    if ballPosition is None:
        print("no circle found")
        cv.imshow("no ball found", frame)
    else:
        gamestate.updateState(ballPosition)
        cv.imshow("ball found", frame)

    if cv.waitKey(1) == ord('q'): break

videoCapture.release()
cv.destroyAllWindows()