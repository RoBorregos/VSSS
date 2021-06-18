import cv2
import numpy as np

# Constants.
pi = 3.14159265

# Private variables.
crossPoints = []
allies = []
enemies = []
# ball = shape

class foo(object):
    firstTimeFlag = False
    x = 0.0
    y = 0.0
    dx = 0.0
    dy = 0.0
    ori = 0.0

class hsv(object):
    hMin = 0
    hMax = 0
    sMin = 0
    sMax = 0
    vMin = 0
    vMax = 0

# TODO: Fix this.
# class c_pair(object):
    # c_color = cv2.Point2f
    # c_teamColor = cv2.Point2f

class vision(object):
    def __init__(self, original, teamColor, allies, enemies, ball):
        self.original = original
        self.heigth = original.shape[0]
        self.width = original.shape[1]
        
        # Missing calibration parameters for HVS.

        self.teamColor = teamColor
        self.enemies = enemies
        self.allies = allies
        self.ball = ball

        self.drawSet = False

    # TODO: Never found the crosspoints.txt file.
    # def setCrossPoints():
        # Reads the file.
        # with open('./vision/calibration/crosspoints.txt', 'r') as f:

    # TODO: Never found the limits.txt file.
    # def setLimits():
            
    #TODO: Make this part more efficient.
    def setHSV(self, hsvColor, color):
        # Reads the file.
        with open('Calibration/colors.txt', 'r') as f:
            for line in f:
                # Separates the line into strings.
                line = line.split()
                # The first string is the name of the color.
                c = line[0]
                # Converts the rest of the list into integers and asigns them to the hsvColor.
                mapOfStrings = map(int, line[1:])
                listOfIntegers = list(mapOfStrings)
                if(c == color):
                    print(listOfIntegers)
                    hMin, hMax, sMin, sMax, vMin, vMax = listOfIntegers
                    hsvColor.hMin = hMin
                    hsvColor.hMax = hMax
                    hsvColor.sMin = sMin
                    hsvColor.sMax = sMax
                    hsvColor.vMin = vMin
                    hsvColor.vMax = vMax

    

    def updateMask(self, c):
        # Updates the hsv image.
        hsv_image = cv2.cvtColor(self.original, cv2.COLOR_BGR2HSV)
        # Updates mask values with the corresponding HSV.
        hsv_image = cv2.inRange(hsv_image, (c.hMin, c.sMin, c.vMin), (c.hMax, c.sMax, c.vMax))
        # Shows image.
        cv2.imshow('original', self.original)
        cv2.imshow('HSV', hsv_image)
        cv2.waitKey(0)


    # TODO: call fixContours.
    # TODO: call updateMask.
    # TODO: clean this section after working correctly.
    def getContours(self, color):
        # Create a black image with the same dimensions as our loaded image.
        black_image = np.zeros((self.original.shape[0], self.original.shape[1], 3))

        # Create a copy of the original image.
        original_copy = self.original

        # Grayscale.
        gray = cv2.cvtColor(original_copy, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Grayscale', gray)

        # Find Canny edges.
        edged = cv2.Canny(gray, 50, 200)
        cv2.imshow('Canny Edges', edged)

        # Find contours and print how many there are.
        contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        print("Number of contours found = ", len(contours))

        # Drawing contours on the original image.
        cv2.drawContours(original_copy, contours, -1, (0,255,0), 3)
        cv2.imshow('Contours', original_copy)
        cv2.waitKey(0)

        return contours

    # TODO: Fix min and max area.
    def fixContours(self, contours):
        minArea = 1
        maxArea = 2
        for cnt in contours:
            # Image area's percentage.
            area = cv2.contourArea(cnt)/(self.width*self.heigth)*100
            print('area = ',area)
            # Not working yet.
            #if(area < minArea or area > maxArea):
                #contours.remove(cnt)

    # def getCentroids(color):
        #TODO

    # def getCentroidPair(c_color, c_target):
        #TODO

    # def drawContours(contours, centroids):
        #TODO

    # def update():
        #TODO

    # def updateValues(f, cp):
        #TODO



input = cv2.imread('media/test_image.png')
a = vision(input,1,1,1,1)
# a.updateMask(1)
contours = a.getContours(1)
print(len(contours))
#a.fixContours(contours)
print(len(contours)) 
orange = hsv()
a.setHSV(orange, 'Orange') 
a.updateMask(orange)
#blue = hsv()
#a.setHSV(blue, 'Blue') 
#a.updateMask(blue)
#yellow = hsv()
#a.setHSV(yellow, 'Yellow') 
#a.updateMask(yellow)
red = hsv()
a.setHSV(red, 'Red') 
a.updateMask(red) 
