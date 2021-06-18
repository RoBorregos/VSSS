import cv2
import numpy as np

# Scalar constants.
#define ORANGE cv::Scalar(0,165,255)
#define BLUE cv::Scalar(255,0,0)
#define YELLOW cv::Scalar(0,255,255)
#define RED cv::Scalar(0,0,255)
#define GREEN cv::Scalar(0,255,0)
#define PINK cv::Scalar(147,20,255)
#define WHITE cv::Scalar(255,255,255)

# Modes.
HSV_COLORS = 1
SET_CORNERS = 2
DISTANCES = 3

# Field constants.
NUM_OF_CORNERS = 4
FIELD_ROWS = 520
FIELD_COLS = 600
FILED_SCALE = 4

# TODO: How to implement private variables.
# Private variables.
cv2.Point2f cornerPoints[NUM_OF_CORNERS]

class calibration(object):
    def __init__(self, screenName, image):
        self.screenName = screenName
        self.image = image

        # Cross template.
        crossTemplate = cv2.imread("../media/cross.jpg")
        # cv2.imshow('original', crossTemplate)
        crossTemplate_gray = cv2.cvtColor(crossTemplate, cv2.COLOR_BGR2GRAY)
        # TODO: fix this.
        # crossTemplate = cv2.threshold(crossTemplate, 240, 255, cv2.THRESH_TOZERO)
        # cv2.imshow('Modified', crossTemplate)
        cv2.waitKey(0)

        # TODO: Fix this after adding scalar constants, modes and fields constants.
        # currentColor = 'white'
        # scalarColor = WHITE
        # logText = ''
        mode = HSV_COLORS

        perspectiveON = False
        isDrawing = False
        stopDrawing = True

        # Sets maximum slider values to 255.
        hueMax = 255
        satMax = 255
        valMax = 255

        # Sets minimum slider values to 0.
        hueMin = 0
        satMin = 0
        valMin = 0
        
        # Sets epsilon values.
        epsilon = [5, 90, 100]  # [H, S, V]
        
        # Creates a windos display for current image.
        cv2.namedWindow(screenName, cv2.WINDOW_AUTOSIZE)

        # TODO: Fix this.
        # Creates callback for screenName.
        # cv2.setMouseCallback(screenName, onMouse, this)

        # Stores a hsv copy of the original image.
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Creates 6 sliders in our window display with a maxium value of 255
        # TODO: Missing 1 argument: The function to call.
        #cv2.createTrackbar("Low  H", screenName, hueMin, 255)
        #cv2.createTrackbar("High H", screenName, hueMin, 255)
        #cv2.createTrackbar("Low  S", screenName, hueMin, 255)
        #cv2.createTrackbar("High S", screenName, hueMin, 255)
        #cv2.createTrackbar("Low  V", screenName, hueMin, 255)
        #cv2.createTrackbar("High V", screenName, hueMin, 255)

        # Reads corners points from file.
        # TODO: Makae readCorners function.
        # readCorners()

        # Displays the original image with the sliders once.
        # TODO: Makae update function.
        # update()

    def listenKey():
        key = cv2.waitKey(30)
        # TODO: Investigate if there is something like switch case on python.
        # TODO: Function readCorners and constants.
        if(key == '1'):
            mode = HSV_COLORS
            #stopDrawing = True
            logText = ""
            #readCorners()
        elif(key == '2'):
            mode = SET_CORNERS
            #stopDrawing = True
            logText = ""
            #readCorners()
        elif(key == '3'):
            mode = DISTANCES
            #stopDrawing = True
            logText = ""
            #readCorners()
        elif(key == 'o'):
            scalarColor = ORANGE
            readColor("Orange")
        elif(key == 'b'):
            scalarColor = BLUE
            readColor("Blue")
        elif(key == 'y'):
            scalarColor = YELLOW
            readColor("Yellow")
        elif(key == 'r'):
            scalarColor = RED
            readColor("Red")
        elif(key == 'g'):
            scalarColor = GREEN
            readColor("Green")
        elif(key == 'p'):
            scalarColor = PINK
            readColor("Pink")
        elif(key == 'c'): # This keeps the same currentColor but changes color to DEFAULT.
            readColor("DEFAULT")
        elif(key == 'z'):
            perspectiveON = not perspectiveON
        elif(key == 10): # This is the value for ENTER.
            if(mode == HSV_COLORS and scalarColor != WHITE):
                saveColor()
            elif(mode == SET_CORNERS and cornerCount == NUM_OF_CORNERS):
                saveCorners()
        elif(key == 32):# This is the value for SPACE.
            return 0
        elif(key == 27):# This is the value for ESC.
            return -1
        return 1
    
    def readCorners():
        # Reads the file.
        # TODO: What if the file could not be opened?
        with open('dir', 'r') as f:
            

image = cv2.imread("../media/test.png")
cal = calibration("Wenos", image)
cal.listenKey