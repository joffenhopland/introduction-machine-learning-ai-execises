from queue import Empty
from Graph import Graph
from Vertex import Vertex
from Edge import Edge

import pygame as pg
'''
The AStar class inherits the Graph class
'''


class AStar(Graph):

    '''
    # 
    #  delay: seconds between each iteration when visualizing is turned on
    # visual: Turns pygame visualization on/off
    #
    '''

    def __init__(self, delay=0.001, visual=True):
        super().__init__()
        self.pygame = visual
        self.background = None
        self.LIGHTGREY = (180, 180, 180)
        self.DARKGREEN = (0, 255, 0)
        self.PINK = (255, 200, 200)
        self.GREEN = (200, 255, 200)
        self.WHITE = (245, 245, 245)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.delay = delay
        # walls define obstacles in grid, e.g. walls, boxes etc, by defining each position in grid that is part of an obstacle
        self.walls = []

    '''       
    #
    # Defines obstacles provided in removevertecies from the graph by removing all edges 
    # to vertecies that is defined as an obstacle
    #
    '''

    def removeVertecies(self, removevertecies=[]):
        err_v = []
        err_e = []
        # Removing the vertecies
        for r in removevertecies:
            self.walls.append(self.vertecies[r])
            self.vertecies.pop(r)
        # Checking the edges ...
        for v in self.vertecies:
            vtex = self.vertecies[v]
            for edge in vtex.adjecent:
                vertex = edge.vertex
                if vertex.name not in self.vertecies:
                    err_v.append(vtex)
                    err_e.append(edge)
        for i in range(0, len(err_v)):
            err_v[i].adjecent.remove(err_e[i])
        return removevertecies

    '''       
    #
    # Read in the list of obstacles (defined by tag "remove"), the startnode from which traversal is defined, 
    # and the targetnode
    #
    '''

    def readLimitations(self, filename):
        import pandas as pd
        from collections import namedtuple

        columnnames = ['item', 'valuelist']
        df = pd.read_csv(filename, on_bad_lines='warn',
                         encoding='latin-1',
                         names=columnnames, header=None, sep=':')
        for i in range(0, 3):
            if df.iat[i, 0] == 'startvertex':
                startVertex = df.iat[i, 1]
            elif df.iat[i, 0] == 'targetvertex':
                targetVertex = df.iat[i, 1]
            elif df.iat[i, 0] == 'remove':
                removed = self.removeVertecies(df.iat[i, 1].split(';'))
        return startVertex, targetVertex, removed

    '''       
    # Initialize pygame visualization, if visualization has been defined
    # Creates a dynamic visual grid according to the number of columns and rows
    # read/defined during initialization. The visual limitations are defined by 1000x1000 pixels
    '''

    def initPygame(self):
        if self.pygame:
            xmin = ymin = xmax = ymax = 0
            for v in self.vertecies:
                vertex = self.vertecies[v]
                x, y = vertex.position()
                if x < xmin:
                    xmin = x
                elif x > xmax:
                    xmax = x
                if y < ymin:
                    ymin = y
                elif y > ymax:
                    ymax = y

            pg.init()
            w, h = 1000, 1000
            self.xboxsize = int(w / ((xmax + 1) - xmin))
            self.yboxsize = int(w / ((ymax + 1) - ymin))

            w = self.xboxsize * ((int(w/self.xboxsize)))
            h = self.yboxsize * ((int(h/self.yboxsize)))
            self.background = pg.display.set_mode((w, h))
            background = self.background

            self.clock = pg.time.Clock()

            self.clock.tick(5)

            for c in range(0, (int(w/self.xboxsize)) + 1):
                for l in range(0, (int(h/self.yboxsize)) + 1):
                    pg.draw.rect(background, self.WHITE, (c * self.xboxsize,
                                 l * self.yboxsize, self.xboxsize, self.yboxsize))
                    pg.draw.line(background, self.BLACK, (c * self.xboxsize, l * self.yboxsize),
                                 (c * self.xboxsize + self.xboxsize, l * self.yboxsize))
                    pg.draw.line(background, self.BLACK, (c * self.xboxsize, l * self.yboxsize),
                                 (c * self.xboxsize, l * self.yboxsize + self.yboxsize))
                    pg.draw.line(background, self.BLACK, (c * self.xboxsize + self.xboxsize, l * self.yboxsize),
                                 (c * self.xboxsize + self.xboxsize, l * self.yboxsize + self.yboxsize))
                    pg.draw.line(background, self.BLACK, (c * self.xboxsize, l * self.yboxsize + self.yboxsize),
                                 (c * self.xboxsize + self.xboxsize, l * self.yboxsize + self.yboxsize))
            for wall in self.walls:
                self.pygameState(wall, self.BLACK)
            pg.display.flip()

    '''       
    # Draw a box, representing the current vertex in the position defined by the name of the vertex.
    # The color-parameter defines the (R,G,B)-value of the box
    # If no visualization is used (self.pygame == False), no box is visualized
    '''

    def pygameState(self, current, color):
        import time
        if self.pygame:
            background = self.background
            x, y = current.position()
            pg.draw.rect(background, color, (x * self.xboxsize,
                         y * self.yboxsize, self.xboxsize, self.yboxsize))
            pg.draw.line(background, self.BLACK, (x * self.xboxsize, y * self.yboxsize),
                         (x * self.xboxsize + self.xboxsize, y * self.yboxsize))
            pg.draw.line(background, self.BLACK, (x * self.xboxsize, y * self.yboxsize),
                         (x * self.xboxsize, y * self.yboxsize + self.yboxsize))
            pg.draw.line(background, self.BLACK, (x * self.xboxsize + self.xboxsize, y * self.yboxsize),
                         (x * self.xboxsize + self.xboxsize, y * self.yboxsize + self.yboxsize))
            pg.draw.line(background, self.BLACK, (x * self.xboxsize, y * self.yboxsize + self.yboxsize),
                         (x * self.xboxsize + self.xboxsize, y * self.yboxsize + self.yboxsize))
            if color not in [self.BLUE, self.RED, self.BLACK]:
                time.sleep(self.delay)
                pass
            pg.display.flip()

    '''
    #
    # Defining the heuristics used to calculate the estimated distance between the node being handled (startVertexName), 
    # and the targetnode (targetVertexName)
    # Please note that the name of the vertecies are passed, not the vertex itself. The name is used for lookup
    # in the list of vertecies in the graph.
    # Further, the name of the vertex has the syntax: xNNyMM, where NN and MM are numerical and indicates column and row.
    # E.g. x4y15 means column 4 of row 15. 
    # By identifying the column and row of a vertex, the estimated shorted distance between two vertecies may be 
    # calculated using the Manhatten distance
    #
    '''

    def heuristics(self, startVertexName=None, targetVertexName=None):
        if not startVertexName or not targetVertexName:
            raise KeyError(
                "VertexLookup need the names of the Vertecies addressed.")
        if startVertexName not in self.vertecies:
            raise KeyError(
                "Node/Vertex defined as FROM-vertex is not present in graph")
        if targetVertexName not in self.vertecies:
            raise KeyError(
                "Node/Vertex defined as TO-vertex is not present in graph")

        xstart, ystart = self.vertecies[startVertexName].position()
        xend, yend = self.vertecies[targetVertexName].position()
        #
        # Manhatten heuristics
        #
        dx = abs(xstart - xend)
        dy = abs(ystart - yend)
        D = 1
        return D * (dx + dy)

    '''
    #
    # The Dijkstra's algorithm has been adapted to support visualization as defined by the graph
    # It has further been adopted to present a targetVetrx even though Dijkstra's has no use of
    # it during execution. The tragetVertex is used only for visualization purposes.
    '''

    def Dijkstra(self, startVertexName=None, targetVertexName=None):
        self.initPygame()
        # Check to see that startvertex is in Graph
        if startVertexName not in self.vertecies:
            raise KeyError("Start node not present in graph")
        # Reset visited and previous pointer before running algorithm
        vertex = self.vertecies[startVertexName]
        vertex.distance = distance = weight = 0
        previous_node = None
        startNode = self.vertecies[startVertexName]
        toNode = self.vertecies[targetVertexName]
        #
        # Create priority queue, priority = current weight on edge ...
        # No duplicate edges in queue allowed
        #
        import heapdict
        priqueue = heapdict.heapdict()
        # Defines enqueue/dequeue methods on priqueue

        def enqueue(data):
            priqueue[data] = data.distance

        def dequeue():
            return priqueue.popitem()[0]

        enqueue(vertex)
        while priqueue:
            # Get the element with lowest priority (i.e. weight on edge)
            vertex = dequeue()
            self.pygameState(vertex, self.GREEN)
            self.pygameState(startNode, self.BLUE)
            self.pygameState(toNode, self.RED)
            # If not visited previously, we need to define the distance
            if not vertex.known:
                vertex.distance = distance
                vertex.previous = previous_node
            vertex.known = True

            # If the vertex pointed to by the edge has an adjecency list, we need to iterate on it
            for adjecentedge in vertex.adjecent:
                if not adjecentedge.vertex.known:
                    adjecentedge.vertex.distance = vertex.distance + adjecentedge.weight
                    adjecentedge.vertex.previous = vertex
                    adjecentedge.vertex.known = True
                    enqueue(adjecentedge.vertex)
                    self.pygameState(adjecentedge.vertex, self.PINK)
                else:
                    if adjecentedge.vertex.distance > vertex.distance + adjecentedge.weight:
                        adjecentedge.vertex.distance = vertex.distance + adjecentedge.weight
                        adjecentedge.vertex.previous = vertex
                        enqueue(adjecentedge.vertex)

            self.pygameState(vertex, self.LIGHTGREY)
        for n in self.getPath(startVertexName, targetVertexName):
            self.pygameState(n, self.DARKGREEN)
        return self.getPath(startVertexName, targetVertexName)

    '''
    ###############################################################################
    #
    # def AStarSearch(self, startVertexName = None, targetVertexName = None)
    #
    # Implement your code below. 
    # Please note that no other parts of this code or provided code should be altered
    # 
    ###############################################################################
    '''

    def AStarSearch(self, startVertexName=None, targetVertexName=None):
        self.initPygame()
        # Check to see that start vertex is in Graph
        if startVertexName not in self.vertecies:
            raise KeyError("Start node not present in graph")
        # check to see if target vertex is in Graph
        if targetVertexName not in self.vertecies:
            raise KeyError("Cannot find target node in graph")

        startNode = self.vertecies[startVertexName]
        startNode.g = 0
        startNode.h = self.heuristics(startVertexName, targetVertexName)
        startNode.f = startNode.g + startNode.h
        toNode = self.vertecies[targetVertexName]

        import heapdict
        openSet = heapdict.heapdict()
        closedSet = []

        def enqueue(data):
            openSet[data] = data.f

        def dequeue():
            return openSet.popitem()[0]

        enqueue(startNode)

        while openSet:
            current = dequeue()
            self.pygameState(current, self.GREEN)
            self.pygameState(startNode, self.BLUE)
            self.pygameState(toNode, self.RED)

            if current == toNode:
                break

            current.known = True

            for adjecentedge in current.adjecent:
                if not adjecentedge.vertex.known:
                    if adjecentedge.vertex not in closedSet:
                        adjecentedge.vertex.previous = current
                        adjecentedge.vertex.g = current.g + adjecentedge.weight
                        adjecentedge.vertex.h = self.heuristics(
                            adjecentedge.vertex.name, targetVertexName)
                        adjecentedge.vertex.f = adjecentedge.vertex.g + adjecentedge.vertex.h
                        enqueue(adjecentedge.vertex)
                        self.pygameState(adjecentedge.vertex, self.PINK)
                    else:
                        if adjecentedge.vertex.g > current.g + adjecentedge.weight:
                            adjecentedge.vertex.previous = current
                            adjecentedge.g = current.g + adjecentedge.weight
                            adjecentedge.vertex.f = adjecentedge.vertex.g + adjecentedge.vertex.h
                        if adjecentedge.vertex in closedSet:
                            closedSet.remove(adjecentedge.vertex)
                            enqueue(adjecentedge.vertex)

            closedSet.append(current)

            self.pygameState(current, self.LIGHTGREY)

        for n in self.getPath(startVertexName, targetVertexName):
            self.pygameState(n, self.DARKGREEN)
        return self.getPath(startVertexName, targetVertexName)


astar = AStar(delay=0, visual=True)

# astar.readFile('minigraf.txt')
# startVertexName, targetVertexName, removed = astar.readLimitations(
#     'minigraf_xtras.txt')
# astar.readFile('astjernegraf.txt')
# startVertexName, targetVertexName, removed = astar.readLimitations('xtras.txt')
# astar.readFile('biggraph.txt')
# startVertexName, targetVertexName, removed = astar.readLimitations(
#     'biggraph_xtras.txt')
astar.readFile('AStarObligGraf.txt')
startVertexName, targetVertexName, removed = astar.readLimitations(
    'AStarObligGraf_xtras.txt')

# astar.Dijkstra(startVertexName, targetVertexName)
astar.AStarSearch(startVertexName, targetVertexName)
# astar.AStarSearch2(startVertexName, targetVertexName)


if astar.pygame:
    from pygame.locals import *
    while astar.pygame:
        for events in pg.event.get():
            if events.type == QUIT:
                pg.quit()
else:
    print(astar.getPathAsString(startVertexName, targetVertexName))
