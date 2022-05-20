# tutorials:
# https://www.youtube.com/watch?v=RaCwLrKuS1w, basics of using opencv
# https://www.analyticsvidhya.com/blog/2020/03/ball-tracking-cricket-computer-vision/, segmenting a circle
# https://www.geeksforgeeks.org/filter-color-with-opencv/, process of color filtering

import cv2 as cv
import numpy as np
import keyboard

videoCapture = cv.VideoCapture(1)
prevCircle = None
dist = lambda x1, y1, x2, y2: (x1 - x2) ** 2 * (y1 - y2) ** 2

# Establish net line parameters
ret, frame = videoCapture.read()
height, width = frame.shape[:2]
net_x = width // 2

# User input
keyboard.on_press_key("q", lambda: exit())
def moveNetLeft():
    global net_x
    net_x -= 1
keyboard.on_press_key("left arrow", moveNetLeft())
def moveNetRight():
    global net_x
    net_x += 1
keyboard.on_press_key("right arrow", moveNetRight())

while True:
    ret, frame = videoCapture.read()
    image = cv.line(frame, (net_x, 0), (net_x, height), (255, 0, 255), 3)

    if not ret: break

    # Gaussian blur, the larger the kernel size the more blurred, not sure what sigma x is.
    blurFrame = cv.GaussianBlur(frame, (17, 17), 0)

    # Filter by orange
    hsv = cv.cvtColor(blurFrame, cv.COLOR_BGR2HSV)
    lower_orange = np.array([14, 85, 87],)
    upper_orange = np.array([27, 255, 255])
    mask = cv.inRange(hsv, lower_orange, upper_orange)

    # Hough circle on the mask
    # circles = cv.HoughCircles(mask, cv.HOUGH_GRADIENT, 1.2, 100, param1=100, param2=30, minRadius=75, maxRadius=400)
    # print(circles)
    # if circles is not None:
    #     circles = np.uint16(np.around(circles))
    #     chosen = circles[0][0]
    #
    #     cv.circle(frame, (chosen[0], chosen[1]), 1, (0, 100, 100), 3)
    #     cv.circle(frame, (chosen[0], chosen[1]), chosen[2], (255, 0, 255), 3)

    # Get contours of mask.
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        # Choose the contour with the largest area.
        ball_contour = contours[0]
        for contour in contours:
            if cv.contourArea(contour) > cv.contourArea(ball_contour):
                ball_contour = contour

        # Convert contour into circle.
        (x, y), radius = cv.minEnclosingCircle(ball_contour)
        center = (int(x), int(y))
        radius = int(radius)
        cv.circle(frame, center, radius, (0, 255, 0), 10)


    cv.imshow("circle", frame)



videoCapture.release()
cv.destroyAllWindows()
