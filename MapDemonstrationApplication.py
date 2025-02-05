import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import math
import matplotlib.animation as animation
from DataStructures import MinHeap
from Utilities import sin,cos, ConvertDegreesToRadians, ConvertKilometresToMiles
from tkinter import messagebox

PATH_FINDING_ALGORITHMS = {'A-Star': 0, 'Dijkstras':1}
class MapDemonstrationWindow():
    def __init__(self, filepath, algorithm, useMiles):
        self.graph =  ox.load_graphml(filepath=filepath)
        try:
            self.algorithmId = PATH_FINDING_ALGORITHMS[algorithm]
        except:
            raise('Unexpected value passed for algorithmId')
        self.useMiles = useMiles
        self.click_coords = []
        self.figAndAxis = plt.subplots()
        self.fig = self.figAndAxis[0]
        self.ax = self.figAndAxis[1]

    def OnClick(self, event):
        x_Coord = event.xdata
        y_Coord = event.ydata
        if x_Coord and y_Coord and len(self.click_coords) < 2: #Ensuring valid clicks
            self.click_coords.append((x_Coord, y_Coord))
            self.HighlightPoints()

        if len(self.click_coords) == 2:
            print('Now begin animating')
            #plt.close()
            #animate_astar(self.graph, self.click_coords[0], self.click_coords[1])
            self.ax.clear()
            animator = NetworkAnimator(self.graph,self.click_coords[0], self.click_coords[1], self.algorithmId, self.useMiles, self.figAndAxis)
            self.fig.canvas.draw_idle()
        

        # If two points are clicked, highlight them
        
    def HighlightPoints(self):
        # Clear the previous plot
        self.ax.clear()

        ox.plot_graph(self.graph, ax=self.ax, show=False, close=False, node_size=5, edge_linewidth=0.3, edge_color="gray")

        # If the first click exists, highlight the first point
        if len(self.click_coords) >= 1:
            (x_Coord1, y_Coord1) = self.click_coords[0]
            self.ax.scatter(x_Coord1, y_Coord1, c='g', s=100, marker='.')  # First point in red

        # If the second click exists, highlight the second point
        if len(self.click_coords) >= 2:
            (x_Coord2, y_Coord2) = self.click_coords[1]
            self.ax.scatter(x_Coord2, y_Coord2, c='r', s=100, marker='.')  

        # Redraw the figure to show the updated plot
        plt.draw()
        
    def DisplayNetwork(self):
        # shortestPath = nx.shortest_path(self.graph, source=self.startNode, target=self.endNode, weight='length')
        ox.plot_graph(self.graph, ax=self.ax, show=False, close=False, node_size=5, edge_linewidth=0.3, edge_color="gray")
        #self.ax.set_facecolor('black')
        # ax.scatter(self.startCoords[1], self.startCoords[0], c='r', s=100, marker='x') # Start node
        # ax.scatter(self.endCoords[1], self.endCoords[0], c='g', s=100, marker='x') #End node
        # ox.plot_graph_route(self.graph, shortestPath, route_linewidth=4, route_color='r', orig_dest_size=100, ax=ax)
       
        #Event listener waiting for a button press 
        cid = self.fig.canvas.mpl_connect('button_press_event',  self.OnClick)
        plt.show()

    
    def GetGraph(self):
        return self.graph

class NetworkAnimator():
    def __init__(self, graph, startCoord, endCoord, algorithmId, useMiles, figAndAxis, edgeSkipFactor = 20, interval = 0.5):
        self.graph = graph
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
        #self.fig.canvas.mpl_connect("draw_event", lambda: self.on_animation_complete())
        self.StartAnimation()
    
    def StartAnimation(self):
        GRAPH = self.graph
        startNode = ox.nearest_nodes(GRAPH, self.startCoord[0], self.startCoord[1])
        endNode = ox.nearest_nodes(GRAPH, self.endCoord[0], self.endCoord[1])
        highlightingEdgeColour = None
        match self.algorithmId:
            #Each case pre computes pathfinding algorithm before running to get the path, explored edges and length of path
            case 0:
                path,  exploredEdges, lengthOfPath = AStar(GRAPH, startNode, endNode)
                print('Using A-Star')
                highlightingEdgeColour = 'blue'
            case 1:
                path,  exploredEdges, lengthOfPath = Dijkstra(GRAPH, startNode, endNode)
                highlightingEdgeColour = 'orange'
                print('Using Dijkstras')
            case _: # If does not match any use AStar
                path,  exploredEdges, lengthOfPath = AStar(GRAPH, startNode, endNode)
        #Converting to Kilometres
        self.lengthOfPath = round(lengthOfPath / 1000, 1)
        if self.useMiles:
            self.lengthOfPath = ConvertKilometresToMiles(self.lengthOfPath)
        numberOfFrames = len(exploredEdges) // self.edgeSkipFactor + len(path)
        #Intitialising plot
        #fig, ax = plt.subplots(figsize=(10, 10))
        ax= self.ax
        fig = self.fig 
        ox.plot_graph(GRAPH, ax=ax, show=False, close=False, node_size=5, edge_linewidth=0.3, edge_color="gray")

        startNodeMarker, = ax.plot(GRAPH.nodes[startNode]['x'], GRAPH.nodes[startNode]['y'], 'go', markersize=6, label="Start Node")
        endNodeMarker, = ax.plot(GRAPH.nodes[endNode]['x'], GRAPH.nodes[endNode]['y'], 'ro', markersize=6, label="End Node")
        shortestPathLine, = ax.plot([], [], '-', color='red', linewidth=3, label="Shortest Path")
        exploredEdgesLine, = ax.plot([], [], '-', color=highlightingEdgeColour, linewidth=1, label="Visited Edges")
        
        #Updates animation frame by frame
        def update(frameNum):
            edge_x = []
            edge_y = []
            #Highlighting explored Edges. 
            for edge in exploredEdges[:frameNum* self.edgeSkipFactor]: # Highlighting 'edgeSkipFactor' edges per frame
                edge_x.extend([GRAPH.nodes[edge[0]]['x'], GRAPH.nodes[edge[1]]['x'], None])
                edge_y.extend([GRAPH.nodes[edge[0]]['y'], GRAPH.nodes[edge[1]]['y'], None])
            exploredEdgesLine.set_data(edge_x, edge_y)

            #If the number of the frame is greater than total explored Edges then all edges processed and we can display shortest path
            if frameNum >= len(exploredEdges) // self.edgeSkipFactor:
                path_x = [GRAPH.nodes[n]['x'] for n in path]
                path_y = [GRAPH.nodes[n]['y'] for n in path]
                shortestPathLine.set_data(path_x, path_y)

            if frameNum == numberOfFrames - 1:
                self.on_animation_complete()
            
                

            return shortestPathLine, exploredEdgesLine
        
        #Number of frames set to the number the amount of edges we will be highlighting and the length of the path.
        self.anim = animation.FuncAnimation(fig, update, frames=numberOfFrames, interval=self.interval, repeat=False)
        plt.legend()
        
        #plt.show()

    def on_animation_complete(self):
        print('Animation Complete')
        messagebox.showinfo(title='Length Of Path', 
                            message=f"The length of path found is {round(self.lengthOfPath,1)} {"Miles" if self.useMiles else "Kilometres"}")#Conditionally show Miles or kilometres
def HaverSineDistance(graph: nx.MultiDiGraph, node1: int,  node2: int) -> float:
    coordinateNode1 = NodeToCordiante(graph,node1)
    coordinateNode2 = NodeToCordiante(graph, node2)
    lat1 = coordinateNode1[0]
    lon1 = coordinateNode1[1]
    lat2 = coordinateNode2[0]
    lon2 = coordinateNode2[1]

    lat1 = ConvertDegreesToRadians(lat1)
    lon1 = ConvertDegreesToRadians(lon1)
    lat2 = ConvertDegreesToRadians(lat2)
    lon2 = ConvertDegreesToRadians(lon2)
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of Earth in kilometers
    r = 6371.0
    
    # Calculate the result
    distance = c * r
    
    return distance

def EuclideanDistance(graph, node1, node2):
    coordinateNode1 = NodeToCordiante(graph,node1)
    coordinateNode2 = NodeToCordiante(graph, node2)
    distanceLatitude = abs(coordinateNode1[0]-coordinateNode2[0])
    distanceLongitude = abs(coordinateNode1[1] - coordinateNode2[1])
    distance = math.sqrt(distanceLatitude**2 + distanceLongitude**2)
    return distance

def NodeToCordiante(graph, node):
    return graph.nodes[node]['x'], graph.nodes[node]['y']

def GetPath(cameFrom, currentNode, startNode) -> list:
    path = []
    while currentNode in cameFrom:
        path.append(currentNode)
        currentNode = cameFrom[currentNode]
    path.append(startNode)
    #Could use stack?
    return path[::-1] #Return reversed path


def AStar(graph: nx.MultiDiGraph, startNode: int, endNode: int):
    openList = MinHeap()
    closedSet = set()
    cameFrom = {}# Used to track the path
    exploredEdges = []
    #Initialising g and f  for every node to be infinity
    g_score = {node: float('inf') for node in graph.nodes}
    f_score = {node: float('inf') for node in graph.nodes}
    g_score[startNode] = 0
    initialHeuristicEstimate = HaverSineDistance(graph, startNode, endNode)
    f_score[startNode] = g_score[startNode] + initialHeuristicEstimate
    openList.Insert((f_score[startNode], startNode))
   

    while not openList.IsEmpty():
        currentNodeAndFval = openList.RemoveMinValue()
        currentNode = currentNodeAndFval[1]
        if currentNode == endNode:
            path = GetPath(cameFrom, currentNode, startNode)
            lengthOfPath = g_score[endNode]
            nodesAccessed = openList.GetHeapLength()
            return path,  exploredEdges, lengthOfPath
        closedSet.add(currentNode)

        for neighbourNode in graph.neighbors(currentNode):
            if neighbourNode in closedSet:
                continue
            distance = graph[currentNode][neighbourNode][0]['length'] 
            estimateGScore = distance + g_score[currentNode]

            if estimateGScore < g_score[neighbourNode]:
                cameFrom[neighbourNode] = currentNode
                g_score[neighbourNode] = estimateGScore
                f_score[neighbourNode] = g_score[neighbourNode] + HaverSineDistance(graph, neighbourNode, endNode)
                neighbourNodeAndFVal = (f_score[neighbourNode], neighbourNode)
                exploredEdges.append((currentNode, neighbourNode))
                openList.Insert(neighbourNodeAndFVal)
                
            
    #No path found
    return [],  exploredEdges, None

def Dijkstra(graph: nx.MultiDiGraph, startNode: int, endNode: int):
    nodesToBeVisited = MinHeap()
    visitedNodes = set()
    cameFrom = {}
    exploredEdges = []
    distances = {node: float('inf') for node in graph.nodes}
    distances[startNode] = 0
    nodesToBeVisited.Insert((distances[startNode], startNode))

    while not nodesToBeVisited.IsEmpty():
        currentNodeAndDistance = nodesToBeVisited.RemoveMinValue()
        currentNode = currentNodeAndDistance[1]
        if currentNode == endNode:
            path = GetPath(cameFrom, currentNode, startNode)
            lengthOfPath = distances[endNode]
            print(f'This is the length {lengthOfPath}')
            return path,  exploredEdges, lengthOfPath
        visitedNodes.add(currentNode)

        for neighbourNode in graph.neighbors(currentNode):
            if neighbourNode in visitedNodes:
                continue
            currentDistance = distances[currentNode] + graph[currentNode][neighbourNode][0]['length']
            if currentDistance < distances[neighbourNode]:
                cameFrom[neighbourNode] = currentNode
                distances[neighbourNode] = currentDistance
                neighbourNodeAndDistance = (distances[neighbourNode], neighbourNode)
                exploredEdges.append((currentNode, neighbourNode))
                nodesToBeVisited.Insert(neighbourNodeAndDistance)            

    #No path found
    return [], exploredEdges, None
                





if __name__ == "__main__":
    window = MapDemonstrationWindow("Networks/LondonNetwork.graphml")
    window.DisplayNetwork()
    # figax = plt.subplots(figsize=(10, 10))
    # graph =  ox.load_graphml(filepath="Networks/LondonNetwork.graphml")
    # startCoords = (51.5017, -0.1419)  
    # endCoords = (51.53, -0.15)
    # x  = NetworkAnimator(graph, startCoords, endCoords, figax)

    
    
    # startNode = ox.distance.nearest_nodes(graph, startCoords[1], startCoords[0])
    # endNode = ox.distance.nearest_nodes(graph, endCoords[1], endCoords[0])
    # length = nx.shortest_path_length(graph, startNode, endNode, weight='length')

    # print(f"Actual length is {length}")
    # ox.plot_graph(graph, ax=ax, show=False, close=False, node_size=5, edge_linewidth=0.3, edge_color="gray",bgcolor='black')
    # ax.set_facecolor('black')
    # path = AStar(graph, startNode, endNode)
    # #Gett cordinates of nodes on the path
    # path_x = [graph.nodes[node]['x'] for node in path]
    # path_y = [graph.nodes[node]['y'] for node in path]
    # ax.plot(path_x, path_y, linewidth=2, color="red", label="A* Shortest Path")
    # plt.legend()
    # plt.show()

    #animate_astar(ox.load_graphml(filepath="Networks/LondonNetwork.graphml"), (51.5017, -0.1419), (51.53, -0.15))