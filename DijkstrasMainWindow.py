import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
from Utilities import sin, cos
from DataStructures import Node, PriorityQueue
import generatingmatix as g
nodeLabels = {i: chr(65+i) for i in range(11)}

def GetAngles(numNodes: int) -> list:
    #tau is 2pi
    #Make your own pi function
    step = math.tau / numNodes
    angles = [i * step for i in range(numNodes)]
    return angles


def CircularLayout(numNodes):
    radius = 1
    angles = GetAngles(numNodes)
    coordinates = {}
    for i,angle in enumerate(angles):
        x_Coord = radius * cos(angle)
        y_Coord = radius * sin(angle)
        coordinates[i] = (x_Coord, y_Coord)
    return coordinates



def DisplayGraph(adjMatrix, axs):
    numNodes: int = len(adjMatrix)
    nodeReferecnce = {}
    edgeReferences = [[] for i in range(numNodes)]
    
    #plt.figure(figsize=(8,8))
    coordinates = CircularLayout(numNodes)
    
    
    for i, (x, y) in coordinates.items():
        #How to alter properties of value
        #node  = plt.scatter(x, y, s=300, color='skyblue', zorder=3)
        node = axs[0].scatter(x, y, s=300, color='skyblue', zorder=3)
        nodeReferecnce[i] = node
        axs[0].text(x, y, nodeLabels[i], fontsize=12, ha='center', va='center')
        
    #Plotting the edges
    for i in range(numNodes):
        for j in range(i+1, numNodes):
            if adjMatrix[i][j] !=0:  
                x_Coords = [coordinates[i][0], coordinates[j][0]]
                y_Coords = [coordinates[i][1], coordinates[j][1]]
                x_mid = (x_Coords[0] + x_Coords[1]) / 2
                y_mid = (y_Coords[0] + y_Coords[1]) / 2

                # b =plt.plot(x_Coords, y_Coords, color='grey')
                edge, = axs[0].plot(x_Coords, y_Coords, color='grey')
                edgeReferences[i].append(edge)
                edgeReferences[j].append(edge)
                
                # plt.text(x_mid, y_mid-0.05, str([adjMatrix[i][j]])[1:-1], fontsize=14, ha='center', va='center',)
                axs[0].text(x_mid, y_mid-0.05, str([adjMatrix[i][j]])[1:-1], fontsize=14, ha='center', va='center',)
    
    #nodeReferecnce[2].set_color('red')
    # plt.axis('off')
    # plt.title('Dijkstras demeonstration')
    axs[0].set_title('Dijkstras Demonstration')
    axs[0].set_axis_off()
    return nodeReferecnce, edgeReferences
    
    
    

def DisplayDataStrucutures(axs):
    axs[1].set_title('Data Structures')
    #axs[1].set_axis_off()
    S =axs[1].text(0.5, 0.8, 'S{ABCDEF}', fontsize=20, ha='center', va='center', wrap=True)
    P = axs[1].text(0.5, 0.7, 'P[DFAFDAE]', fontsize=20, ha='center', va='center', wrap=True)
    #distances = axs[1].table(0.5,0.1)

def DisplayWindow(adjMatrix, sourceNode):
    fig, axs = plt.subplots(1, 2, figsize=(12, 8), gridspec_kw={'width_ratios': [2, 1]})
    nodeReference, edgeReferences = DisplayGraph(adjMatrix, axs)
    DisplayDataStrucutures(axs)
    AnimateDijkstras(fig, axs, adjMatrix, sourceNode, nodeReference, edgeReferences)
    plt.tight_layout()
    plt.show()


def AnimateDijkstras(fig, axs, adjacencyMatrix, sourceNodeIndex , nodeReferences, edgeReferences):
    #Do your own way in this function
    numNodes = len(adjacencyMatrix)
    




    distances = [float('inf')] * numNodes
    distances[sourceNodeIndex] = 0
    nodeReferences[sourceNodeIndex].set(color='lightgreen')
    #visited = [False] * numNodes
    nodesToBeVisited: list[Node] = PriorityQueue()
    visitedNodes: list[Node]= []
    for i in range(numNodes):
        priority = distances[i]
        nodesToBeVisited.Enqueue(Node(nodeLabels[i], priority, i,False))
        
    #nodesToBeVisited.queue[sourceNode].SetPriority(0)
    #sourceNode = nodesToBeVisited.ReturnNodeAtIndex(sourceNodeIndex)
    #nodesToBeVisited.ChangePriority(sourceNode, 0)
    #nodesToBeVisited.OutputQueue()

    
    
    #nodesToBeVisited.ChangePriority(, 0)
    #nodesToBeVisited.OutputQueue()
    while not nodesToBeVisited.IsEmpty():
        currentNode: Node = nodesToBeVisited.Peek()
        nodesToBeVisited.Dequeue()
        currentIndex = currentNode.GetIndex()
        visitedNodes.append(currentNode)
        if currentIndex != sourceNodeIndex:
            nodeReferences[currentIndex].set(color='darksalmon')
        HighlightEdgesOfNode(edgeReferences[currentIndex])
        plt.pause(2)
        

        for neighbourIndex in range(numNodes):
            weight = adjacencyMatrix[currentIndex][neighbourIndex]
            
            #neighbourNode of type None when neighbourNode has already been visited
            neighbourNode: Node = nodesToBeVisited.GetNodeByIndex(neighbourIndex)
            if weight > 0 and neighbourNode != None:
                newDistance = distances[currentIndex] + weight
                

                if newDistance < distances[neighbourIndex]:
                    distances[neighbourIndex] = newDistance
                    nodesToBeVisited.ChangePriority(neighbourNode,newDistance)
        
        DehighlightEdgesOfNode(edgeReferences[currentIndex])
    DehighlightAllNodes(nodeReferences)
        
    #print(distances)
    for i in range(numNodes):
        print(f"Shortest distance to {nodeLabels[i]} is {distances[i]}")
    
    for i in range(numNodes):
        visitedNodes[i].OutputNode()

    #plt.show()

def HighlightEdgesOfNode(nodeEdges):
    for edge in nodeEdges:
        edge.set(color='red')

def DehighlightEdgesOfNode(nodeEdges):
    for edge in nodeEdges:
        edge.set(color='grey')

def DehighlightAllNodes(nodeReferences):
    for node in nodeReferences.values():
        node.set(color = 'skyblue')
if __name__ == '__main__':
    test = [[0,4,3,7,0,0,0],
                [4,0,0,1,0,4,0],
                [3,0,0,3,5,0,0],
                [7,1,3,0,2,2,7],
                [0,0,5,2,0,0,2],
                [0,4,0,2,0,0,4],
                [0,0,0,7,2,4,0]]
    
    
    #For the animation highlight a node being optimised and every edge connected to said node. And add the data structure
    
    #Maker ur own version
    num = 8
    b = g.matrix(5,75)
    #DisplayWindow(test)
    DisplayWindow(test, 0)