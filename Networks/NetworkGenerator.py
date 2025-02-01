import osmnx as ox
import matplotlib.pyplot as plt
import time
class NetworkFileGenerator():
    def __init__(self):
        ...
    
    def GenerateNewYorkNetwork(self):
        point = (40.7341874, -73.9881721)  # Center coordinate
        graph = ox.graph.graph_from_point(point, dist=3000, network_type="drive") # While Testing
        ox.save_graphml(graph, filepath="Interactive Map Demonstration/Networks/NewYorkNetwork.graphml")
        
        

#Run once to generate Network Files
if __name__ == "__main__":
    #Establishing where Network Cache should go 
    ox.settings.cache_folder = "Interactive Map Demonstration/Networks/Network Cache"
    networkFileGenerator = NetworkFileGenerator()
    
    