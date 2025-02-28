import matplotlib.pyplot as plt
import math
from Utilities import sin, cos, NODELABELS
from Forms import SourceNodeInputForm, GraphGeneratorForm
from Algorithms import GenerateMatrix
from Animation import AnimateDijkstras, AnimationController, Animator
import random
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


BARHEIGHT = 40 # Height in pixels of the UI top and bar elements


class GraphRenderer():
    def __init__(self, adjacencyMatrix, graphAxis):
        self.__adjacencyMatrix = adjacencyMatrix
        self.__numNodes = len(self.__adjacencyMatrix)
        self.__graphAxis = graphAxis
        self.TITLE_FONT_SIZE = 20
    
    def GetAngles(self) -> list[float]:
        """
        Returns a list of angles (0 to 2π) for nodes evenly distributed.

        Returns:
            list[float]: Angles for each node. List length number of nodes
        """
        step = math.pi * 2 / self.__numNodes
        angles = [i * step for i in range(self.__numNodes)]
        return angles


    def CircularLayout(self) -> dict[int, tuple[float,float]]:
        '''Get cooridnates for n number of nodes placed around a unit circle'''
        radius = 1
        angles = self.GetAngles() # Get angle of each node from origin
        coordinates = {}
        for i,angle in enumerate(angles): # For each angle convert it to cartesian cordinates placed on the unit circle
            x_Coord = radius * cos(angle) 
            y_Coord = radius * sin(angle) 
            coordinates[i] = (x_Coord, y_Coord) #Add cordinates as tuple to the dictionary
        return coordinates


    def DisplayGraph(self) :
        nodeReferences = {}
        edgeReferences = [[] for i in range(self.__numNodes)] #Used to store a reference to every edge assigned for a node.
        edgeLabels = []
        labelPositions = []
        #plt.figure(figsize=(8,8))
        coordinates = self.CircularLayout() # Get cordinates for each node
        
        
        for i, (x, y) in coordinates.items():
            node = self.__graphAxis.scatter(x, y, s=300, color='skyblue', zorder=3) #Plot a node on the cartesian grid.
            nodeReferences[i] = node # Store a reference to the node plodded
            self.__graphAxis.text(x, y, NODELABELS[i], fontsize=12, ha='center', va='center') # Add a label to the plotted node
            
        #Plotting the edges
        for i in range(self.__numNodes):
            for j in range(i+1, self.__numNodes):
                if self.__adjacencyMatrix[i][j] !=0: # Ensuring there is a coneection between nodes
                    
                    #Get coordinates for the start of the edge and the end of the
                    #edge starts at on of the nodes and ends at the other node
                    x_Coords = [coordinates[i][0], coordinates[j][0]]
                    y_Coords = [coordinates[i][1], coordinates[j][1]]

                    #MR R FIX? 45 + 55 /100
                    x_mid = (x_Coords[0] + x_Coords[1])/2
                    y_mid = (y_Coords[0] + y_Coords[1])/2

                    edge, = self.__graphAxis.plot(x_Coords, y_Coords, color='grey')
                    #Add the edge reference to the node corresponding to i and j
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
        self.__adjMatrix = [[0,4,3,7,0,0,0], # Initialy use demo matrix.
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
        
        self.DisplayWindow(self.__adjMatrix)
    
    def DisplayDataStrucutures(self, axs, numNodes: int):
        '''Initialise the UI components of the distances table and data structures P,S and the distances table.'''
        columnLabels = [NODELABELS[i] for i in range(numNodes)]
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
        '''Displaying the Dijkstra's demonstration window.'''
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
        
        topBar = TopUIBar(window, self) #Add topUI bar to window 
        
        bottomBar = BottomUIBar(window, animator, self) #Add bottomUI bar to window

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

    def GetMatrix(self) -> list[list]:
        return self.__adjMatrix
    
    def GetMatrixLength(self) -> int:
        return len(self.__adjMatrix)
    
    def GetDemoMatrix(self) -> list[list]:
        return [[0,4,3,7,0,0,0],
                [4,0,0,1,0,4,0],
                [3,0,0,3,5,0,0],
                [7,1,3,0,2,2,7],
                [0,0,5,2,0,0,2],
                [0,4,0,2,0,0,4],
                [0,0,0,7,2,4,0]]
    
    def SetMatrix(self, matrix):
        self.__adjMatrix = matrix
    
    def GetSourceNode(self) -> int:
        return self.__sourceNode
    
    def SetSourceNode(self, sourceNode: int):
        self.__sourceNode = sourceNode

    def StartAnimation(self,adjacencyMatrix: list[list], sourceNodeIndex: int,   animator: Animator):
        AnimateDijkstras( adjacencyMatrix, sourceNodeIndex,   animator)


class TopUIBar():
    def __init__(self, window: tk.Tk, windowObject: DijkstrasDemonstrationWindow):
        self.__window = window
        self.__windowObject: DijkstrasDemonstrationWindow = windowObject
        self.__isGraphGeneratorFormRunning: bool = False
        buttonHeight = 2
        butttonWidth = 8

        self.__topBarFrame = tk.Frame(self.__window, height=BARHEIGHT) #Intialise top bar component
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
            #Get graph parameters from the graph generator form and display a new window
            numNodes = graphGeneratorFormObject.GetNumberOfNodes()
            density = graphGeneratorFormObject.pValue
            matrix = GenerateMatrix(numNodes,density)
            self.__windowObject.SetMatrix(matrix) # Might be redundant
            self.__window.destroy()
            self.__windowObject.DisplayWindow(matrix)
        else:
            #If demo mode selcted use the demo mode matrix
            matrix = self.__windowObject.GetDemoMatrix()
            self.__windowObject.SetMatrix(matrix) # Might be redundant
            self.__window.destroy()
            self.__windowObject.DisplayWindow(matrix)
        

    def OnGraphGeneratorFormClose(self, form):
        self.__isGraphGeneratorFormRunning = False #Set flag to false that the form is running
        form.destroy()

        
    def QuitButtonClick(self):
        self.__window.destroy()
        plt.close('all') #Close MatPlotlib plot.

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
            #If animation not initialised allow user to enter source node and run animation
            if self.__isSourceNodeInputFormRunning:
                return
            sourceNode = self.GetSourceNodeIndexFromForm()
            self.__animator.SetAnimationStarted()
            self.__windowObject.SetSourceNode(sourceNode)
            self.__animationController.SetAnimationSpeed(1000)
            AnimateDijkstras(self.__windowObject.GetMatrix(), self.__windowObject.GetSourceNode(), self.__animator)
            
        self.__animationController.PauseAnimation()
        #Conditionally display Resume or Pause based on state of animation
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
    b = GenerateMatrix(5,50)
    #DisplayWindow(test)
    #DisplayWindow(test, 0)
    window = DijkstrasDemonstrationWindow()