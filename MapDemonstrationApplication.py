import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import math
import matplotlib.animation as animation
import time
from tkinter import messagebox
from DataStructures import MinHeap, Stack, LinkedListNode
from Utilities import sin,cos, ConvertDegreesToRadians, ConvertKilometresToMiles
from NetworkGenerator import BaseNetworkGenerator
from matplotlib.widgets import Button



class MapDemonstrationWindow():
    def __init__(self, network: str, algorithm: str, useMiles: bool):
        PATH_FINDING_ALGORITHMS_ID = {'A-Star': 0, 'Dijkstras':1}
        self.filepath = self.GetNetworkSelectedFilePath(network)

        if not BaseNetworkGenerator.CheckFileExists(self.filepath):
            BaseNetworkGenerator.GenerateAllMissingNetworks()

        self.__graph =  ox.load_graphml(filepath=self.filepath) #Load graph from file path as type NetworxX multi d Graph 

        #Create Dictionary to store styles for the grpah     
        self.GRAPH_STYLES = {'EdgeColour': "Grey",
                            'EdgeWidth': 0.3,
                            'StartNodeColour': 'limegreen',
                            'EndNodeColour': '#ff0000', 
                            'NodeSize': 2 }
        try:
            self.algorithmId = PATH_FINDING_ALGORITHMS_ID[algorithm]
        except:
            #In case the user manages to write into the dropdown box which should not be possible
            raise('Unexpected value passed for algorithmId')
            
        self.useMiles = useMiles
        self.click_coords = []
        self.figAndAxis = plt.subplots()
        self.fig = self.figAndAxis[0]
        self.ax = self.figAndAxis[1]

        self.AddUndoButton()

    def AddUndoButton(self):
        button_ax = self.fig.add_axes([0.8, 0.01, 0.1, 0.05])  # Position of the button
        self.undoButton = Button(button_ax, 'Undo Click')
        self.undoButton.on_clicked(self.UndoLastClick)

    def RemoveUndoButton(self):
        if hasattr(self, 'undoButton'):
            self.undoButton.ax.set_visible(False)
            self.fig.canvas.draw_idle() # Refreshing figure to update UI
    
    def UndoLastClick(self, event):
        if self.click_coords:
            self.click_coords.pop()  # Remove last clicked coordinate
            self.HighlightPoints() #Rehighlights points removing the highlighted last click

    def GetNetworkSelectedFilePath(self, networkSelected):
        #Parameterised File path
        return f"Networks/{networkSelected}Network.graphml"


    def DisplayNetwork(self):

        ox.plot_graph(self.__graph, 
                      ax=self.ax, 
                      show=False,
                       close=False, 
                      bgcolor="black",
                      node_size=self.GRAPH_STYLES['NodeSize'], 
                      edge_linewidth=self.GRAPH_STYLES['EdgeWidth'],
                      edge_color=self.GRAPH_STYLES['EdgeColour'])
        self.ax.set_facecolor('black')

        #Event listener waiting for a button press 
        cid = self.fig.canvas.mpl_connect('button_press_event',  self.OnClick)
        plt.show()

    def OnClick(self, event):
        if event.inaxes != self.ax:  # Ignore clicks outside the main plot area
            return
        x_Coord = event.xdata
        y_Coord = event.ydata

                
        if self.CheckValidClick(x_Coord, y_Coord) and len(self.click_coords) < 2: #Ensuring valid clicks
            #If second click cordinate is not far enough away from first click do not add to click coords.
            if len(self.click_coords) == 1 and not self.CheckIfCoordsAreSpaced(x_Coord, y_Coord): 
                return 
            self.click_coords.append((x_Coord, y_Coord))
            self.HighlightPoints()

        if len(self.click_coords) == 2:# If two points are clicked, highlight them
            print('Now begin animating')
            self.ax.clear()
            self.RemoveUndoButton()
            animator = NetworkAnimator(self.__graph,self.click_coords[0], self.click_coords[1], self.algorithmId, self.useMiles, self.figAndAxis, self.GRAPH_STYLES)
            animator.StartAnimation()
            self.fig.canvas.draw_idle()
    
    def CheckIfCoordsAreSpaced(self, x_Coord, y_Coord):
        if ox.nearest_nodes(self.__graph, x_Coord, y_Coord) == ox.nearest_nodes(self.__graph,  self.click_coords[0][0], self.click_coords[0][1]):
            return False
        return True
    
    def CheckValidClick(self, x_Coord, y_Coord):
        return x_Coord != None or y_Coord !=None

        
        
    def HighlightPoints(self):
        # Clear the previous plot
        self.ax.clear()

        ox.plot_graph(self.__graph, 
                      ax=self.ax, 
                      show=False,
                       close=False, 
                      bgcolor="black",
                      node_size=self.GRAPH_STYLES['NodeSize'], 
                      edge_linewidth=self.GRAPH_STYLES['EdgeWidth'],
                      edge_color=self.GRAPH_STYLES['EdgeColour'])

        # If the first click exists, highlight the first point
        if len(self.click_coords) >= 1:
            (x_Coord1, y_Coord1) = self.click_coords[0]
            self.ax.scatter(x_Coord1, y_Coord1, c=self.GRAPH_STYLES['StartNodeColour'], s=100, marker='.')  # First point in green

        # If the second click exists, highlight the second point
        if len(self.click_coords) >= 2:
            (x_Coord2, y_Coord2) = self.click_coords[1]
            self.ax.scatter(x_Coord2, y_Coord2, c=self.GRAPH_STYLES['EndNodeColour'], s=100, marker='.')  

        # Redraw the figure to show the updated plot
        plt.draw()
        
    

    
    def GetGraph(self):
        return self.__graph

class NetworkAnimator():
    def __init__(self, graph, startCoord, endCoord, algorithmId, useMiles, figAndAxis, GRAPH_STYLES, edgeSkipFactor = 20, interval = 0.5):
        self.__graph = graph
        self.GRAPH_STYLES = GRAPH_STYLES
        self.startCoord = startCoord
        self.endCoord = endCoord
        self.algorithmId = algorithmId
        self.useMiles = useMiles
        self.edgeSkipFactor = edgeSkipFactor
        self.interval = interval
        #Used to hold the FuncAnimation Object
        self.anim = None
        self.fig = figAndAxis[0]
        self.ax = figAndAxis[1]
        self.startTime = time.time()
        #self.fig.canvas.mpl_connect("draw_event", lambda: self.on_animation_complete())
        
        
    
    def StartAnimation(self):
        GRAPH = self.__graph
        startNode = ox.nearest_nodes(GRAPH, self.startCoord[0], self.startCoord[1])
        endNode = ox.nearest_nodes(GRAPH, self.endCoord[0], self.endCoord[1])
        highlightingEdgeColour = None
        
        match self.algorithmId:
            #Each case pre computes pathfinding algorithm before running to get the path, explored edges and length of path
            case 0:
                path,  exploredEdges, lengthOfPath = AStar(GRAPH, startNode, endNode)
                highlightingEdgeColour = '#2BD9FF'
                #As A* is a faster algorithm the edgeSkip Factor must be decremented
                #self.edgeSkipFactor = self.edgeSkipFactor//2
            case 1:
                path,  exploredEdges, lengthOfPath = Dijkstra(GRAPH, startNode, endNode)
                highlightingEdgeColour = '#FF512B'
            case _: # If does not match any use AStar
                path,  exploredEdges, lengthOfPath = AStar(GRAPH, startNode, endNode)
        
        
        
        if lengthOfPath == None:
            messagebox.showinfo('No Path', 'No path was found between Points')
            return
        
        #Converting to Kilometres
        self.lengthOfPath = round(lengthOfPath / 1000, 1)
        if self.useMiles:
            self.lengthOfPath = ConvertKilometresToMiles(self.lengthOfPath)
        numberOfFrames = len(exploredEdges) // self.edgeSkipFactor + len(path)
        #Intitialising plot
        #fig, ax = plt.subplots(figsize=(10, 10))
        ax= self.ax
        fig = self.fig 
        ox.plot_graph(self.__graph, 
                      ax=self.ax, 
                      show=False,
                       close=False, 
                      bgcolor="black",
                      node_size=self.GRAPH_STYLES['NodeSize'], 
                      edge_linewidth=self.GRAPH_STYLES['EdgeWidth'],
                      edge_color=self.GRAPH_STYLES['EdgeColour'])
        
        #Adding the key for the graph
        startNodeMarker, = ax.plot(GRAPH.nodes[startNode]['x'], GRAPH.nodes[startNode]['y'],  'o', color=self.GRAPH_STYLES['StartNodeColour'], markersize=6, zorder =3, label="Start Node")
        endNodeMarker, = ax.plot(GRAPH.nodes[endNode]['x'], GRAPH.nodes[endNode]['y'], 'o', color=self.GRAPH_STYLES['EndNodeColour'], markersize=6, zorder=3, label="End Node")
        shortestPathLine, = ax.plot([], [], '-', color='yellow', linewidth=5, label="Shortest Path")
        exploredEdgesLine, = ax.plot([], [], '-', color=highlightingEdgeColour, linewidth=1, zorder=1, label="Visited Edges")
        ax.legend(loc='best', fontsize='small', frameon=True, title= 'Key')

        #shortestPathLine, = plt.plot([], [], 'y', label="Shortest Path")  
        
        #Updates animation frame by frame
        def update(frameNum):
            edge_x = []
            edge_y = []
            #Highlighting explored Edges. 
            for edge in exploredEdges[:frameNum* self.edgeSkipFactor]: # Highlighting 'edgeSkipFactor' edges per frame
                edge_x.extend([GRAPH.nodes[edge[0]]['x'], GRAPH.nodes[edge[1]]['x'], None])
                edge_y.extend([GRAPH.nodes[edge[0]]['y'], GRAPH.nodes[edge[1]]['y'], None])
            exploredEdgesLine.set_data(edge_x, edge_y)

            #If the number of the frame is greater than total explored Edges then all edges processed and we can display shortest path, reached final frame
            if frameNum >= len(exploredEdges) // self.edgeSkipFactor:
                path_x = [GRAPH.nodes[n]['x'] for n in path]
                path_y = [GRAPH.nodes[n]['y'] for n in path]
                shortestPathLine.set_data(path_x, path_y)
                # Only trigger message box once
                if not hasattr(self, "messageShown"):  # Check if message was already shown
                    self.messageShown = True  # Mark that the message was displayed
                    plt.draw()  # Ensure UI updates
                    plt.pause(0.1)  # Small delay to ensure UI refresh
                    self.OnAnimationComplete()  # Show the message box


            return shortestPathLine, exploredEdgesLine
        
        #Number of frames set to the number the amount of edges we will be highlighting and the length of the path.
        self.anim = animation.FuncAnimation(fig, update, frames=numberOfFrames, interval=self.interval, repeat=False)

        
        #plt.show()

    def OnAnimationComplete(self):
        print('Animation Complete')
        self.endTime = time.time()
        timeTook = self.endTime-self.startTime
        units = 'Miles' if self.useMiles else 'Kilometres' #Conditionally show Miles or kilometres
        messagebox.showinfo(title='Length Of Path', 
                            message=f"The length of path found is {round(self.lengthOfPath,1)} {units} and was found in {round(timeTook, 2)}s") 
        
def HaversineDistance(graph: nx.MultiDiGraph, node1: int,  node2: int) -> float:
    '''Estimate the distance in Kilometres between 2 points on Earth's surface '''
    coordinateNode1 = NodeToCoordinate(graph,node1)
    coordinateNode2 = NodeToCoordinate(graph, node2)

    #Get lattitude and longitude of nodes
    lat1 = coordinateNode1[0]
    lon1 = coordinateNode1[1]
    lat2 = coordinateNode2[0]
    lon2 = coordinateNode2[1]

    lat1,lon1, lat2, lon2 = map(ConvertDegreesToRadians, [lat1,lon1,lat2,lon2]) # Convert degrees lattitude and longitude into radians
    
    # Apply Haversine formula
    distanceLat = lat2 - lat1
    distanceLon = lon2 - lon1
    a = sin(distanceLat / 2)**2 + cos(lat1) * cos(lat2) * sin(distanceLon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of Earth in kilometers
    RADIUS_EARTH = 6371.0
    
    distance = c * RADIUS_EARTH
    return distance

def EuclideanDistance(graph, node1, node2):
    '''Calculate the aboslute distance between 2 nodes lattitude and longitude'''
    coordinateNode1 = NodeToCoordinate(graph,node1)
    coordinateNode2 = NodeToCoordinate(graph, node2)
    distanceLatitude = abs(coordinateNode1[0]-coordinateNode2[0])
    distanceLongitude = abs(coordinateNode1[1] - coordinateNode2[1])
    distance = math.sqrt(distanceLatitude**2 + distanceLongitude**2)
    return distance

def NodeToCoordinate(graph, node) -> tuple[float,float]:
    return graph.nodes[node]['x'], graph.nodes[node]['y']



def GetPath(cameFrom, currentNode, startNode) -> list:
    path = []
    while currentNode in cameFrom:
        path.append(currentNode)
        currentNode = cameFrom[currentNode]
    path.append(startNode)
    #Could use stack?
    return path[::-1] #Return reversed path

def GetPathLinkedList(endListNode: LinkedListNode) -> list:
    stack = Stack()
    path = []
    node: LinkedListNode = endListNode  # Start from the last node which is the target node
    while node:
        stack.Push(node.GetData())  # Add the node's value to stack
        node = node.GetParent()  # Move backwards using the reference

    while not stack.IsEmptyStack():
        path.append(stack.Pop())
    
    return path 


def AStar(graph: nx.MultiDiGraph, startNode: int, endNode: int , heuristicWeight = 850):
    #Initialise the open list(priority queue) and closedSet(visited nodes)
    openList = MinHeap()
    closedSet = set()

    cameFrom = {}# Dictionary  to track the path
    exploredEdges = []
    #Initialising g and f  for every node to be infinity
    g_score = {node: float('inf') for node in graph.nodes}
    f_score = {node: float('inf') for node in graph.nodes}

    g_score[startNode] = 0

    #Calculate initial heuristic estimate from start to end node. 
    initialHeuristicEstimate = HaversineDistance(graph, startNode, endNode)

    f_score[startNode] = g_score[startNode] + initialHeuristicEstimate

    #Insert the start node into the open list with f score
    openList.Insert((f_score[startNode], startNode))
    while not openList.IsEmpty():
        #Get node with the lowest f score
        _, currentNode = openList.RemoveMinValue()

        if currentNode == endNode:
            path = GetPathLinkedList(cameFrom[endNode]) #Reconstruct path.
            lengthOfPath = g_score[endNode]
            return path,  exploredEdges, lengthOfPath
        closedSet.add(currentNode)

        #Iterate over neighbours of the current node
        for neighbourNode in graph.neighbors(currentNode):
            #Skip neighbour node if already visited
            if neighbourNode in closedSet:
                continue
            #Get length from current node to neighbour node
            distance = graph[currentNode][neighbourNode][0]['length']
            provisionalGScore = distance + g_score[currentNode]

            #if provisional g score is less than current g score update the score 
            if provisionalGScore < g_score[neighbourNode]:
                #Use memory reference to track the parent node for path reconstruction.
                cameFrom[neighbourNode] = LinkedListNode(neighbourNode, parent=cameFrom.get(currentNode))
                g_score[neighbourNode] = provisionalGScore
                #Increase heuristic by a multiplier for strongr weighting 
                f_score[neighbourNode] = provisionalGScore + HaversineDistance(graph, neighbourNode, endNode) * heuristicWeight

                #Update new f score for neighbour node
                openList.Insert((f_score[neighbourNode], neighbourNode))

                #Mark edge as explored
                exploredEdges.append((currentNode, neighbourNode))
                
            
    #No path found
    return [],  exploredEdges, None




def Dijkstra(graph: nx.MultiDiGraph, startNode: int, endNode: int):
    nodesToBeVisited = MinHeap()
    visitedNodes = set()

    cameFrom = {}
    exploredEdges = []

    distances = {node: float('inf') for node in graph.nodes} #Initialise the distance to every node as infinity.
    distances[startNode] = 0
    nodesToBeVisited.Insert((distances[startNode], startNode)) #Mark start node as first node to be visited

    while not nodesToBeVisited.IsEmpty():
        currentNodeAndDistance = nodesToBeVisited.RemoveMinValue()
        currentNode = currentNodeAndDistance[1]
        if currentNode == endNode:
            path = GetPathLinkedList(cameFrom[endNode]) #Reconstruct path
            lengthOfPath = distances[endNode]
            return path,  exploredEdges, lengthOfPath
        visitedNodes.add(currentNode) # add node to visited nodes set

        for neighbourNode in graph.neighbors(currentNode): #Explore ever neighbour node.
            if neighbourNode in visitedNodes: #Skip node if already visited
                continue
            currentDistance = distances[currentNode] + graph[currentNode][neighbourNode][0]['length']
            if currentDistance < distances[neighbourNode]:
                #Add node to linked list for path reconstruction
                cameFrom[neighbourNode] = LinkedListNode(neighbourNode, parent=cameFrom.get(currentNode))
                distances[neighbourNode] = currentDistance
                neighbourNodeAndDistance = (distances[neighbourNode], neighbourNode)
                #Mark edge as explored
                exploredEdges.append((currentNode, neighbourNode))
                nodesToBeVisited.Insert(neighbourNodeAndDistance)            

    #No path found
    return [], exploredEdges, None
                





if __name__ == "__main__":
    window = MapDemonstrationWindow("London", algorithm='Dijkstras', useMiles=False)
    window.DisplayNetwork()
    # window = MapDemonstrationWindow("NewYork", algorithm='Dijkstras', useMiles=True)
    # window.DisplayNetwork()




    # GRAPH_STYLES = {'EdgeColour': "Grey",
    #                         'EdgeWidth': 0.3,
    #                         'StartNodeColour': 'limegreen',
    #                         'EndNodeColour': '#ff0000', 
    #                         'NodeSize': 2 }
    # figax = plt.subplots(figsize=(10, 10))
    # graph =  ox.load_graphml(filepath="Networks/LondonNetwork.graphml")
    # startCoords = (51.5017, -0.1419)  
    # endCoords = (51.53, -0.15)
    # x  = NetworkAnimator(graph, startCoords, endCoords,1, True, figax, GRAPH_STYLES)
    # plt.show()
    
    # startNode = ox.distance.nearest_nodes(graph, startCoords[1], startCoords[0])
    # endNode = ox.distance.nearest_nodes(graph, endCoords[1], endCoords[0])
   
    # startTime = time.time()
    # path, exploredEdges, length = Dijkstra(graph, startNode, endNode)
    # endTime = time.time()
    # print(endTime-startTime)
    # print(path)
    # #Gett cordinates of nodes on the path
    # path_x = [graph.nodes[node]['x'] for node in path]
    # path_y = [graph.nodes[node]['y'] for node in path]
    # ax.plot(path_x, path_y, linewidth=2, color="red", label="A* Shortest Path")
    # plt.legend()
    # plt.show()

    #animate_astar(ox.load_graphml(filepath="Networks/LondonNetwork.graphml"), (51.5017, -0.1419), (51.53, -0.15))