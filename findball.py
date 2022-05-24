import cv2 as cv
from math import pi
import numpy as np


# HELPER FUNCTIONS
def manhattanDistance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def ballCheck(contour):
    perimeter = cv.arcLength(contour, True)
    if perimeter == 0:  # avoid division by 0
        return 10000, False

    area = cv.contourArea(contour)
    circularity = 4 * pi * (area / (perimeter * perimeter))

    if area <= 100 or area >= 400:
        rightSize = False
    else:
        rightSize = True

    return circularity, rightSize


# MAIN FUNCTION
# TODO: FIX THIS WITH GREEN BALL
# If the ball is found, return a tuple with the x and y coordinate of the circle. Otherwise, return None.
def findBall(frame, gamestate):
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
    if len(contours) == 0:
        return None
    else:
        # If the ball hasn't been found yet, choose the contour that is most circular and within a certain area.
        if len(gamestate.ballPositions) == 0:
            ball_contour = None
            closest_circularity = None
            for contour in contours:
                circularity, rightSize = ballCheck(contour)

                if not rightSize:
                    return None

                if ball_contour is None:
                    ball_contour = contour
                    closest_circularity = circularity
                elif abs(1 - circularity) < abs(1 - closest_circularity):
                    closest_circularity = circularity
                    ball_contour = contour

            # If no ball fits the criteria wait for the next frame.
            if ball_contour is None:
                return None

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
                    closest_distance = manhattanDistance(gamestate.ballPositions[-1], ballPosition)
                    likelyContour = contour
                else:
                    tempDistance = manhattanDistance(ballPosition, gamestate.ballPositions[-1])
                    if tempDistance < closest_distance:
                        ballPosition = (int(x), int(y))
                        closest_distance = tempDistance
                        likelyContour = contour

            # Make sure this contour is likely the ping pong ball.
            circularity, rightSize = ballCheck(likelyContour)
            print("circularity", circularity)
            if not rightSize:
                return None
            if not (0.6 <= circularity <= 1.4):
                return None
            cv.circle(frame, ballPosition, int(radius), (0, 255, 0), 10)

        return ballPosition
