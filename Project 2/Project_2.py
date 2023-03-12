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
    pts = np.array([[100-clearance,y_invert-0+clearance],[100-clearance,y_invert-100-clearance], [150+clearance,y_invert-100-clearance], [150+clearance,y_invert-0+clearance]], np.int32)
    pts = pts.reshape((-1,1,2))
    cv2.fillPoly(canvas,[pts],(255,255,255))
    pts = np.array([[100,y_invert-0],[100,y_invert-100], [150,y_invert-100], [150,y_invert-0]], np.int32)
    pts = pts.reshape((-1,1,2))
    cv2.fillPoly(canvas,[pts],(0, 255, 0))

    #Rectangle 2
    pts = np.array([[100-clearance,0-clearance],[100-clearance,100+clearance], [150+clearance,100+clearance], [150+clearance,0-clearance]], np.int32)
    pts = pts.reshape((-1,1,2))
    cv2.fillPoly(canvas,[pts],(255,255,255))
    pts = np.array([[100,0],[100,100], [150,100], [150,0]], np.int32)
    pts = pts.reshape((-1,1,2))
    cv2.fillPoly(canvas,[pts],(0, 255, 0))
   
    #Hexagon
    a = 75
    h = int((math.sqrt(3)/2)*a)
    a_ = clearance/math.sqrt(2)
    pts = np.array([[300-h-a_,125-a/2-a_],[300-h-a_,125+a/2+a_],[300,125+a+clearance],[300+h+a_,125+a/2+a_],[300+h+a_,125-a/2-a_],[300,125-a-clearance]], np.int32)
    pts = pts.reshape((-1,1,2))
    cv2.fillPoly(canvas,[pts],(255,255,255))
    pts = np.array([[300-h,125-a/2],[300-h,125+a/2],[300,125+a],[300+h,125+a/2],[300+h,125-a/2],[300,125-a]], np.int32)
    pts = pts.reshape((-1,1,2))
    cv2.fillPoly(canvas,[pts],(0, 255, 0))

    #Triangle
    theta = 63.43
    pts = np.array([[460-clearance*math.cos(np.deg2rad(theta)),225+clearance*math.sin(np.deg2rad(theta))],[460-clearance*math.cos(np.deg2rad(theta)),25-clearance*math.sin(np.deg2rad(theta))],[510+clearance,125]], np.int32)
    pts = np.array([[460-clearance,225+clearance*4],[460-clearance,25-clearance*4],[510+clearance,125]], np.int32)
    pts = pts.reshape((-1,1,2))
    cv2.fillPoly(canvas,[pts],(255,255,255))
    pts = np.array([[460,225],[460,25],[510,125]], np.int32)
    pts = pts.reshape((-1,1,2))
    cv2.fillPoly(canvas,[pts],(0, 255, 0))

    #Walls
    for i in range(frame_width):
        for j in range(clearance):
            canvas[249 - j][i] = [230,230,170]
        for j in range(frame_height-clearance,frame_height):
            canvas[249 - j][i] = [230,230,170]

    for i in range(frame_height):
        for j in range(clearance):
            canvas[249 - i][j] = [230,230,170]
        for j in range(frame_width-clearance,frame_width):
            canvas[249 - i][j] = [230,230,170]

    return canvas


def SetStartEndPoints():

    while True:
        start_X = int(input("Enter start point, [x-coordinate] 6-595: "))
        start_Y = int(input("Enter start point, [y-coordinate] 6-245: "))
        start = [start_X,start_Y]
        if(start[0] < 0 or start[0] > frame_width or start[1] < 0 or  start[1] > frame_height ):
            print("Out of canvas!!! Invalid coordinates given, please provide new valid start points")
            continue
        elif InvalidSpace(start):
            print("Obstacle Space!!! Invalid coordinates given, please provide new valid start points")
            continue
        else:
            break

    while True:
        end_X = int(input("Enter end point, [x-coordinate] 6-595: "))
        end_Y = int(input("Enter end point, [y-coordinate] 6-245: "))
        end = [end_X,end_Y]
        if(end[0] < 0 or end[0] > frame_width or end[1] < 0 or end[1] > frame_height ):
            print("Out of canvas!!! Invalid coordinates given, please provide new valid start points")
            continue
        elif InvalidSpace(end):
            print("Obstacle Space!!! Invalid coordinates given, please provide new valid goal points")
            continue
        else:
            break

    return start, end

def InvalidSpace(node):
    x,y = node[0],node[1]
    b,g,r = canvas[y-1,x-1]
    if((b==0 and g==255 and r==0) or (b==230 and g==230 and r==170)):
        return True
    else:
        return False

if __name__ == "__main__":

    canvas = Obstacle_Area()
    start_loc, goal_loc = SetStartEndPoints()
    print("Start Point :",start_loc)
    print("Goal Point :",goal_loc)

    cv2.imshow("map",canvas)

    key = cv2.waitKey(0)
    if key == 27:
        cv2.destroyAllWindows()