import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
from Utilities import sin, cos

class NodeAnimationController():
    def __init__(self):
        pass
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
    nodeReferecnce = {}
    numNodes: int = len(adjMatrix)
    #plt.figure(figsize=(8,8))
    coordinates = CircularLayout(numNodes)
    
    
    for i, (x, y) in coordinates.items():
        #How to alter properties of value
        #node  = plt.scatter(x, y, s=300, color='skyblue', zorder=3)
        axs[0].scatter(x, y, s=300, color='skyblue', zorder=3)
        #nodeReferecnce[i] = node
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
                axs[0].plot(x_Coords, y_Coords, color='grey')
                
                # plt.text(x_mid, y_mid-0.05, str([adjMatrix[i][j]])[1:-1], fontsize=14, ha='center', va='center',)
                axs[0].text(x_mid, y_mid-0.05, str([adjMatrix[i][j]])[1:-1], fontsize=14, ha='center', va='center',)
    
    #nodeReferecnce[2].set_color('red')
    # plt.axis('off')
    # plt.title('Dijkstras demeonstration')
    axs[0].set_title('Dijkstras Demonstration')
    axs[0].set_axis_off()
    
    
    

def DisplayDataStrucutures(axs):
    axs[1].set_title('Data Structures')
    #axs[1].set_axis_off()
    S =axs[1].text(0.5, 0.8, 'S{ABCDEF}', fontsize=20, ha='center', va='center', wrap=True)
    P = axs[1].text(0.5, 0.7, 'P[DFAFDAE]', fontsize=20, ha='center', va='center', wrap=True)
    #distances = axs[1].table(0.5,0.1)

def DisplayWindow(adjMatrix):
    fig, axs = plt.subplots(1, 2, figsize=(12, 8), gridspec_kw={'width_ratios': [2, 1]})
    DisplayGraph(adjMatrix, axs)
    DisplayDataStrucutures(axs)
    plt.tight_layout()
    plt.show()

def UpdateFrame(frame):
    pass

def UpdateGraph():
    pass
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
    b = [[], [], [], []]
    DisplayWindow(test)