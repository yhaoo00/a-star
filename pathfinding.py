'''
    -Left click to fill in start and end node, then walls
    -ESCAPE to clear grids

    -To use random wall generator, uncommand line 55 and line 56
    -Left click to fill in your own start and end node

    -ENTER to start the visualiser
'''

import pygame as pg
import math
import random
from queue import PriorityQueue

#---------Constants----------
#screen size
SIZE = 500
#create window
SCREEN = pg.display.set_mode((SIZE, SIZE))
#set title
pg.display.set_caption("A* Visualiser")

#colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
LIGHTGREY = (200, 200, 200)
TURQUOISE = (64, 224, 208)

#number of grids
ROWS = 50

#--------------Class-------------
#class for all nodes
class Node:
    #init function
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.color = LIGHTGREY
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows
        self.auto_wall = False
        
        '''if random.randint(0, 100) < 20:
             self.auto_wall = True'''

    #----Functions for states of each nodes-----
    #get node positions/index
    def get_pos(self):
        return self.row, self.col

    #--getter functions
    #mark visited nodes
    def visited(self):
        return self.color == WHITE

    #mark unvisited nodes
    def notVisited(self):
        return self.color == YELLOW

    #mark walls
    def isWall(self):
        return self.color == BLACK

    #mark starting node
    def isStart(self):
        return self.color == ORANGE

    #mark end node
    def isEnd(self):
        return self.color == TURQUOISE

    #reset node
    def reset(self):
        self.color = LIGHTGREY

    #--setter functions
    #set visited nodes color
    def setVisited(self):
        self.color = WHITE

    #set unvisited nodes color
    def setNotVisited(self):
        self.color = YELLOW

    #set walls color
    def setIsWall(self):
        self.color = BLACK

    #set starting node color
    def setIsStart(self):
        self.color = ORANGE

    #set end node color
    def setIsEnd(self):
        self.color = TURQUOISE

    #set shortest path color
    def shortestPath(self):
        self.color = BLUE

    #draw rect function
    def draw(self, win):
        if self.auto_wall == True:
            self.color = BLACK
        pg.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    #update neighbour nodes
    def update(self, node):
        self.neighbours = []
        #--check surrounding of current nodes and if not wall then add to neighbour list
        #add top node to neighbour list if node is not at pos 0 and top node is not a wall
        if self.row > 0 and not node[self.row - 1][self.col].isWall():
            self.neighbours.append(node[self.row - 1][self.col])
        #add bottom node to neighbour list if node is not at last row and bottom node is not a wall
        if self.row < self.total_rows - 1 and not node[self.row + 1][self.col].isWall():
            self.neighbours.append(node[self.row + 1][self.col])
        #add left node to neighbour list if node is not at pos 0 and left node is not a wall
        if self.col > 0 and not node[self.row][self.col - 1].isWall():
            self.neighbours.append(node[self.row][self.col - 1])
        #add right node to neighbour list if node is not at last col and right node is not a wall
        if self.col < self.total_rows - 1 and not node[self.row][self.col + 1].isWall():
            self.neighbours.append(node[self.row][self.col + 1])

    #less than function
    '''
        handle nodes when comparing two nodes
        such as comparing self node and other node
        always return other node is greater than self node.
    '''
    def __lt__(self, other):
        return False

#heuristic function (manhattan distance formula)
def heuristic(pt1, pt2):
    #pt returns (x,y)
    x_1, y_1 = pt1
    x_2, y_2 = pt2
    return abs(x_1 - x_2) + abs(y_1 - y_2)

#construct shortest path
def construct_shortest(prev, current, draw):
    #backtrack end node to start node
    while current in prev:
        #set current node = previous node
        current = prev[current]
        current.shortestPath()
        draw()

#a star algo function
def a_star(draw, grid, start, end):
    #keep track of when we insert item into queue
    count = 0
    node_set = PriorityQueue() #sort the nodes
    #add start node and F(n) into set
    node_set.put((0, count, start))
    #previous node set
    prev_node = {}

    #set Gn to infinity to all other nodes
    Gn = {node: float('inf') for row in grid for node in row}
    #set Gn of start node to 0
    Gn[start] = 0

    #set Fn to infinity to all other nodes
    Fn = {node: float('inf') for row in grid for node in row}
    #set Fn of start node to heuristic/Hn
    #this is to estimated dist from start node to end node
    Fn[start] = heuristic(start.get_pos(), end.get_pos())

    #to keep track for nodes in priority queue sets
    node_set_current = {start}

    #if set is empty then break loop
    while not node_set.empty():
        #allow user to quit
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

        #index put at 2 as in node_set the node location is at index 2
        #eg. node_set((Fn, count, node))
        current = node_set.get()[2]
        #pop the node same as for node_set
        node_set_current.remove(current)

        #if the current node popped out is end node, shortest path is found
        if current == end:
            #create path
            construct_shortest(prev_node, end, draw)
            end.setIsEnd()
            start.setIsStart()
            return True

        #add 1 to Gn as moving to neighbour node
        for neighbour in current.neighbours:
            temp_Gn = Gn[current] + 1

            #if there is a shorter path, update
            if temp_Gn < Gn[neighbour]:
                prev_node[neighbour] = current
                Gn[neighbour] = temp_Gn
                Fn[neighbour] = temp_Gn + heuristic(neighbour.get_pos(), end.get_pos())
                # if node is not in set, add the node in
                if neighbour not in node_set_current:
                    count += 1
                    node_set.put((Fn[neighbour], count, neighbour))
                    node_set_current.add(neighbour)
                    neighbour.setNotVisited()

        #lambda is used
        draw()

        #if the node added is not a start node, mark it as visited
        if current != start:
            current.setVisited()

    return False #path not found

#create grid
def create_grid(rows, width):
    grid = []
    #width of each squares
    gap = width//rows

    #in grid row i, append node into it
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid

#draw grid lines
def draw_grid(screen, rows, width):
    gap = width//rows

    #draw line to every rows (x and y axis)
    for i in range(rows):
        pg.draw.line(screen, BLACK, (0, i*gap), (width, i*gap))
        for j in range(rows): 
            pg.draw.line(screen, BLACK, (j*gap, 0), (j*gap, width))

#draw function
def draw(screen, grid, rows, width):
    screen.fill(LIGHTGREY)

    for row in grid:
        for node in row:
            node.draw(screen)

    draw_grid(screen, rows, width)
    pg.display.update()

#get mouse position
def get_mouse_pos(pos, rows, width):
    gap = width//rows
    x, y = pos
    row = x//gap
    col = y//gap

    return row, col

def main(screen, width):
    global ROWS
    grid = create_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(screen, grid, ROWS, width)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            #left click to draw
            if pg.mouse.get_pressed()[0]:
                pos = pg.mouse.get_pos()
                row, col = get_mouse_pos(pos, ROWS, width)
                node = grid[row][col]

                #set start node
                if not start and node != end:
                    start = node
                    start.setIsStart()
                #set end node
                elif not end and node != start:
                    end = node
                    end.setIsEnd()
                #set wall is start and end is exist
                elif node != end and node != start:
                    node.setIsWall()

            #right click to erase
            elif pg.mouse.get_pressed()[2]:
                pos = pg.mouse.get_pos()
                row, col = get_mouse_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()

                #clear start and end node
                if node == start:
                    start = None
                elif node == end:
                    end = None

            #press enter to start visualiser
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN and start and end:
                    for row in grid:
                        for node in row:
                            node.update(grid)
                    #lambda is used to pass the function and call it
                    solution = a_star(lambda: draw(screen, grid, ROWS, width), grid, start, end)
                    if solution:
                        print("Shortest path generated")
                    else:
                        print("No solution")

                #clear grid with escape
                if event.key == pg.K_ESCAPE:
                    start = None
                    end = None
                    grid = create_grid(ROWS, width)

    
    pg.quit()

main(SCREEN, SIZE)
