import osmnx as ox
import os

class BaseNetworkGenerator:
    def __init__(self, cityName: str, centrePoint: tuple[float,float], radius=3000):
        self.cityName= cityName
        self.centrePoint = centrePoint #Centre of network
        # Radius of circle from centre point that should be included in graph (measured in metres)
        self.radius = radius 
        self.filepath = f"Networks/{self.cityName}Network.graphml" #Parameterised file path 

    def GenerateNetwork(self):
        graph = ox.graph.graph_from_point(self.centrePoint, dist=self.radius, network_type="drive") 
        ox.save_graphml(graph, filepath=self.filepath) #Saves graph as graphml file 
    
    @staticmethod
    def CheckFileExists(filepath):
        if os.path.exists(filepath):
            return True
        else:
            return False
    

    @classmethod
    def GenerateAllMissingNetworks(cls):
        ox.settings.cache_folder = "Networks/Network Cache" #Establishing where Network Cache should go 
        for subclass in cls.__subclasses__(): 
         subClassInstance = subclass() # Instantiate each subclass
         
         if not BaseNetworkGenerator.CheckFileExists(subClassInstance.filepath): # If file does not exist generate the network
             subClassInstance.GenerateNetwork()

#Derived Classes
class NewYorkNetworkGenerator(BaseNetworkGenerator):
    def __init__(self):
        super().__init__("NewYork", centrePoint=(40.7341874, -73.9881721)) 

class ParisNetworkGenerator(BaseNetworkGenerator):
    def __init__(self):
        super().__init__("Paris",centrePoint= (48.8584, 2.2945))

class LondonNetworkGenerator(BaseNetworkGenerator):
    def __init__(self):
        super().__init__("London", centrePoint= (51.522921, -0.151174), radius=4000) #Specifying larger radius for London network


        
        

#If ran as main file all missing networks will be generated.
if __name__ == "__main__":
    #Establishing where Network Cache should go 
    ox.settings.cache_folder = "Networks/Network Cache"
    BaseNetworkGenerator.GenerateAllMissingNetworks()
    
    
    
    