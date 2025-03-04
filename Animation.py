from DataStructures import PriorityQueue, Node
from Utilities import NODELABELS
import osmnx as ox
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from tkinter import messagebox
from Utilities import ConvertKilometresToMiles
from Algorithms import Dijkstra, AStar

class AnimationController():
    def __init__(self):
        self.__frameDelay: int = 1000 #Time between frame in miliseconds.
        self.__isPaused: bool = True
    
    
    def PauseAnimation(self):
        self.__isPaused = not self.__isPaused
        if self.__isPaused:
            print("Animation Paused")
        else:
            print("Animation Resumed")
    
    def IncreaseAnimationSpeed(self):
        #Increment Animation speed to a max value
        if self.__frameDelay > 100:
            self.__frameDelay -= 100 #Decreasing frame delay to increase animation speed
        else:
            print('Maximum PlayBack Speed has been reached')
        print(self.__frameDelay)

    def DecreaseAnimationSpeed(self):
        #Decrease animation speed to a minimum value
        if self.__frameDelay < 2500:
            self.__frameDelay +=500
        else:
            print('Minimum Playback speed has been reached')
        print(self.__frameDelay)

    def JumpToEndOfAnimation(self):
        self.SetAnimationSpeed(0) #Setting the frame delay to zero to complete the animation stratight away

    def IsPaused(self):
        return self.__isPaused

    def SetAnimationSpeed(self, num: int):
        self.__frameDelay = num  
    
    def GetFrameDelay(self):
        return self.__frameDelay

class Animator():
    def __init__(self, nodeReferences, edgeReferences, visitedNodesText, nodesToBeVisitedText, distancesTable, tableData, axs, fig):
        self.__visitedNodesText = visitedNodesText
        self.__nodesToBeVisitedText = nodesToBeVisitedText
        self.__nodeReferences = nodeReferences
        self.__edgeReferences = edgeReferences
        self.__distancesTable = distancesTable
        self.__tableData: list = tableData
        self.__axs = axs
        self.__fig = fig 
        self.__animationController = AnimationController()
        self.__isRunning: bool = False
        self.__animationStarted: bool = False
        self.__removeBlankSpaceTrueFlag: bool = True

    def UpdateDistancesTableUI(self, distances):
        #Removing placeholder blank space row in distances table
        if self.__removeBlankSpaceTrueFlag:
            self.__tableData.pop(0)
            self.__removeBlankSpaceTrueFlag = False
        
        #Adding a new row to the table 
        newRow = [distance if distance != float('inf') else '∞' for distance in distances.copy()]
        self.__tableData.append(newRow)
        #Clearing old table
        if self.__distancesTable:
            self.__distancesTable.remove()
        
      
        #Redrawing table with new data
        self.__distancesTable = self.__axs[1].table(
        cellText=self.__tableData,
        colLabels=[NODELABELS[i] for i in range(len(distances))],
        loc='center',
        cellLoc='center',
        bbox = [0,0.1,1,0.4]
        )
        self.__distancesTable.auto_set_font_size(False)
        self.__distancesTable.set_fontsize(18) # **** #
        for cell in self.__distancesTable.get_celld().values(): #Get each cell from distances table
            cell.PAD = 4
        
        self.__fig.canvas.draw()

    
    def HighlightEdgesOfNode(self, nodeID) -> None:
        '''Highlights all the edges connected to the node passed as the argument as red.'''
        for edge in self.__edgeReferences[nodeID]:
            edge.set(color='red', linewidth=2)
        self.__fig.canvas.draw()

    def DehighlightEdgesOfNode(self, nodeID) -> None:
        '''Dehighlights all the edges connected to the node passed as the argument by highlighting it grey.'''
        for edge in self.__edgeReferences[nodeID]:
            edge.set(color='grey')
        self.__fig.canvas.draw()

    def DehighlightAllNodes(self) -> None:
        '''Sets all nodes in the graph to skyblue'''
        for node in self.__nodeReferences.values():
            node.set(color = 'skyblue')
        self.__fig.canvas.draw()
    
    #Updater UI methods
    def __UpdateVisitedNodesText(self, visitedNodes: list[Node]) -> None:
        '''Change the VisitedNodes text to the new visitedNodes passed as an argument'''
        visitedNodesString = ','.join(node.GetLabel() for node in visitedNodes)
        self.__visitedNodesText.set_text(f'S{{{visitedNodesString}}}')

    def __UpdateNodesToBeVisitedText(self, nodesToBeVisited: PriorityQueue) -> None:
        '''Change the nodesToBeVisited text to the new nodesToBeVisited passed as an argument'''
        notesToBeVisitedString = ','.join(node.GetLabel() for node in nodesToBeVisited.GetQueue())
        self.__nodesToBeVisitedText.set_text(f'P[{notesToBeVisitedString}]')
    
    def UpdateDataStructuresPAndS(self, visitedNodes: list[Node], nodesToBeVisited: PriorityQueue):
        self.__UpdateNodesToBeVisitedText(nodesToBeVisited)
        self.__UpdateVisitedNodesText(visitedNodes)
        self.__fig.canvas.draw() #Redraw canvaas with updates
    
    def SetNodeColour(self, id, colour):
        '''Sets node at passed id to colour passed as argument'''
        self.__nodeReferences[id].set(color = colour)
        #Redraw figure with update
        self.__fig.canvas.draw()


    def GetFigure(self):
        return self.__fig
    
    def GetFrameDelay(self):
        return self.__animationController.GetFrameDelay()
    
    def IsPaused(self):
        return self.__animationController.IsPaused()  
    
    def GetAnimationController(self) -> AnimationController:
        return self.__animationController
    
    def SetRunningState(self, state: bool):
        self.__isRunning = state

    def IsRunning(self):
        return self.__isRunning
    
    def GetHasAnimationStarted(self) -> bool:
        return self.__animationStarted
    
    def SetAnimationStarted(self):
        self.__animationStarted = True

def AnimateDijkstras(adjacencyMatrix: list[list[int]], sourceNodeIndex: int,  animator: Animator) -> None:
    numNodes = len(adjacencyMatrix)
    window = animator.GetFigure().canvas.get_tk_widget().master #Accessing the window where the animation is being displayed
    
    distances = [float('inf')] * numNodes #Initialise the distance from every node to the source node as infinity.
    distances[sourceNodeIndex] = 0 # Distance to source node set to zero
    animator.UpdateDistancesTableUI(distances)
    animator.SetNodeColour(sourceNodeIndex, 'lightgreen')

    nodesToBeVisited: list[Node] = PriorityQueue()
    visitedNodes: list[Node]= []
    #Initiallisng the priority queue of nodes to be visited
    for i in range(numNodes):
        priority = distances[i]
        nodesToBeVisited.Enqueue(Node(NODELABELS[i], priority, id=i))
    
    #Animation function that is called upon every frame.
    def updateAnimation():
        if animator.IsPaused(): #Check if paused
            window.after(100, updateAnimation) #Check again if not paused 
            return 
        
        if not animator.IsRunning():  # Check if already running
            animator.SetRunningState(True)  
        else:
            return
        
        #Condition to show if animation is complete
        if nodesToBeVisited.IsEmpty():
            animator.DehighlightAllNodes()
            print('Animaton Complete!')
            for i in range(numNodes):
                print(f"Shortest distance to {NODELABELS[i]} is {distances[i]}")
    
            animator.SetRunningState(False)
            return 
        

        currentNode: Node = nodesToBeVisited.Peek()
        nodesToBeVisited.Dequeue()
        
        currentIndex = currentNode.GetID()
        
        animator.HighlightEdgesOfNode(currentIndex)
        animator.UpdateDataStructuresPAndS(visitedNodes, nodesToBeVisited)
        animator.SetNodeColour(currentIndex, 'yellow') if currentIndex != sourceNodeIndex else None #REmove?
        
        visitedNodes.append(currentNode)
        
        #Set node to 'dark salmon' if we have visited node and it is not the source node
        animator.SetNodeColour(currentIndex, 'darksalmon') if currentIndex != sourceNodeIndex else None
        

        for neighbourIndex in range(numNodes):
            weight = adjacencyMatrix[currentIndex][neighbourIndex] #Get edge weight from adjacency matrix.s
            
            #neighbourNode of type None when neighbourNode has already been visited
            neighbourNode: Node = nodesToBeVisited.GetNodeByID(neighbourIndex)
            if weight > 0 and neighbourNode != None:
                newDistance = distances[currentIndex] + weight
                

                if newDistance < distances[neighbourIndex]:
                    #Update distance with the new distance found
                    distances[neighbourIndex] = newDistance
                    nodesToBeVisited.ChangePriority(neighbourNode,newDistance)
                    
        animator.UpdateDistancesTableUI(distances)
        
        
        
        
        animator.UpdateDataStructuresPAndS(visitedNodes, nodesToBeVisited)
        def DehighlightCurrentNodeAndEdges():
            '''Dehighlight node after being optimised by dijkstras'''
            if animator.IsPaused():
                window.after(100, DehighlightCurrentNodeAndEdges)  # Retry after a small delay
                return
            animator.DehighlightEdgesOfNode(currentIndex)
            #animator.DehighlightAllNodes()
            animator.SetRunningState(False)
            window.after(animator.GetFrameDelay(), updateAnimation)  # Call the next animation step after dehighlighting

    # Delay dehighlighting to let highlighting be visible
        window.after(int(animator.GetFrameDelay() * 0.75), DehighlightCurrentNodeAndEdges)
    updateAnimation() #Call updateAnimation to run the next frame

#Map demonstration animator class
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
        
    def OnAnimationComplete(self):
        print('Animation Complete')
        self.endTime = time.time()
        timeTook = self.endTime-self.startTime
        units = 'Miles' if self.useMiles else 'Kilometres' #Conditionally show Miles or kilometres
        messagebox.showinfo(title='Length Of Path', 
                            message=f"The length of path found is {round(self.lengthOfPath,1)} {units} and was found in {round(timeTook, 2)}s") 