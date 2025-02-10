import osmnx as ox
import matplotlib.pyplot as plt
import time
class BaseNetworkGenerator:
    def __init__(self, cityName, centrePoint, distance=3000):
        self.cityName= cityName
        self.centrePoint = centrePoint
        self.distance = distance

    def GenerateNetwork(self):
        graph = ox.graph.graph_from_point(self.centrePoint, dist=self.distance, network_type="drive")
        filepath = f"Networks/{self.cityName}Network.graphml"
        ox.save_graphml(graph, filepath=filepath)

class NewYorkNetworkGenerator(BaseNetworkGenerator):
    def __init__(self):
        super().__init__("NewYork", (40.7341874, -73.9881721))

class ParisNetworkGenerator(BaseNetworkGenerator):
    def __init__(self):
        super().__init__("Paris",(48.8584, 2.2945))

# class NetworkFileGenerator():
#     def __init__(self):
#         self.CENTRE_POINTS = {}


#     @staticmethod    
#     def GenerateNewYorkNetwork():
#         centrePoint = (40.7341874, -73.9881721)  # Center coordinate
#         graph = ox.graph.graph_from_point(centrePoint, dist=3000, network_type="drive") # While Testing
#         ox.save_graphml(graph, filepath="Networks/NewYorkNetwork.graphml")
    
    
#     def GenerateParisNetwork(self):
#         #centrePoint = (35.6594347, 139.6799793)
#         centrePoint = (48.8584, 2.2945)
#         graph = ox.graph.graph_from_point(centrePoint, dist=3000, network_type='drive')
#         ox.save_graphml(graph, filepath="Networks/ParisNetwork.graphml")

#     def GenerateMissingNetworks(self):
#         ...

        
        

#Run once to generate Network Files
if __name__ == "__main__":
    #Establishing where Network Cache should go 
    ox.settings.cache_folder = "Interactive Map Demonstration/Networks/Network Cache"
    p = NewYorkNetworkGenerator()
    p.GenerateNetwork()
    # NetworkFileGenerator.GenerateParisNetwork()
    
    
    