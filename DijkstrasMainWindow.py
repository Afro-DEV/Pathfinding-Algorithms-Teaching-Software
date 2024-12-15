import matplotlib.pyplot as plt
import math
from Utilities import sin, cos
from DataStructures import Node, PriorityQueue
import generatingmatix as g
import random
from adjustText import adjust_text
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from time import sleep
nodeLabels = {i: chr(65+i) for i in range(11)}

class AnimationController():
    def __init__(self, nodeReferences, edgeReferences, visitedNodesText, nodesToBeVisitedText, distancesTable, tableData, axs, fig):
        self.__visitedNodesText = visitedNodesText
        self.__nodesToBeVisitedText = nodesToBeVisitedText
        self.__nodeReferences = nodeReferences
        self.__edgeReferences = edgeReferences
        self.__distancesTable = distancesTable
        self.__tableData: list = tableData
        self.__axs = axs
        self.__fig = fig 
        self.__callCounter = 10

    def UpdateDistancesTableUI(self, distances):
        newRow = [distance if distance != float('inf') else '∞' for distance in distances.copy()]
        self.__tableData.append(newRow)
        if self.__distancesTable:
            self.__distancesTable.remove()
    
        self.__distancesTable = self.__axs[1].table(
        cellText=self.__tableData,
        colLabels=[nodeLabels[i] for i in range(len(distances))],
        loc='center',
        cellLoc='center',
        bbox = [0,0.1,1,0.4]
        )
        # self.__distancesTable.auto_set_font_size(False)
        # self.__distancesTable.set_fontsize(14)
        for cell in self.__distancesTable.get_celld().values():
            #cell.PAD = 1
            pass
        
        self.__callCounter += 0.1
        self.__fig.canvas.draw()
        #self.__distancesTable.plt.remove()

    def HighlightEdgesOfNode(self, currentIndex) -> None:
        for edge in self.__edgeReferences[currentIndex]:
            edge.set(color='red', linewidth=2)
        self.__fig.canvas.draw()

    def DehighlightEdgesOfNode(self, currentIndex) -> None:
        for edge in self.__edgeReferences[currentIndex]:
            edge.set(color='grey')
        self.__fig.canvas.draw()

    def DehighlightAllNodes(self) -> None:
        for node in self.__nodeReferences.values():
            node.set(color = 'skyblue')
        self.__fig.canvas.draw()

    def UpdateVisitedNodesText(self, visitedNodes: list[Node]) -> None:
        visitedNodesString = ','.join(node.GetLabel() for node in visitedNodes)
        self.__visitedNodesText.set_text(f'S{{{visitedNodesString}}}')

    def UpdateNodesToBeVisitedText(self, nodesToBeVisited: PriorityQueue) -> None:
        notesToBeVisitedString = ','.join(node.GetLabel() for node in nodesToBeVisited.GetQueue())
        self.__nodesToBeVisitedText.set_text(f'P[{notesToBeVisitedString}]')
    
    def UpdateDataStructuresPAndS(self, visitedNodes: list[Node], nodesToBeVisited: PriorityQueue):
        self.UpdateNodesToBeVisitedText(nodesToBeVisited)
        self.UpdateVisitedNodesText(visitedNodes)
        self.__fig.canvas.draw()
    
    def SetNodeColour(self, id, colour):
        self.__nodeReferences[id].set(color = colour)
        self.__fig.canvas.draw()

    def GetFigure(self):
        return self.__fig
    
    def AnimationSleep(self):
        window = self.__fig.canvas.get_tk_widget().master  # Get the Tkinter window
        window.after(10000, self.resume_animation)
    
    def resume_animation():  
        pass


def GetAngles(numNodes: int) -> list[float]:
    #tau is 2pi
    #Make your own pi function
    step = math.tau / numNodes
    angles = [i * step for i in range(numNodes)]
    return angles


def CircularLayout(numNodes: int) -> dict[int, tuple[float,float]]:
    radius = 1
    angles = GetAngles(numNodes)
    coordinates = {}
    for i,angle in enumerate(angles):
        x_Coord = radius * cos(angle) 
        y_Coord = radius * sin(angle) 
        coordinates[i] = (x_Coord, y_Coord)
    return coordinates



def DisplayGraph(adjacencyMatrix: list[list[int]], axs) :
    numNodes: int = len(adjacencyMatrix)
    nodeReferecnce = {}
    edgeReferences = [[] for i in range(numNodes)]
    edgeLabels = []
    lablePositions = []
    #plt.figure(figsize=(8,8))
    coordinates = CircularLayout(numNodes)
    
    
    for i, (x, y) in coordinates.items():
        #How to alter properties of value
        #node  = plt.scatter(x, y, s=300, color='skyblue', zorder=3)
        node = axs.scatter(x, y, s=300, color='skyblue', zorder=3)
        nodeReferecnce[i] = node
        axs.text(x, y, nodeLabels[i], fontsize=12, ha='center', va='center')
        
    #Plotting the edges
    for i in range(numNodes):
        for j in range(i+1, numNodes):
            if adjacencyMatrix[i][j] !=0:  
                x_Coords = [coordinates[i][0], coordinates[j][0]]
                y_Coords = [coordinates[i][1], coordinates[j][1]]
                x_mid = (x_Coords[0] + x_Coords[1]) / 2
                y_mid = (y_Coords[0] + y_Coords[1]) / 2

                # b =plt.plot(x_Coords, y_Coords, color='grey')
                edge, = axs.plot(x_Coords, y_Coords, color='grey')
                edgeReferences[i].append(edge)
                edgeReferences[j].append(edge)
                if numNodes == 2:
                # For two nodes, place label exactly at the midpoint
                    label_x = x_mid
                    label_y = y_mid
                else:
                    offset_x = 0.05 if abs(x_Coords[0] - x_Coords[1]) > abs(y_Coords[0] - y_Coords[1]) else 0 
                    offset_y = 0 if abs(x_Coords[0] - x_Coords[1]) > abs(y_Coords[0] - y_Coords[1]) else 0.05
                    #Adding random jitter in addition to offset
                    label_x = x_mid + offset_x + random.uniform(-0.02, 0.02)
                    label_y = y_mid + offset_y + random.uniform(-0.02, 0.02)
                edgeLabels.append(axs.text(label_x, label_y, str([adjacencyMatrix[i][j]])[1:-1], fontsize=14, ha='center', va='center',))
    adjust_text(edgeLabels, ax=axs)
    
    #nodeReferecnce[2].set_color('red')
    # plt.axis('off')
    # plt.title('Dijkstras demeonstration')
    axs.set_title('Dijkstras Demonstration')
    axs.set_axis_off()
    return nodeReferecnce, edgeReferences


    
    

def DisplayDataStrucutures(axs, numNodes, sourceNodeIndex):
    columnLabels = [nodeLabels[i] for i in range(numNodes)]
    initialDistances = [float('inf')]* numNodes
    initialDistances[sourceNodeIndex] = 0
    axs.set_title('Data Structures')
    #axs[1].set_axis_off()
    visitedNodesText =axs.text(0.5, 0.8, 'S{ABCDEF}', fontsize=20, ha='center', va='center', wrap=True)
    nodesToOptimiseText = axs.text(0.5, 0.7, 'P[]', fontsize=20, ha='center', va='center', wrap=True)
    #Fix lol
    data = [[distance if distance != float('inf') else '∞' for distance in initialDistances]]
    distancesTable = axs.table(cellText=data,
                                  colLabels=columnLabels,
                                  loc='center',
                                  cellLoc='center',
                                  edges='closed',
                                  bbox = [0,0.1,1,0.4])
    distancesTable.auto_set_font_size(False)
    distancesTable.set_fontsize(14)
    #axs[1].set_axis_off()
    #distancesTable.auto_set_column_width(col=list(range(len(columnLabels))))
    
    return visitedNodesText, nodesToOptimiseText, distancesTable, data

def DisplayWindow(adjacencyMatrix: list[list[int]], sourceNodeIndex: int) -> None:
    


    numNodes: int = len(adjacencyMatrix)
    fig, axs = plt.subplots(1, 2, figsize=(12, 8), gridspec_kw={'width_ratios': [2, 1]})
    nodeReference, edgeReferences = DisplayGraph(adjacencyMatrix, axs[0])
    visitedNodesText, nodesToBeVisitedText, distancesTable, tableData = DisplayDataStrucutures(axs[1], numNodes, sourceNodeIndex)
    animationController = AnimationController(nodeReference, edgeReferences, visitedNodesText, nodesToBeVisitedText , distancesTable, tableData, axs, fig)

    window = tk.Tk()
    window.title("Dijkstra's demonstration")
    GraphFrame = tk.Frame(master=window)
    GraphFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)    
    canvas = FigureCanvasTkAgg(fig, master=GraphFrame,)
    canvasWidget = canvas.get_tk_widget()  # Get the Tkinter widget
    canvasWidget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    #window.mainloop()
    AnimateDijkstras( adjacencyMatrix, sourceNodeIndex,  distancesTable, animationController)
    window.mainloop()
    plt.tight_layout()
    #plt.show()
    


def AnimateDijkstras(adjacencyMatrix: list[list[int]], sourceNodeIndex: int,  distancesTable, animationController: AnimationController) -> None:
    #Do your own way in this function
    numNodes = len(adjacencyMatrix)
    window = animationController.GetFigure().canvas.get_tk_widget().master 




    distances = [float('inf')] * numNodes
    distances[sourceNodeIndex] = 0
    animationController.SetNodeColour(sourceNodeIndex, 'lightgreen')
    #visited = [False] * numNodes
    nodesToBeVisited: list[Node] = PriorityQueue()
    visitedNodes: list[Node]= []
    for i in range(numNodes):
        priority = distances[i]
        nodesToBeVisited.Enqueue(Node(nodeLabels[i], priority, i))
        
    #nodesToBeVisited.queue[sourceNode].SetPriority(0)
    #sourceNode = nodesToBeVisited.ReturnNodeAtIndex(sourceNodeIndex)
    #nodesToBeVisited.ChangePriority(sourceNode, 0)
    #nodesToBeVisited.OutputQueue()

    
    
    #nodesToBeVisited.ChangePriority(, 0)
    #nodesToBeVisited.OutputQueue()
    def updateAnimation():
        
        if nodesToBeVisited.IsEmpty():
            animationController.DehighlightAllNodes()
            print('Animaton Complete!')
            for i in range(numNodes):
                print(f"Shortest distance to {nodeLabels[i]} is {distances[i]}")
    
    
            for i in range(numNodes): 
                visitedNodes[i].OutputNode()
            return 
        currentNode: Node = nodesToBeVisited.Peek()
        nodesToBeVisited.Dequeue()
        
        currentIndex = currentNode.GetID()
        animationController.HighlightEdgesOfNode(currentIndex)
        animationController.UpdateDataStructuresPAndS(visitedNodes, nodesToBeVisited)
        animationController.SetNodeColour(currentIndex, 'yellow') if currentIndex != sourceNodeIndex else None
        #plt.pause(3)
        #animationController.AnimationSleep()
        
        
        visitedNodes.append(currentNode)
        print(visitedNodes)
        animationController.SetNodeColour(currentIndex, 'darksalmon') if currentIndex != sourceNodeIndex else None
        
        

        for neighbourIndex in range(numNodes):
            weight = adjacencyMatrix[currentIndex][neighbourIndex]
            
            #neighbourNode of type None when neighbourNode has already been visited
            neighbourNode: Node = nodesToBeVisited.GetNodeByID(neighbourIndex)
            if weight > 0 and neighbourNode != None:
                newDistance = distances[currentIndex] + weight
                

                if newDistance < distances[neighbourIndex]:
                    distances[neighbourIndex] = newDistance
                    nodesToBeVisited.ChangePriority(neighbourNode,newDistance)
                    
        animationController.UpdateDistancesTableUI(distances)
        
        
        
        
        animationController.UpdateDataStructuresPAndS(visitedNodes, nodesToBeVisited)
        def dehighlightCurrentNodeAndEdges():
            animationController.DehighlightEdgesOfNode(currentIndex)
            animationController.DehighlightAllNodes()
            window.after(1000, updateAnimation)  # Call the next animation step after dehighlighting

    # Delay dehighlighting to let highlighting be visible
        window.after(750, dehighlightCurrentNodeAndEdges)
    updateAnimation()
    #print(distances)
    

    #plt.show()


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
    b = g.GenerateMatrix(5,50)
    #DisplayWindow(test)
    DisplayWindow(test, 0)