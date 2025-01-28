import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
class MapDemonstrationWindow():
    def __init__(self):
        self.graph =  ox.load_graphml(filepath="Interactive Map Demonstration/Networks/LondonNetwork.graphml")
        self.startCoords = (51.5017, -0.1419)  
        self.endCoords = (51.53, -0.15)

        self.startNode = ox.distance.nearest_nodes(self.graph, self.startCoords[1], self.startCoords[0])
        self.endNode = ox.distance.nearest_nodes(self.graph, self.endCoords[1], self.endCoords[0])

    def OnClick(self, event):
        x_Coord = event.xdata
        y_Coord = event.ydata
        node = ox.distance.nearest_nodes(self.graph)
        print(x_Coord, y_Coord)
        
    def DisplayNetwork(self):
        shortest_path = nx.shortest_path(self.graph, source=self.startNode, target=self.endNode, weight='length')
        fig, ax = ox.plot_graph(self.graph, node_size=0, edge_color='w', bgcolor='k', show=False)
        ax.scatter(self.startCoords[1], self.startCoords[0], c='r', s=100, marker='x') # Start node
        ax.scatter(self.endCoords[1], self.endCoords[0], c='g', s=100, marker='x') #End node
        ox.plot_graph_route(self.graph, shortest_path, route_linewidth=4, route_color='r', orig_dest_size=100, ax=ax)
       

        #cid = fig.canvas.mpl_connect('button_press_event',  self.OnClick)
        plt.show()

if __name__ == "__main__":
    window = MapDemonstrationWindow()
    window.DisplayNetwork()