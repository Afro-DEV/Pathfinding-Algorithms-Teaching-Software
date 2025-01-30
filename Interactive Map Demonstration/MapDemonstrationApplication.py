import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import math
class MapDemonstrationWindow():
    def __init__(self):
        self.graph =  ox.load_graphml(filepath="Interactive Map Demonstration/Networks/LondonNetwork.graphml")
        self.startCoords = (51.5017, -0.1419)  
        self.endCoords = (51.53, -0.15)
        self.click_coords = []
        self.fig, self.ax = plt.subplots()
        self.startNode = ox.distance.nearest_nodes(self.graph, self.startCoords[1], self.startCoords[0])
        self.endNode = ox.distance.nearest_nodes(self.graph, self.endCoords[1], self.endCoords[0])

    def OnClick(self, event):
        x_Coord = event.xdata
        y_Coord = event.ydata
        if x_Coord and y_Coord: #Ensuring valid clicks
            self.click_coords.append((x_Coord, y_Coord))

        print(f"Click {len(self.click_coords)}: ({y_Coord}, {x_Coord})")

        # If two points are clicked, highlight them
        self.HighlightPoints()

    
    def HighlightPoints(self):
        # Clear the previous plot
        self.ax.clear()

        ox.plot_graph(self.graph, ax=self.ax, node_size=10, edge_color='w', bgcolor='black', show=False)

        # If the first click exists, highlight the first point
        if len(self.click_coords) >= 1:
            (x_Coord1, y_Coord1) = self.click_coords[0]
            self.ax.scatter(x_Coord1, y_Coord1, c='r', s=100, marker='.')  # First point in red

        # If the second click exists, highlight the second point
        if len(self.click_coords) >= 2:
            (x_Coord2, y_Coord2) = self.click_coords[1]
            self.ax.scatter(x_Coord2, y_Coord2, c='g', s=100, marker='.')  

        # Redraw the figure to show the updated plot
        plt.draw()
        
    def DisplayNetwork(self):
        # shortestPath = nx.shortest_path(self.graph, source=self.startNode, target=self.endNode, weight='length')
        ox.plot_graph(self.graph, ax=self.ax, node_size=5, edge_color='w', bgcolor='black', show=False)
        self.ax.set_facecolor('black')
        # ax.scatter(self.startCoords[1], self.startCoords[0], c='r', s=100, marker='x') # Start node
        # ax.scatter(self.endCoords[1], self.endCoords[0], c='g', s=100, marker='x') #End node
        # ox.plot_graph_route(self.graph, shortestPath, route_linewidth=4, route_color='r', orig_dest_size=100, ax=ax)
       

        cid = self.fig.canvas.mpl_connect('button_press_event',  self.OnClick)
        plt.show()

    def GetStartNode(self):
        return self.startNode
    def GetEndNode(self):
        return self.endNode
    
    def GetGraph(self):
        return self.graph

class MinHeap:
    def __init__(self):
        #REmeber min will always be top of heapq
        self.__heap = []

    def Insert(self, item):
        self.__heap.append(item)
        index = len(self.__heap)-1
        self.HeapifyUp(index)
    
    def HeapifyUp(self, index):
        if self.HasParent(index) and self.Parent(index)> self.__heap[index]:
            self.Swap(self.GetParentIndex(index), index)
            index = self.GetParentIndex(index)
            #Recursively heapify the index up the Binary tree until it is in the correct position
            self.HeapifyUp(index)

    def HeapifyDown(self, index):
        smallest = index
        if self.HasLeftChild(index) and self.__heap[smallest] > self.LeftChild(index):
            smallest = self.GetLeftChildIndex(index)
        if self.HasRightChild(index) and self.__heap[smallest] > self.RightChild(index):
            smallest = self.GetRightChildIndex(index)
        
        #If this true left or right child of index is smaller than node we are currently at
        if(smallest!= index):
            self.Swap(index, smallest)
            #Recursively move down the tree moving the index to the correct place on tree
            self.HeapifyDown(smallest)

    def RemoveMinValue(self):
        if self.IsEmpty():
            raise('Empty Heap')
        data = self.__heap[0]
        #Replacing last value in the heap with the first value
        self.__heap[0] = self.__heap[-1]
        self.__heap.pop() #Removing last element
        #We Traverse down the tree from top to bottom so index will always be 0
        self.HeapifyDown(0)
        return data

    #HELPER FUNCTIONS 

    def Peek(self):
        if self.IsEmpty():
            raise('Empty Heap')
        return self.__heap[0]

    def Parent(self, index):
        return self.__heap[self.GetParentIndex(index)]

    def LeftChild(self, index):
        return self.__heap[self.GetLeftChildIndex(index)]
    
    def RightChild(self, index):
        return self.__heap[self.GetRightChildIndex(index)]

    def GetLeftChildIndex(self, index):
        return 2* index + 1
        
    
    def GetRightChildIndex(self, index):
        return 2* index + 2
    
    def GetParentIndex(self, index):
        return (index-1)//2

    def HasLeftChild(self, index):
        return self.GetLeftChildIndex(index) < len(self.__heap)

    def HasRightChild(self, index):
        return self.GetRightChildIndex(index) < len(self.__heap)

    def HasParent(self, index):
        return self.GetParentIndex(index) >=0

    def Swap(self, index1, index2):
        temp = self.__heap[index1]
        self.__heap[index1] = self.__heap[index2]
        self.__heap[index2] = temp

    def IsEmpty(self):
        return len(self.__heap) == 0

    def OutputHeap(self):
        print(self.__heap)

def EuclideanDistance(graph, node1, node2):
    coordinateNode1 = NodeToCordiante(graph,node1)
    coordinateNode2 = NodeToCordiante(graph, node2)
    distanceLatitude = abs(coordinateNode1[0]-coordinateNode2[0])
    distanceLongitude = abs(coordinateNode1[1] - coordinateNode2[1])
    distance = math.sqrt(distanceLatitude**2 + distanceLongitude**2)
    return distance

def NodeToCordiante(graph, node):
    return graph.nodes[node]['x'], graph.nodes[node]['y']

def AStar(graph, startNode, endNode):
    
    openSet = []
    cameFrom = {}# Used to track the path
    ...
    #Initialising g and f  for every node to be infinity
    g_score = {node: float('inf') for node in graph.nodes}
    f_score = {node: float('inf') for node in graph.nodes}
    g_score[startNode] = 0
    heuristicEstimate = EuclideanDistance(graph, startNode, endNode)
    f_score[startNode] = g_score[startNode] + heuristicEstimate
    print(f_score) 

    while len(openSet) > 0:
        ...

    EuclideanDistance(graph, startNode, endNode)


if __name__ == "__main__":
    # window = MapDemonstrationWindow()
    # window.DisplayNetwork()

    # graph =  ox.load_graphml(filepath="Interactive Map Demonstration/Networks/LondonNetwork.graphml")
    # startCoords = (51.5017, -0.1419)  
    # endCoords = (51.53, -0.15)
    # startNode = ox.distance.nearest_nodes(graph, startCoords[1], startCoords[0])
    # endNode = ox.distance.nearest_nodes(graph, endCoords[1], endCoords[0])

    # AStar(graph, startNode, endNode)
    heap = MinHeap()
    heap.Insert(20)
    heap.Insert(8)
    heap.Insert(15)
    heap.Insert(30)
    heap.Insert(5)
    heap.Insert(10)
    heap.Insert(0)
    heap.RemoveMinValue( )
    heap.OutputHeap()

    