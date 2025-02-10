import osmnx as ox
import matplotlib.pyplot as plt
import time
class NetworkFileGenerator():
    def __init__(self):
        self.CENTRE_POINTS = {}
    
    def GenerateNewYorkNetwork(self):
        centrePoint = (40.7341874, -73.9881721)  # Center coordinate
        graph = ox.graph.graph_from_point(centrePoint, dist=3000, network_type="drive") # While Testing
        ox.save_graphml(graph, filepath="Networks/NewYorkNetwork.graphml")
    
    
    def GenerateParisNetwork(self):
        #centrePoint = (35.6594347, 139.6799793)
        centrePoint = (48.8584, 2.2945)
        graph = ox.graph.graph_from_point(centrePoint, dist=3000, network_type='drive')
        ox.save_graphml(graph, filepath="Networks/ParisNetwork.graphml")

        
        

#Run once to generate Network Files
if __name__ == "__main__":
    #Establishing where Network Cache should go 
    ox.settings.cache_folder = "Interactive Map Demonstration/Networks/Network Cache"
    NetworkFileGenerator.GenerateParisNetwork()
    
    
    