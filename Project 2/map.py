import numpy as np
import math

frame_height = 250
frame_width = 600
clearance = 5
blank_canvas = np.zeros((frame_height,frame_width,3), np.uint8)
y_invert = 249


def Rect(x, y):

    if (100 <= x <= 150) and (150 <= y <= frame_height) or \
        (100 <= x <= 150) and (0 <= y <= 100):
        return True
    
    return False


def Rect_C(x, y):

    if (100 - clearance) <= x <= (150 + clearance) and \
       (0 <= y <= (100 + clearance) )or \
       (100 - clearance) <= x <= (150 + clearance) and \
       (150 - clearance) <= y <= frame_height:
        return True
    
    return False
          

def Hexagon(x, y):

    side = 75
    H1 = (300 - side * math.cos(math.radians(30)))
    H2 = (300 + side * math.cos(math.radians(30)))

    if (x >= H1 and x <= H2) and \
       (y - 0.58 * x - 26.8) <= 0 and \
       (y + 0.58 * x - 373.2) <= 0 and \
       (y - 0.58 * x + 123.2) >= 0 and \
       (y + 0.58 * x - 223.2) >= 0:
        return True
    
    return False


def Hexagon_C(x, y):

    side = 75
    H1 = (300 - side * math.cos(math.radians(30)))
    H2 = (300 + side * math.cos(math.radians(30)))

    if (x >= (H1 - clearance)) and \
       (x <= (H2 + clearance)) and \
       (y - 0.58 * x - 32.6) <= 0 and \
       (y + 0.58 * x - 379) <= 0 and \
       (y - 0.58 * x + 129) >= 0 and \
       (y + 0.58 * x - 217.4) >= 0:
        return True
    
    return False


def Triangle(x, y):
    if x >= 460 and (y + 2 * round(x, 0) - 1145) <= 0 and (y - 2 * round(x, 0) + 895) >= 0:
        return True
    return False


def Triangle_C(x, y):
    if x >= (460 - clearance) and \
       (y + 2 * round(x, 0) - 1155) <= 0 and \
       (y - 2 * round(x, 0) + 905) >= 0:
        return True
    return False


def Obstacle_Area():

    canvas = blank_canvas.copy()

    for y in range(frame_height):
        for x in range(frame_width):

            if (Rect_C(x,y)): 
                canvas[y_invert - y][x] = [255,255,255]
            
            if(Triangle_C(x,y) ):
               canvas[y_invert - y][x] = [255,255,255]

            if(Hexagon_C(x,y)):
                canvas[y_invert - y][x] = [255,255,255]

            if(Rect(x,y)):
                canvas[y_invert - y][x] = [0, 255, 0]

            if(Triangle(x,y) ):
               canvas[y_invert - y][x] = [0, 255, 0]
               
            if(Hexagon(x,y)):
                canvas[y_invert - y][x] = [0, 255, 0]

    for x in range(frame_width):
        for y in range(clearance):
            canvas[y_invert - y][x] = [230,230,170]
        for y in range(frame_height-clearance,frame_height):
            canvas[y_invert - y][x] = [230,230,170]

    for y in range(frame_height):
        for x in range(clearance):
            canvas[y_invert - y][x] = [230,230,170]
        for x in range(frame_width-clearance,frame_width):
            canvas[y_invert - y][x] = [230,230,170]

    return canvas

canvas = Obstacle_Area()

def InvalidSpace(node):
    x,y = node[0],node[1]
    b,g,r = canvas[y-1,x-1]
    if((b==0 and g==255 and r==0) or (b==230 and g==230 and r==170) or (b==255 and g==255 and r==255)):
        return True
    else:
        return False