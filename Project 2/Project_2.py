#!/usr/bin/python3

import numpy as np
import cv2
import math


frame_height = 250
frame_width = 600
clearance = 5
blank_canvas = np.zeros((frame_height,frame_width,3), np.uint8)
y_invert = 250

def Obstacle_Area():
    canvas = blank_canvas.copy()

    #Rectangle 1
    pts = np.array([[100,y_invert-0],[100,y_invert-100], [150,y_invert-100], [150,y_invert-0]], np.int32)
    pts = pts.reshape((-1,1,2))
    cv2.fillPoly(canvas,[pts],(0, 255, 0))

    #Rectangle 2
    pts = np.array([[100,0],[100,100], [150,100], [150,0]], np.int32)
    pts = pts.reshape((-1,1,2))
    cv2.fillPoly(canvas,[pts],(0, 255, 0))
   
    #Hexagon
    a = 75
    h = int((math.sqrt(3)/2)*a)
    pts = np.array([[300-h,125-a/2],[300-h,125+a/2],[300,125+a],[300+h,125+a/2],[300+h,125-a/2],[300,125-a]], np.int32)
    pts = pts.reshape((-1,1,2))
    cv2.fillPoly(canvas,[pts],(0, 255, 0))

    #Triangle
    pts = np.array([[460,225],[460,25],[510,125]], np.int32)
    pts = pts.reshape((-1,1,2))
    cv2.fillPoly(canvas,[pts],(0, 255, 0))

    return canvas



if __name__ == "__main__":

    canvas = Obstacle_Area()

    cv2.imshow("map",canvas)

    key = cv2.waitKey(0)
    if key == 27:
        cv2.destroyAllWindows()