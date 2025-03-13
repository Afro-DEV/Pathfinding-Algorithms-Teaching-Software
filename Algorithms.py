import time
import random
import networkx as nx
import math
from Utilities import cos, sin, ConvertDegreesToRadians
from DataStructures import MinHeap, LinkedListNode, Stack

def GenerateAdjacencyMatrix(numberOfNodes: int,densityVal: float) -> list[list[int]]:
    '''
    Generate an adjacency matrix that represents an undirected simple graph.
    The graph will have random weights between 2 and 12.
    The graph will be of size corresponding to the numberOfNodes parameter.
    The graph will have connectivity corresponding to the densityVal parameter
    '''
    matrix = [[0 for x in range(numberOfNodes)] for y in range(numberOfNodes)] # Populating an n x n matrix with only zeroes
    for i in range(numberOfNodes):
        for j in range(i+1, numberOfNodes):
            pValue = random.random() #Generates random number between 0 and 1
            if pValue < densityVal/100: # if random number is less than specified density value then we create an edge. 
                matrix[i][j] = random.randint(2,20) # Assign edge random weighting
                matrix[j][i] = matrix[i][j] # Update adjacency matrix connection going to the other way to create an undirected edge.
    return matrix

#Used to output each array in adjacency matrix for debugging
def OutputMatrix(matrix):
    for each in matrix:
        print(each)

def HaversineDistance(graph: nx.MultiDiGraph, node1: int,  node2: int) -> float:
    '''Estimate the distance in Kilometres between 2 points on Earth's surface '''
    coordinateNode1 = NodeToCoordinate(graph,node1)
    coordinateNode2 = NodeToCoordinate(graph, node2)

    #Get latitude and longitude of nodes
    lat1 = coordinateNode1[0]
    lon1 = coordinateNode1[1]
    lat2 = coordinateNode2[0]
    lon2 = coordinateNode2[1]

    lat1,lon1, lat2, lon2 = map(ConvertDegreesToRadians, [lat1,lon1,lat2,lon2]) # Convert degrees latitude and longitude into radians
    
    # Apply Haversine formula
    distanceLat = lat2 - lat1
    distanceLon = lon2 - lon1
    a = sin(distanceLat / 2)**2 + cos(lat1) * cos(lat2) * sin(distanceLon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of Earth in kilometres
    RADIUS_EARTH = 6371.0
    
    distance = c * RADIUS_EARTH
    return distance

def EuclideanDistance(graph: nx.MultiDiGraph,node1: int, node2: int)-> float:
    '''Calculate the absolute distance between 2 nodes latitude and longitude'''
    coordinateNode1 = NodeToCoordinate(graph,node1)
    coordinateNode2 = NodeToCoordinate(graph, node2)
    distanceLatitude = abs(coordinateNode1[0]-coordinateNode2[0])
    distanceLongitude = abs(coordinateNode1[1] - coordinateNode2[1])
    distance = math.sqrt(distanceLatitude**2 + distanceLongitude**2)
    return distance

def NodeToCoordinate(graph: nx.MultiDiGraph, node: int) -> tuple[float,float]:
    '''Gets coordinates of nx multi graph '''
    return graph.nodes[node]['x'], graph.nodes[node]['y']



def GetPathLinkedList(endListNode: LinkedListNode) -> list:
    '''Given the last node of a linked list, traverse and reverse linked list
        to return path from start node to end node.'''
    stack = Stack()
    path = []
    node: LinkedListNode = endListNode  # Start from the last node which is the target node
    while node:
        stack.Push(node.GetData())  # Add the node's value to stack
        node = node.GetParent()  # Move backwards using the reference

    while not stack.IsEmptyStack():
        path.append(stack.Pop())
    
    return path #Return path from the start node to the end node.


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
                #Increase heuristic by a multiplier for stronger weighting 
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
    pass
