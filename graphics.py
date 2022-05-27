import cv2 as cv

class GraphicsEngine:
    def __init__(self, height, tableHeight, width):
        self.height = height
        self.tableHeight = tableHeight
        self.width = width

    def drawState(self, frame, currentStateString):
        font = cv.FONT_HERSHEY_DUPLEX
        text = currentStateString
        scale = 5
        thickness = 5
        textSize = cv.getTextSize(text, font, scale, thickness)[0]
        textX = 0
        textY = 200
        cv.putText(frame, text, (textX, textY), font, scale, (255, 255, 255), thickness)

    def drawScore(self, frame, leftScore, rightScore, leftIsServing):
        # Make the score of the serving side green.
        leftColor = (255, 255, 255)
        rightColor = (255, 255, 255)
        if leftIsServing:
            leftColor = (0, 255, 0)
        else:
            rightColor = (0, 255, 0)

        # Draw score centered on the left
        font = cv.FONT_HERSHEY_DUPLEX
        text = str(leftScore)
        scale = 10
        thickness = 10
        textSize = cv.getTextSize(text, font, scale, thickness)[0]
        textX = ((self.width // 2) - textSize[0]) // 2
        textY = ((self.height - self.tableHeight - textSize[1]) // 2) + self.tableHeight + textSize[1]
        cv.putText(frame, text, (textX, textY), font, scale, leftColor, thickness)

        # Draw dash on the center
        font = cv.FONT_HERSHEY_DUPLEX
        text = "-"
        scale = 10
        thickness = 10
        textSize = cv.getTextSize(text, font, scale, thickness)[0]
        textX = (self.width - textSize[0]) // 2
        textY = ((self.height - self.tableHeight - textSize[1]) // 2) + self.tableHeight + textSize[1]
        cv.putText(frame, text, (textX, textY), font, scale, (255, 255, 255), thickness)

        # Draw score centered on the right
        font = cv.FONT_HERSHEY_DUPLEX
        text = str(rightScore)
        scale = 10
        thickness = 10
        textSize = cv.getTextSize(text, font, scale, thickness)[0]
        textX = (((self.width // 2) - textSize[0]) // 2) + self.width // 2
        textY = ((self.height - self.tableHeight - textSize[1]) // 2) + self.tableHeight + textSize[1]
        cv.putText(frame, text, (textX, textY), font, scale, rightColor, thickness)
