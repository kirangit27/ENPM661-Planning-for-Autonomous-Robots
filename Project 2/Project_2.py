#!/usr/bin/python3

import cv2
from queue import PriorityQueue
import timeit
from map import *


frame_height = 250
frame_width = 600
clearance = 5
blank_canvas = np.zeros((frame_height,frame_width,3), np.uint8)
y_invert = 250

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
    print("Searching...")

    return start, end
    

class Node:
    def __init__(self, pos, cost, parent):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.cost = cost
        self.parent = parent


def Orientation(node):

    x,y = node.x,node.y
    actions = [(x, y+1), (x+1, y), (x-1, y), (x, y-1), (x+1, y+1), (x-1, y-1), (x-1, y+1), (x+1, y-1)]
    actions_path = []
    for pos, path in enumerate(actions):
        if not ((path[0] < 0 or path[0] >= frame_width or path[1] < 0 or  path[1] >= frame_height ) and InvalidSpace(path)):
            if pos > 3:
                cost = 1.4 
            else:
                cost = 1
            actions_path.append([path, cost])
    return actions_path


def Dijkstra(start_loc, goal_loc):
    
    pQ = PriorityQueue()
    visited_node = []
    parent_node = {}
    total_cost = {}
    
    node = Node(start_loc, 0, None)
    pQ.put([node.cost, node.pos])  
    visited_node.append(start_loc)
    total_cost[start_loc] = 0
    parent_node[node.pos] = node
   
    while pQ:
        current_node = pQ.get()
        node = parent_node[current_node[1]]
        if (current_node[1] == goal_loc):
            parent_node[goal_loc] = Node(goal_loc, current_node[0], node)
            break
        for next_node, cost in Orientation(node):
            if not InvalidSpace(next_node) and next_node[0] <= frame_width and next_node[1] <= frame_height:
                    if next_node in visited_node:
                        current_cost = total_cost[node.pos] + cost
                        if current_cost < total_cost[next_node]:
                            parent_node[next_node].parent = node
                            total_cost[next_node] = current_cost                         
                    else:
                        visited_node.append(next_node)
                        final_cost = cost + total_cost[node.pos]    
                        temp_node = Node(next_node, final_cost, parent_node[node.pos])
                        pQ.put([final_cost, temp_node.pos])
                        parent_node[next_node] = temp_node
                        total_cost[next_node] = final_cost                
    goal_loc_final = parent_node[goal_loc]
    parent_node_ = goal_loc_final.parent
    back_track = []
    while parent_node_:
        back_track.append(parent_node_.pos)
        parent_node_ = parent_node_.parent

    return visited_node, back_track


if __name__ == "__main__":

    canvas = Obstacle_Area()
    start_loc, goal_loc = SetStartEndPoints()
    
    run_start = timeit.default_timer()

    start_X, start_Y = start_loc[0], start_loc[1]
    cv2.circle(canvas, (start_X, y_invert - start_Y), radius=4, color=(0, 0, 255), thickness=-1)
    goal_X, goal_Y =  goal_loc[0], goal_loc[1]
    cv2.circle(canvas, (goal_X, y_invert - goal_Y), radius=4, color=(0, 0, 255), thickness=-1)

    start_loc = (start_X, start_Y)
    goal_loc = (goal_X, goal_Y)
    visited, optimal_path = Dijkstra(start_loc, goal_loc)
    run_end = timeit.default_timer()
    print("Time to reach Target -> %s seconds" % (run_end - run_start))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('kpatil27_Proj2.mp4', fourcc, 2000,(600, 250))

    for point in visited:
        canvas[y_invert-point[1]-1, point[0]] = (0,128,255)
        out.write(canvas)

    for point in optimal_path:
        canvas[y_invert-point[1]-1, point[0]-1] = (200, 25, 0)
        out.write(canvas)

    for point in range(1000):
        out.write(canvas)

    cv2.circle(canvas, (start_X, y_invert - start_Y), radius=4, color=(0, 0, 255), thickness=-1)
    cv2.circle(canvas, (goal_X, y_invert - goal_Y), radius=4, color=(0, 0, 255), thickness=-1)

    cv2.imwrite("Result.png", canvas)  
    cv2.imshow("Final",canvas)

    print("ESC to end!!!")
    out.release()
    key = cv2.waitKey(0)
    if key == 27:
        cv2.destroyAllWindows()
