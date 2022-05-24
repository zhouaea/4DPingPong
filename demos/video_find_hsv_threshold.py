# taken from https://medium.com/programming-fever/how-to-find-hsv-range-of-an-object-for-computer-vision-applications-254a8eb039fc

# finding hsv range of target object(pen)
import cv2
import numpy as np
import time


# A required callback method that goes into the trackbar function.
def nothing(x):
    pass


# Initializing the webcam feed.
video = "6.mp4"
cap = cv2.VideoCapture(video)
cap.set(3, 1280)
cap.set(4, 720)

# Create a window named trackbars.
cv2.namedWindow("Trackbars")

# Now create 6 trackbars that will control the lower and upper range of
# H,S and V channels. The Arguments are like this: Name of trackbar,
# window name, range,callback function. For Hue the range is 0-179 and
# for S,V its 0-255.
default_lower = [9, 61, 120]
default_upper = [13, 255, 255]

cv2.createTrackbar("L - H", "Trackbars", default_lower[0], 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", default_lower[1], 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", default_lower[2], 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", default_upper[0], 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", default_upper[1], 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", default_upper[2], 255, nothing)

while True:

    # Start reading the webcam feed frame by frame.
    ret, frame = cap.read()
    if not ret:
        cap = cv2.VideoCapture(video)
        continue

    frame = cv2.GaussianBlur(frame, (17, 17), 0)

    # Convert the BGR image to HSV image.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get the new values of the trackbar in real time as the user changes
    # them
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")

    # Set the lower and upper HSV range according to the value selected
    # by the trackbar
    lower_range = np.array([l_h, l_s, l_v])
    upper_range = np.array([u_h, u_s, u_v])

    # Filter the image and get the binary mask, where white represents
    # your target color
    mask = cv2.inRange(hsv, lower_range, upper_range)

    # You can also visualize the real part of the target color (Optional)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Converting the binary mask to 3 channel image, this is just so
    # we can stack it with the others
    mask_3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # stack the mask, orginal frame and the filtered result
    stacked = np.hstack((mask_3, frame, res))

    # Show this stacked frame at 40% of the size.
    cv2.imshow('Trackbars', cv2.resize(stacked, None, fx=0.4, fy=0.4))

    # If the user presses ESC then exit the program
    key = cv2.waitKey(1)
    if key == 27:
        break

    # If the user presses `s` then print this array.
    if key == ord('s'):
        thearray = [[l_h, l_s, l_v], [u_h, u_s, u_v]]
        print(thearray)

        # Also save this array as penval.npy
        np.save('hsv_value', thearray)
        break

# Release the camera & destroy the windows.
cap.release()
cv2.destroyAllWindows()