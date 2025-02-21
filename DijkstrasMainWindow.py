import matplotlib.pyplot as plt
import math
from Utilities import sin, cos
from DataStructures import Node, PriorityQueue
from Forms import SourceNodeInputForm, GraphGeneratorForm
import GeneratingAdjacencyMatrix as g
import random
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

NODELABELS = {i: chr(65+i) for i in range(11)} #Dictionary to access a node label from ID e.g 0 -> A, 1 -> B
BARHEIGHT = 40 # Height in pixels of the UI top and bar elements

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
        for cell in self.__distancesTable.get_celld().values():
            cell.PAD = 1
        
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

class GraphRenderer():
    def __init__(self, adjacencyMatrix, graphAxis):
        self.__adjacencyMatrix = adjacencyMatrix
        self.__numNodes = len(self.__adjacencyMatrix)
        self.__graphAxis = graphAxis
        self.TITLE_FONT_SIZE = 20
    
    def GetAngles(self) -> list[float]:
        #tau is 2pi
        #Make your own pi function
        step = math.tau / self.__numNodes
        angles = [i * step for i in range(self.__numNodes)]
        return angles


    def CircularLayout(self) -> dict[int, tuple[float,float]]:
        radius = 1
        angles = self.GetAngles()
        coordinates = {}
        for i,angle in enumerate(angles):
            x_Coord = radius * cos(angle) 
            y_Coord = radius * sin(angle) 
            coordinates[i] = (x_Coord, y_Coord)
        return coordinates


    def DisplayGraph(self) :
        nodeReferences = {}
        edgeReferences = [[] for i in range(self.__numNodes)]
        edgeLabels = []
        labelPositions = []
        #plt.figure(figsize=(8,8))
        coordinates = self.CircularLayout()
        
        
        for i, (x, y) in coordinates.items():
            node = self.__graphAxis.scatter(x, y, s=300, color='skyblue', zorder=3)
            nodeReferences[i] = node
            self.__graphAxis.text(x, y, NODELABELS[i], fontsize=12, ha='center', va='center')
            
        #Plotting the edges
        for i in range(self.__numNodes):
            for j in range(i+1, self.__numNodes):
                if self.__adjacencyMatrix[i][j] !=0:  
                    x_Coords = [coordinates[i][0], coordinates[j][0]]
                    y_Coords = [coordinates[i][1], coordinates[j][1]]
                    #MR R FIX? 45 + 55 /100
                    x_mid = (x_Coords[0] + x_Coords[1])/2
                    y_mid = (y_Coords[0] + y_Coords[1])/2

                    edge, = self.__graphAxis.plot(x_Coords, y_Coords, color='grey')
                    edgeReferences[i].append(edge)
                    edgeReferences[j].append(edge)
                    if self.__numNodes == 2:
                    # For two nodes, place label exactly at the midpoint
                        label_x = x_mid
                        label_y = y_mid
                    else:
                        #Initially placing edge weight label in the middle of the edge
                        label_x, label_y = self.ResolveEdgeLabelOverlap(x_mid, y_mid, labelPositions)
                        labelPositions.append((label_x, label_y))
                    edgeLabels.append(self.__graphAxis.text(label_x, label_y, str([self.__adjacencyMatrix[i][j]])[1:-1], fontsize=14, ha='center', va='center',))
        self.__graphAxis.set_title('Dijkstras Demonstration', fontsize= self.TITLE_FONT_SIZE)
        self.__graphAxis.set_axis_off()
        #plt.show()
        return nodeReferences, edgeReferences
    
    def ResolveEdgeLabelOverlap(self, x: float, y: float, label_positions: list[tuple[float, float]], minimumDistance=0.1) -> tuple[float, float]:
        for existing_x, existing_y in label_positions: #Loop through each edge label checking for overlap.
            distance = math.sqrt((x - existing_x) ** 2 + (y - existing_y) ** 2) # Calculating distance between new label and existing labels 
            if distance < minimumDistance: # If new label too close to exisiting label adjust the position
                # Adjust the position to resolve the overlap
                x += random.uniform(-minimumDistance, minimumDistance)
                y += random.uniform(-minimumDistance, minimumDistance)
                # Check again with updated position (recursively)
                return self.ResolveEdgeLabelOverlap(x, y, label_positions)
        return x, y

class DijkstrasDemonstrationWindow():
    def __init__(self):
        self.TITLE_FONT_SIZE = 20
        self.__adjMatrix = [[0,4,3,7,0,0,0],
                [4,0,0,1,0,4,0],
                [3,0,0,3,5,0,0],
                [7,1,3,0,2,2,7],
                [0,0,5,2,0,0,2],
                [0,4,0,2,0,0,4],
                [0,0,0,7,2,4,0]]
        self.__sourceNode = 0
        #Unpacking the fig and axis object from subplots then storing it in a single variable fig and axis
        figAndAxis = fig, axs = plt.subplots(1, 2, figsize=(12, 8), gridspec_kw={'width_ratios': [2, 1]})
        self.__fig = figAndAxis[0]
        self.__axs = figAndAxis[1]
        
        #visitedNodesText, nodesToBeVisitedText, distancesTable, tableData = self.DisplayDataStrucutures(axs[1], numNodes, sourceNodeIndex)
        #nodeReference, edgeReferences = self.DisplayGraph(self.__demoGraph, axs[0])
        self.DisplayWindow(self.__adjMatrix)
    
    def DisplayDataStrucutures(self, axs, numNodes):
        columnLabels = [NODELABELS[i] for i in range(numNodes)]
        # initialDistances = [float('inf')]* numNodes
        # initialDistances[sourceNodeIndex] = 0
        blankSpaceRow = [[None] * len(columnLabels)]
        axs.set_title('Data Structures', fontsize=self.TITLE_FONT_SIZE)
        #axs[1].set_axis_off()
        visitedNodesText =axs.text(0.5, 0.8, 'S{}', fontsize=20, ha='center', va='center', wrap=True)
        nodesToOptimiseText = axs.text(0.5, 0.7, 'P[]', fontsize=20, ha='center', va='center', wrap=True)
        distancesTable = axs.table(cellText=blankSpaceRow,
                                    colLabels=columnLabels,
                                    loc='center',
                                    cellLoc='center',
                                    edges='closed',
                                    bbox = [0,0.1,1,0.4])
        distancesTable.auto_set_font_size(False)
        distancesTable.set_fontsize(14)
        axs.set_axis_off()
        #distancesTable.auto_set_column_width(col=list(range(len(columnLabels))))
   
        return visitedNodesText, nodesToOptimiseText, distancesTable, blankSpaceRow
    
    
    def DisplayWindow(self, adjacencyMatrix: list[list[int]]) -> None:
        numNodes: int = len(adjacencyMatrix)
        fig, axs = plt.subplots(1, 2, figsize=(12, 8), gridspec_kw={'width_ratios': [2, 1]})
        #Getting references to UI elements
        graphRenderer = GraphRenderer(adjacencyMatrix, graphAxis=axs[0])
        nodeReference, edgeReferences = graphRenderer.DisplayGraph()

        visitedNodesText, nodesToBeVisitedText, distancesTable, tableData = self.DisplayDataStrucutures(axs[1], numNodes)
        
        animator = Animator(nodeReference, edgeReferences, visitedNodesText, nodesToBeVisitedText , distancesTable, tableData, axs, fig)

        window = tk.Tk()
        #For laptop turn code below off
        #window.geometry("1800x1000")
        
        window.title("Dijkstra's demonstration")
        
        topBar = TopUIBar(window, self)
        
        bottomBar = BottomUIBar(window, animator, self)
        GraphFrame = tk.Frame(master=window, width=700, height=250)
        GraphFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)   

         
        #GraphFrame.pack_propagate(False)
        canvas = FigureCanvasTkAgg(fig, master=GraphFrame)
        canvasWidget = canvas.get_tk_widget()  # Get the Tkinter widget
        canvasWidget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        #tk.Button(window, text="Update", height=10).pack()
        
        window.mainloop()
        
        plt.tight_layout()

    def GetAxis(self):
        return self.__axs

    def GetMatrix(self):
        return self.__adjMatrix
    
    def GetMatrixLength(self) -> int:
        return len(self.__adjMatrix)
    
    def GetDemoMatrix(self):
        return [[0,4,3,7,0,0,0],
                [4,0,0,1,0,4,0],
                [3,0,0,3,5,0,0],
                [7,1,3,0,2,2,7],
                [0,0,5,2,0,0,2],
                [0,4,0,2,0,0,4],
                [0,0,0,7,2,4,0]]
    
    def SetMatrix(self, matrix):
        self.__adjMatrix = matrix
    
    def GetSourceNode(self):
        return self.__sourceNode
    
    def SetSourceNode(self, sourceNode):
        self.__sourceNode = sourceNode

    def StartAnimation(self,adjacencyMatrix, sourceNodeIndex,   animator):
        AnimateDijkstras( adjacencyMatrix, sourceNodeIndex,   animator)


class TopUIBar():
    def __init__(self, window, windowObject):
        self.__window = window
        self.__windowObject: DijkstrasDemonstrationWindow = windowObject
        self.__isGraphGeneratorFormRunning: bool = False
        buttonHeight = 2
        butttonWidth = 8

        self.__topBarFrame = tk.Frame(self.__window, height=BARHEIGHT)
        self.__topBarFrame.pack(side="top", fill=tk.X)

        self.__quitButton = tk.Button(self.__topBarFrame, text='Quit', height=buttonHeight, width=butttonWidth, command=self.QuitButtonClick )
        self.__quitButton.pack(side=tk.RIGHT, padx=10)
        

        self.__graphGeneratorButton = tk.Button(self.__topBarFrame, text="Generate New Graph", height=buttonHeight, command=self.GenerateNewGraphButtonClick)
        self.__graphGeneratorButton.pack(side=tk.RIGHT)

        
        
        #self.__topBarFrame.pack_propagate(False)
    
    def GenerateNewGraphButtonClick(self):
        if self.__isGraphGeneratorFormRunning:
            tk.messagebox.showwarning("Warning", "The form is already open.")
            return
        self.__isGraphGeneratorFormRunning = True
        graphGeneratorFormObject = GraphGeneratorForm()
        form = graphGeneratorFormObject.GetForm()
        #Ensuring when the window is closed via the window manager it is handled in the correct way
        form.protocol("WM_DELETE_WINDOW", lambda: self.OnGraphGeneratorFormClose(form))
        graphGeneratorFormObject.Run()
        if not graphGeneratorFormObject.IsDemoModeSelected():
            numNodes = graphGeneratorFormObject.GetNumberOfNodes()
            density = graphGeneratorFormObject.pValue
            matrix = g.GenerateMatrix(numNodes,density)
            self.__windowObject.SetMatrix(matrix) # Might be redundant
            self.__window.destroy()
            self.__windowObject.DisplayWindow(matrix)
        else:
            matrix = self.__windowObject.GetDemoMatrix()
            self.__windowObject.SetMatrix(matrix) # Might be redundant
            self.__window.destroy()
            self.__windowObject.DisplayWindow(matrix)
        

    def OnGraphGeneratorFormClose(self, form):
        self.__isGraphGeneratorFormRunning = False
        form.destroy()

        
    def QuitButtonClick(self):
        self.__window.destroy()
        
class BottomUIBar():
    def __init__(self, window, animator: Animator, windowObject):
        self.__window = window
        self.__windowObject: DijkstrasDemonstrationWindow = windowObject
        self.__isSourceNodeInputFormRunning: bool = False
        buttonHeight = 2
        buttonWidth = 8

        self.__animationController: AnimationController = animator.GetAnimationController()
        self.__animator = animator

        self.__bottomBarFrame = tk.Frame(window, height=BARHEIGHT)
        self.__bottomBarFrame.pack(side="bottom",  fill=tk.X)
        self.__bottomBarFrame.pack_propagate(False)  
        
        #Left Spacer widget
        tk.Frame(self.__bottomBarFrame).pack(side=tk.LEFT, expand=True)

        self.__slowDownButton = tk.Button(self.__bottomBarFrame, text="Slow Down", height=buttonHeight, width=buttonWidth, command= self.__animationController.DecreaseAnimationSpeed, padx=10)
        self.__slowDownButton.pack(side=tk.LEFT,  padx=10)

        self.__pausePlayButton = tk.Button(self.__bottomBarFrame, text="Play", height=buttonHeight, width=buttonWidth, command= self.EnablePausePlayFunctionality, padx=10)
        self.__pausePlayButton.pack(side=tk.LEFT, padx=10)
        #self.__pauseButton.place(relx = 0.5, rely = 0.5, anchor = 'center')

        self.__speedUpButton = tk.Button(self.__bottomBarFrame, text="Speed Up", height=buttonHeight, width=buttonWidth, command= self.__animationController.IncreaseAnimationSpeed, padx=10)
        self.__speedUpButton.pack(side=tk.LEFT,  padx=10)
        #self.__fastForwardButton.place(relx = 0.7, rely = 0.7, anchor = 'center')

        self.__restartButton = tk.Button(self.__bottomBarFrame, text="Restart", height=buttonHeight, width=buttonWidth, command= self.RestartAnimationButtonClick, padx=10)
        self.__restartButton.pack(side=tk.LEFT,  padx=10)

        self.__jumpToEndButton = tk.Button(self.__bottomBarFrame, text="Jump To End", height=buttonHeight, width=buttonWidth, command= self.__animationController.JumpToEndOfAnimation, padx=10)
        self.__jumpToEndButton.pack(side=tk.LEFT,  padx=10)

        #Right Spacer widget 
        tk.Frame(self.__bottomBarFrame).pack(side=tk.LEFT, fill=tk.X, expand=True)


       

    def RestartAnimationButtonClick(self):
        self.__window.destroy()
        self.__windowObject.DisplayWindow(self.__windowObject.GetMatrix()) # Restart Window with the same matrix
       

    
    
    def EnablePausePlayFunctionality(self):
        if not self.__animator.GetHasAnimationStarted():
            #If animation not initiallised allow user to enter source node and run animation
            if self.__isSourceNodeInputFormRunning:
                return
            sourceNode = self.GetSourceNodeIndexFromForm()
            self.__animator.SetAnimationStarted()
            self.__windowObject.SetSourceNode(sourceNode)
            self.__animationController.SetAnimationSpeed(1000)
            AnimateDijkstras(self.__windowObject.GetMatrix(), self.__windowObject.GetSourceNode(), self.__animator)
            
        self.__animationController.PauseAnimation()
        #Conditionally display Resume or Pause based on state of aniamtion
        pausePlayButtonText = "Resume" if self.__animationController.IsPaused() else "Pause"
        self.__pausePlayButton.config(text=pausePlayButtonText)

    def GetSourceNodeIndexFromForm(self) -> int:
        self.__isSourceNodeInputFormRunning = True
        sourceNodeInputFormObject = SourceNodeInputForm(self.__windowObject.GetMatrixLength())
        form = sourceNodeInputFormObject.GetForm()

        #Ensuring when the window is closed via the cross in the top right corner it is handled in the correct way
        form.protocol("WM_DELETE_WINDOW", lambda: self.OnSourceNodeInputFormClose(form))
        sourceNodeInputFormObject.Run()
        sourceNode = sourceNodeInputFormObject.GetSourceNodeID()
        return sourceNode
    
    def OnSourceNodeInputFormClose(self, form):
        self.__isSourceNodeInputFormRunning = False
        form.destroy()

    


def AnimateDijkstras(adjacencyMatrix: list[list[int]], sourceNodeIndex: int,  animator: Animator) -> None:
    numNodes = len(adjacencyMatrix)
    window = animator.GetFigure().canvas.get_tk_widget().master #Accessing the window where the animation is being displayed
    
    distances = [float('inf')] * numNodes #Intialise the distance from every node to the source node as infinity.
    distances[sourceNodeIndex] = 0 # Distance to source node set to zero
    animator.UpdateDistancesTableUI(distances)
    animator.SetNodeColour(sourceNodeIndex, 'lightgreen')

    nodesToBeVisited: list[Node] = PriorityQueue()
    visitedNodes: list[Node]= []
    #Initiallisng the priority queue of nodes to be visited
    for i in range(numNodes):
        priority = distances[i]
        nodesToBeVisited.Enqueue(Node(NODELABELS[i], priority, id=i))
    
    #Animaiton function that is called upon every frame.
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
        animator.SetNodeColour(currentIndex, 'yellow') if currentIndex != sourceNodeIndex else None
        
        visitedNodes.append(currentNode)
        
        animator.SetNodeColour(currentIndex, 'darksalmon') if currentIndex != sourceNodeIndex else None
        

        for neighbourIndex in range(numNodes):
            weight = adjacencyMatrix[currentIndex][neighbourIndex]
            
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
            '''Dehighlight node after being optimised by dijskstras'''
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
    #DisplayWindow(test, 0)
    window = DijkstrasDemonstrationWindow()