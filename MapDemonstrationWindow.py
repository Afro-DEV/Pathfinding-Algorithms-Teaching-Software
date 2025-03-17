import osmnx as ox
import matplotlib.pyplot as plt
from NetworkGenerator import BaseNetworkGenerator
from matplotlib.widgets import Button
from Animation import NetworkAnimator

class MapDemonstrationWindow():
    def __init__(self, network: str, algorithm: str, useMiles: bool):
        PATH_FINDING_ALGORITHMS_TO_ID = {'A-Star': 0, 'Dijkstras':1}
        self.networkName = network
        self.filepath = self.GetNetworkSelectedFilePath(network)
  
        if not BaseNetworkGenerator.CheckFileExists(self.filepath):
            BaseNetworkGenerator.GenerateAllMissingNetworks()

        self.__graph =  ox.load_graphml(filepath=self.filepath) #Load graph from file path as type NetworkX multi d Graph 

        #Create Dictionary to store styles for the graph     
        self.GRAPH_STYLES = {'EdgeColour': "Grey",
                            'EdgeWidth': 0.3,
                            'StartNodeColour': 'limegreen',
                            'EndNodeColour': '#ff0000', 
                            'NodeSize': 2 }
        try:
            self.algorithmId = PATH_FINDING_ALGORITHMS_TO_ID[algorithm]
        except:
            #In case the user manages to write into the dropdown box which should not be possible
            raise ValueError('Unexpected value passed for algorithmId')
            
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
        #Parametrised File path
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
        self.ax.set_title('Click 2 points on the road network to begin pathfinding.', loc='center', fontsize=12, color='black')

        plt.show()
        

    def OnClick(self, event):
        if event.inaxes != self.ax:  # Ignore clicks outside the main plot area
            return
        x_Coord = event.xdata
        y_Coord = event.ydata

                
        if self.CheckValidClick(x_Coord, y_Coord) and len(self.click_coords) < 2: #Ensuring valid clicks
            #If second click coordinate is not far enough away from first click do not add to click coords.
            if len(self.click_coords) == 1 and not self.CheckIfCoordsAreSpaced(x_Coord, y_Coord): 
                return 
            self.click_coords.append((x_Coord, y_Coord))
            self.HighlightPoints()

        if len(self.click_coords) == 2:# If two points are clicked, highlight them
            self.ax.clear()
            self.RemoveUndoButton()
            animator = NetworkAnimator(self.__graph,self.click_coords[0], self.click_coords[1], self.algorithmId, self.useMiles, self.figAndAxis, self.GRAPH_STYLES, self.networkName)
            animator.StartAnimation()
            self.fig.canvas.draw_idle()
    
    def CheckIfCoordsAreSpaced(self, x_Coord: float, y_Coord: float) -> bool:
        if ox.nearest_nodes(self.__graph, x_Coord, y_Coord) == ox.nearest_nodes(self.__graph,  self.click_coords[0][0], self.click_coords[0][1]):
            return False
        return True
    
    def CheckValidClick(self, x_Coord: float, y_Coord: float) -> bool:
        '''Return True if both of the x and y coordinate is not equal to none'''
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


if __name__ == "__main__":
    window = MapDemonstrationWindow("London", algorithm='A-Star', useMiles=False)
    window.DisplayNetwork()
    