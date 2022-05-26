import cv2 as cv
from math import pi
import numpy as np


# HELPER FUNCTIONS
def manhattanDistance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def ballStats(contour):
    if contour is None:
        return None, None

    perimeter = cv.arcLength(contour, True)
    if perimeter == 0:  # avoid division by 0
        return None, None
    area = cv.contourArea(contour)
    circularity = 4 * pi * (area / (perimeter * perimeter))
    return circularity, area

# Note: Circularity is not a good measure of the ball on low fps fast shots.
def ballCheck(circularity, area, debug=False):
    if debug:
        print(area)

    if area is None:
        return False

    if area < 500:
        return False

    return True


# MAIN FUNCTION
# TODO: FIX THIS WITH GREEN BALL
# If the ball is found, return a tuple with the x and y coordinate of the circle. Otherwise, return None.
def findBall(frame, ballPositions):
    # Gaussian blur, the larger the kernel size the more blurred, not sure what sigma x is.
    blurFrame = cv.GaussianBlur(frame, (17, 17), 0)

    # Filter by green
    hsv = cv.cvtColor(blurFrame, cv.COLOR_BGR2HSV)
    lower_green = np.array([35, 33, 117])
    upper_green = np.array([57, 255, 255])
    mask = cv.inRange(hsv, lower_green, upper_green)

    # Get contours of mask.
    retrieval_method = cv.RETR_EXTERNAL # we only want the outside of the ball
    contours, hierarchy = cv.findContours(mask, retrieval_method, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(frame, contours, -1, (0, 255, 0), 3)

    # Figure out which contour is the ball if contours are found.
    if len(contours) == 0:
        return None
    else:
        # Choose the contour that is the largest
        bestContour = None
        largestArea = 0
        for contour in contours:
            _, area = ballStats(contour)
            if area is not None and area > largestArea:
                bestContour = contour
                largestArea = area

        # Make sure selected contour isn't just noise
        circularity, area = ballStats(bestContour)
        if not ballCheck(circularity, area, True):
            print("ball selected but rejected at the end", circularity, area)
            return None

        # Convert chosen contour into circle.
        print("ball found")
        (x, y), radius = cv.minEnclosingCircle(bestContour)
        potentialBallPosition = (int(x), int(y))
        radius = int(radius)
        print(potentialBallPosition)
        cv.circle(frame, potentialBallPosition, radius, (255, 0, 0), 10)


        return potentialBallPosition
