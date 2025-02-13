import osmnx as ox
import matplotlib.pyplot as plt
import time
import os
class BaseNetworkGenerator:
    def __init__(self, cityName, centrePoint, distance=3000):
        self.cityName= cityName
        self.centrePoint = centrePoint
        self.distance = distance
        self.filepath = f"Networks/{self.cityName}Network.graphml" #Parameterised file path 

    def GenerateNetwork(self):
        graph = ox.graph.graph_from_point(self.centrePoint, dist=self.distance, network_type="drive")
        ox.save_graphml(graph, filepath=self.filepath)
    
    @staticmethod
    def CheckFileExists(filepath):
        if os.path.exists(filepath):
            return True
        else:
            return False
    

    @classmethod
    def GenerateAllMissingNetworks(cls):
        ox.settings.cache_folder = "Interactive Map Demonstration/Networks/Network Cache" #Establishing where Network Cache should go 
        for subclass in cls.__subclasses__(): 
         subClassInstance = subclass() # Instantiate each subclass
         
         if not BaseNetworkGenerator.CheckFileExists(subClassInstance.filepath):
             subClassInstance.GenerateNetwork()

class NewYorkNetworkGenerator(BaseNetworkGenerator):
    def __init__(self):
        super().__init__("NewYork", (40.7341874, -73.9881721))

class ParisNetworkGenerator(BaseNetworkGenerator):
    def __init__(self):
        super().__init__("Paris",(48.8584, 2.2945))


        
        

#Run once to generate Network Files
if __name__ == "__main__":
    #Establishing where Network Cache should go 
    ox.settings.cache_folder = "Interactive Map Demonstration/Networks/Network Cache"
    # p = NewYorkNetworkGenerator()
    # p.GenerateNetwork()
    BaseNetworkGenerator.GenerateAllMissingNetworks()
    
    
    
    