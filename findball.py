import cv2 as cv
from math import pi
import numpy as np


# HELPER FUNCTIONS
def manhattanDistance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def ballStats(contour):
    if contour is None:
        return None

    area = cv.contourArea(contour)
    return area


# Note: Circularity is not a good measure of the ball on low fps fast shots.
def ballCheck(area, debug=False):
    if debug:
        print(area)

    if area is None:
        return False

    # 500 for 1920 x 1080, 0.5 for 640 x 480
    if area < 0.5:
        return False

    return True


# MAIN FUNCTION
# If the ball is found, return a tuple with the x and y coordinate of the circle. Otherwise, return None.
def findBall(frame, tableHeight, width):
    # Gaussian blur, the larger the kernel size the more blurred, not sure what sigma x is.
    blurFrame = cv.GaussianBlur(frame, (17, 17), 0)

    # Don't detect ball if it is on the lower third of the screen.
    TABLE_HEIGHT_MARGIN = 10 # in case the user places the camera slightly off
    mask = np.zeros(frame.shape[:2], dtype="uint8")
    cv.rectangle(mask, (0, 0), (width, tableHeight + TABLE_HEIGHT_MARGIN), 255, -1)
    blurFrame = cv.bitwise_and(blurFrame, blurFrame, mask=mask)

    # Filter by green
    hsv = cv.cvtColor(blurFrame, cv.COLOR_BGR2HSV)
    lower_green = np.array([31, 39, 117])
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
            area = ballStats(contour)
            if area is not None and area > largestArea:
                bestContour = contour
                largestArea = area

        # Make sure selected contour isn't just noise
        area = ballStats(bestContour)
        if not ballCheck(area):
            print("ball selected but rejected at the end", area)
            return None

        # Convert chosen contour into circle.
        print("ball found, area:", area)
        (x, y), radius = cv.minEnclosingCircle(bestContour)
        potentialBallPosition = (int(x), int(y))
        radius = int(radius)
        cv.circle(frame, potentialBallPosition, radius, (255, 0, 0), 10)

        return potentialBallPosition
