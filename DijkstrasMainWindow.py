import matplotlib.pyplot as plt
import math
from Utilities import sin, cos
from DataStructures import Node, PriorityQueue
from Forms import SourceNodeInputForm, GraphGeneratorForm
import GeneratingAdjacencyMatrix as g
import random
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

NODELABELS = {i: chr(65+i) for i in range(11)}
BARHEIGHT = 40

class AnimationController():
    def __init__(self):
        self.__frameDelay: int = 1000
        self.__isPaused: bool = True
        
    
    def GetFrameDelay(self):
        return self.__frameDelay

    def IsPaused(self):
        return self.__isPaused
    
    def PauseAnimation(self):
        print(self.__isPaused)
        self.__isPaused = not self.__isPaused
        if self.__isPaused:
            print("Animation Paused")
        else:
            print("Animation Resumed")
    
    def IncreaseAnimationSpeed(self):
        #Increment Speed up to a max
        if self.__frameDelay > 100:
            self.__frameDelay -= 100
        else:
            print('Maximum PlayBack Speed has been reached')
        print(self.__frameDelay)

    def DecreaseAnimationSpeed(self):
        if self.__frameDelay < 2500:
            self.__frameDelay +=500
        else:
            print('Minimum Playback speed has been reached')
        print(self.__frameDelay)

    def JumpToEndOfAnimation(self):
        self.SetAnimationSpeed(0)

    def SetAnimationSpeed(self, num: int):
        self.__frameDelay = num  

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
        self.__numNodes = len(self.__nodeReferences)

    def UpdateDistancesTableUI(self, distances):
        #Removing placeholder blank space row in distances table
        if self.__removeBlankSpaceTrueFlag:
            self.__tableData.pop(0)
            self.__removeBlankSpaceTrueFlag = False
            
        newRow = [distance if distance != float('inf') else '∞' for distance in distances.copy()]
        self.__tableData.append(newRow)
        if self.__distancesTable:
            self.__distancesTable.remove()
        
      
    
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
            #pass
        
        self.__fig.canvas.draw()
        #self.__distancesTable.plt.remove()

    def ClearTable(self):
        print('clear')
        # columnLabels = [NODELABELS[i] for i in range(self.__numNodes)]
        # blankSpaceRow = [[None] * len(columnLabels)]
        # if self.__distancesTable:
        #     self.__distancesTable.remove()
        # distancesTable = self.__axs[1].table(cellText=blankSpaceRow,
        #                            colLabels=columnLabels,
        #                             loc='center',
        #                             cellLoc='center',
        #                             edges='closed',
        #                             bbox = [0,0.1,1,0.4])
        # distancesTable.auto_set_font_size(False)
        # distancesTable.set_fontsize(14)

        self.__distancesTable.remove()
        columnLabels = [NODELABELS[i] for i in range(self.__numNodes)]
        blankSpaceRow = [[None] * len(columnLabels)]
        self.__distancesTable = self.__axs[1].table(cellText=blankSpaceRow,
                                    colLabels=columnLabels,
                                    loc='center',
                                    cellLoc='center',
                                    edges='closed',
                                    bbox = [0,0.1,1,0.4])
        self.__distancesTable.auto_set_font_size(False)
        self.__distancesTable.set_fontsize(14)
        #self.__axs[1].set_axis_off()
        

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

    # def RestartAnimation(self, windowObject):
    #     windowObject: Window = windowObject
    #     self.__restartFlag = True
    #     m = windowObject.GetMatrix()
    #     AnimateDijkstras(m, windowObject.GetSourceNode(), self)


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

class Window():
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
        self.DisplayWindow(self.__adjMatrix, self.__sourceNode)
    
    def DisplayDataStrucutures(self, axs, numNodes):
        columnLabels = [NODELABELS[i] for i in range(numNodes)]
        # initialDistances = [float('inf')]* numNodes
        # initialDistances[sourceNodeIndex] = 0
        blankSpaceRow = [[None] * len(columnLabels)]
        axs.set_title('Data Structures', fontsize=self.TITLE_FONT_SIZE)
        #axs[1].set_axis_off()
        visitedNodesText =axs.text(0.5, 0.8, 'S{}', fontsize=20, ha='center', va='center', wrap=True)
        nodesToOptimiseText = axs.text(0.5, 0.7, 'P[]', fontsize=20, ha='center', va='center', wrap=True)
        #Fix This part
        #data = [[distance if distance != float('inf') else '∞' for distance in initialDistances]]
        #data = [['∞' for distance in initialDistances]]
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
    def GetAngles(self, numNodes: int) -> list[float]:
        #tau is 2pi
        #Make your own pi function
        step = math.tau / numNodes
        angles = [i * step for i in range(numNodes)]
        return angles


    def CircularLayout(self, numNodes: int) -> dict[int, tuple[float,float]]:
        radius = 1
        angles = self.GetAngles(numNodes)
        coordinates = {}
        for i,angle in enumerate(angles):
            x_Coord = radius * cos(angle) 
            y_Coord = radius * sin(angle) 
            coordinates[i] = (x_Coord, y_Coord)
        return coordinates


    def DisplayGraph(self, adjacencyMatrix: list[list[int]], axs) :
        numNodes: int = len(adjacencyMatrix)
        nodeReferences = {}
        edgeReferences = [[] for i in range(numNodes)]
        edgeLabels = []
        labelPositions = []
        #plt.figure(figsize=(8,8))
        coordinates = self.CircularLayout(numNodes)
        
        
        for i, (x, y) in coordinates.items():
            #How to alter properties of value
            #node  = plt.scatter(x, y, s=300, color='skyblue', zorder=3)
            node = axs.scatter(x, y, s=300, color='skyblue', zorder=3)
            nodeReferences[i] = node
            axs.text(x, y, NODELABELS[i], fontsize=12, ha='center', va='center')
            
        #Plotting the edges
        for i in range(numNodes):
            for j in range(i+1, numNodes):
                if adjacencyMatrix[i][j] !=0:  
                    x_Coords = [coordinates[i][0], coordinates[j][0]]
                    y_Coords = [coordinates[i][1], coordinates[j][1]]
                    #MR R FIX? 45 + 55 /100
                    x_mid = (x_Coords[0] + x_Coords[1])/2
                    y_mid = (y_Coords[0] + y_Coords[1])/2

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
                        #Initially placing edge weight label in the middle of the edge
                        label_x, label_y = self.ResolveEdgeLabelOverlap(x_mid, y_mid, labelPositions)
                        labelPositions.append((label_x, label_y))
                    edgeLabels.append(axs.text(label_x, label_y, str([adjacencyMatrix[i][j]])[1:-1], fontsize=14, ha='center', va='center',))
        axs.set_title('Dijkstras Demonstration', fontsize= self.TITLE_FONT_SIZE)
        axs.set_axis_off()
        #plt.show()
        return nodeReferences, edgeReferences
    
    def ResolveEdgeLabelOverlap(self, x: float, y: float, label_positions: list[tuple[float, float]], min_distance=0.1) -> tuple[float, float]:
        for existing_x, existing_y in label_positions:
            distance = math.sqrt((x - existing_x) ** 2 + (y - existing_y) ** 2)
            if distance < min_distance:
                # Adjust the position to resolve the overlap
                x += random.uniform(-min_distance, min_distance)
                y += random.uniform(-min_distance, min_distance)
                # Check again with updated position (recursively)
                return self.ResolveEdgeLabelOverlap(x, y, label_positions, min_distance)
        return x, y
    
    def DisplayWindow(self, adjacencyMatrix: list[list[int]], sourceNodeIndex: int) -> None:
        numNodes: int = len(adjacencyMatrix)
        fig, axs = plt.subplots(1, 2, figsize=(12, 8), gridspec_kw={'width_ratios': [2, 1]})
        #Getting references to UI elements
        nodeReference, edgeReferences = self.DisplayGraph(adjacencyMatrix, axs[0])
        visitedNodesText, nodesToBeVisitedText, distancesTable, tableData = self.DisplayDataStrucutures(axs[1], numNodes)
        
        animator = Animator(nodeReference, edgeReferences, visitedNodesText, nodesToBeVisitedText , distancesTable, tableData, axs, fig)

        window = tk.Tk()
        #For laptop turn code below off
        #window.geometry("1800x1000")
        
        window.title("Dijkstra's demonstration")
        
        topBar = TopBar(window, self)
        
        bottomBar = BottomBar(window, animator, self)
        GraphFrame = tk.Frame(master=window, width=700, height=250)
        GraphFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)   

         
        #GraphFrame.pack_propagate(False)
        canvas = FigureCanvasTkAgg(fig, master=GraphFrame)
        canvasWidget = canvas.get_tk_widget()  # Get the Tkinter widget
        canvasWidget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        #tk.Button(window, text="Update", height=10).pack()
        
        
        
        #sourceNodeInputForm = SourceNodeInputForm(numNodes)
        # sourceNodeInputForm.Run()
        # sourceNodeIndex = sourceNodeInputForm.GetSourceNodeIndex()
        #self.StartAnimation(adjacencyMatrix, sourceNodeIndex,   animator)
        
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


class TopBar():
    def __init__(self, window, windowObject):
        self.__window = window
        self.__windowObject: Window = windowObject
        self.__isGraphGeneratorFormRunning: bool = False
        buttonHeight = 2
        butttonWidth = 8

        self.__topBarFrame = tk.Frame(self.__window, height=BARHEIGHT)
        self.__topBarFrame.pack(side="top", fill=tk.X)

        self.__quitButton = tk.Button(self.__topBarFrame, text='Quit', height=buttonHeight, width=butttonWidth, command=self.QuitButtonClick )
        self.__quitButton.pack(side=tk.RIGHT, padx=10)
        

        self.__graphGeneratorButton = tk.Button(self.__topBarFrame, text="Generate New Graph", height=buttonHeight, command=self.GenerateNewGraphClick)
        self.__graphGeneratorButton.pack(side=tk.RIGHT)

        
        
        #self.__topBarFrame.pack_propagate(False)
    
    def GenerateNewGraphClick(self):
        if self.__isGraphGeneratorFormRunning:
            tk.messagebox.showwarning("Warning", "The form is already open.")
            return
        self.__isGraphGeneratorFormRunning = True
        graphGeneratorFormObject = GraphGeneratorForm()
        form = graphGeneratorFormObject.GetForm()
        #Ensuring when the window is closed via the cross in the top right corner it is handled in the correct way
        form.protocol("WM_DELETE_WINDOW", lambda: self.OnGraphGeneratorFormClose(form))
        graphGeneratorFormObject.Run()
        if not graphGeneratorFormObject.IsDemoModeSelected():
            numNodes = graphGeneratorFormObject.GetNumberOfNodes()
            density = graphGeneratorFormObject.pValue
            matrix = g.GenerateMatrix(numNodes,density)
            self.__windowObject.SetMatrix(matrix) # Might be redundant
            self.__window.destroy()
            self.__windowObject.DisplayWindow(matrix,0)
        else:
            matrix = self.__windowObject.GetDemoMatrix()
            self.__windowObject.SetMatrix(matrix) # Might be redundant
            self.__window.destroy()
            self.__windowObject.DisplayWindow(matrix,0)
        

    def OnGraphGeneratorFormClose(self, form):
        self.__isGraphGeneratorFormRunning = False
        form.destroy()

        
    def QuitButtonClick(self):
        self.__window.destroy()
        
class BottomBar():
    def __init__(self, window, animator: Animator, windowObject):
        self.__window = window
        self.__windowObject: Window = windowObject
        self.__isSourceNodeInputFormRunning: bool = False
        buttonHeight = 2
        buttonWidth = 8

        self.__animationController: AnimationController = animator.GetAnimationController()
        self.__animator = animator

        self.__bottomBarFrame = tk.Frame(window, height=BARHEIGHT)
        self.__bottomBarFrame.pack(side="bottom",  fill=tk.X)
        self.__bottomBarFrame.pack_propagate(False)  
        
        #Left Spacer
        tk.Frame(self.__bottomBarFrame).pack(side=tk.LEFT, expand=True)

        self.__slowDownButton = tk.Button(self.__bottomBarFrame, text="Slow Down", height=buttonHeight, width=buttonWidth, command= self.__animationController.DecreaseAnimationSpeed, padx=10)
        self.__slowDownButton.pack(side=tk.LEFT,  padx=10)

        self.__pausePlayButton = tk.Button(self.__bottomBarFrame, text="Play", height=buttonHeight, width=buttonWidth, command= self.EnablePausePlayFunctionality, padx=10)
        self.__pausePlayButton.pack(side=tk.LEFT, padx=10)
        #self.__pauseButton.place(relx = 0.5, rely = 0.5, anchor = 'center')

        self.__speedUpButton = tk.Button(self.__bottomBarFrame, text="Speed Up", height=buttonHeight, width=buttonWidth, command= self.__animationController.IncreaseAnimationSpeed, padx=10)
        self.__speedUpButton.pack(side=tk.LEFT,  padx=10)
        #self.__fastForwardButton.place(relx = 0.7, rely = 0.7, anchor = 'center')

        self.__restartButton = tk.Button(self.__bottomBarFrame, text="Restart", height=buttonHeight, width=buttonWidth, command= self.RestartAnimation, padx=10)
        self.__restartButton.pack(side=tk.LEFT,  padx=10)

        self.__jumpToEndButton = tk.Button(self.__bottomBarFrame, text="Jump To End", height=buttonHeight, width=buttonWidth, command= self.__animationController.JumpToEndOfAnimation, padx=10)
        self.__jumpToEndButton.pack(side=tk.LEFT,  padx=10)

        #Right Spacer
        tk.Frame(self.__bottomBarFrame).pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.__lastClickTime = 0

       

    def RestartAnimation(self):
        self.__window.destroy()
        self.__windowObject.DisplayWindow(self.__windowObject.GetMatrix(),0)
        # self.__animator.ClearTable()
        # self.__animator.DehighlightAllNodes()
        # AnimateDijkstras(self.__windowObject.GetMatrix(), 0, self.__animator)

    def DebouncedTogglePauseAnimation(self):
        currentTime = time.time()
        if currentTime - self.__lastClickTime > 0.2:  # 200ms debounce
            self.__lastClickTime = currentTime
            self.EnablePausePlayFunctionality()
    
    def EnablePausePlayFunctionality(self):
        if not self.__animator.GetHasAnimationStarted():
            #If animation not initiallised allow user to enter source node and run animation
            if self.__isSourceNodeInputFormRunning:
                return
            self.__isSourceNodeInputFormRunning = True
            sourceNodeInputFormObject = SourceNodeInputForm(self.__windowObject.GetMatrixLength())
            form = sourceNodeInputFormObject.GetForm()

            #Ensuring when the window is closed via the cross in the top right corner it is handled in the correct way
            form.protocol("WM_DELETE_WINDOW", lambda: self.OnSourceNodeInputFormClose(form))
            sourceNodeInputFormObject.Run()
            #Window.DisplayDataStrucutures(self.__windowObject.GetAxis()[1],self.__windowObject.GetMatrixLength(),  sourceNodeInputForm.GetSourceNodeIndex())
            self.__animator.SetAnimationStarted()
            self.__windowObject.SetSourceNode(sourceNodeInputFormObject.GetSourceNodeIndex())
            self.__animationController.SetAnimationSpeed(1000)
            AnimateDijkstras(self.__windowObject.GetMatrix(), self.__windowObject.GetSourceNode(), self.__animator)
            
        self.__animationController.PauseAnimation()
        new_text = "Resume" if self.__animationController.IsPaused() else "Pause"
        self.__pausePlayButton.config(text=new_text)
    
    def OnSourceNodeInputFormClose(self, form):
        self.__isSourceNodeInputFormRunning = False
        form.destroy()



        


def AnimateDijkstras(adjacencyMatrix: list[list[int]], sourceNodeIndex: int,  animator: Animator) -> None:
    numNodes = len(adjacencyMatrix)
    window = animator.GetFigure().canvas.get_tk_widget().master 
    



    distances = [float('inf')] * numNodes
    distances[sourceNodeIndex] = 0
    animator.UpdateDistancesTableUI(distances)
    animator.SetNodeColour(sourceNodeIndex, 'lightgreen')

    nodesToBeVisited: list[Node] = PriorityQueue()
    visitedNodes: list[Node]= []
    for i in range(numNodes):
        priority = distances[i]
        nodesToBeVisited.Enqueue(Node(NODELABELS[i], priority, i))
        
    def updateAnimation():
        if animator.IsPaused():
            window.after(100, updateAnimation) #Check again if not paused 
            return 
        
        if not animator.IsRunning():  # Check if already running
            animator.SetRunningState(True)  
        else:
            return
        
        if nodesToBeVisited.IsEmpty():
            animator.DehighlightAllNodes()
            print('Animaton Complete!')
            for i in range(numNodes):
                print(f"Shortest distance to {NODELABELS[i]} is {distances[i]}")
    
    
            for i in range(numNodes): 
                visitedNodes[i].OutputNode()
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
                    distances[neighbourIndex] = newDistance
                    nodesToBeVisited.ChangePriority(neighbourNode,newDistance)
                    
        animator.UpdateDistancesTableUI(distances)
        
        
        
        
        animator.UpdateDataStructuresPAndS(visitedNodes, nodesToBeVisited)
        def dehighlightCurrentNodeAndEdges():
            if animator.IsPaused():
                window.after(100, dehighlightCurrentNodeAndEdges)  # Retry after a small delay
                return
            animator.DehighlightEdgesOfNode(currentIndex)
            #animator.DehighlightAllNodes()
            animator.SetRunningState(False)
            window.after(animator.GetFrameDelay(), updateAnimation)  # Call the next animation step after dehighlighting

    # Delay dehighlighting to let highlighting be visible
        window.after(int(animator.GetFrameDelay() * 0.75), dehighlightCurrentNodeAndEdges)
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
    #DisplayWindow(test, 0)
    window = Window()