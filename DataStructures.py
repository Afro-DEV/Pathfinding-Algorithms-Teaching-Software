class Node():
    def __init__(self, label,priority, index, visitedState):
        self.__label: str = label
        self.__priority = priority
        self.__index: int = index
        self.__visitedState:bool  = visitedState

    def OutputNode(self):
        print((f"({self.__label}, {self.__priority})"))

    def GetPriority(self):
        return self.__priority
    

    def GetNodeData(self):
        return f"({self.__label}, {self.__priority})"
    
    def GetIndex(self) -> int:
        return self.__index
    
    def GetLabel(self)-> str:
        return self.__label
    
    def GetVisitedState(self):
        return self.__visitedState

    def SetPriority(self, newPriority):
        self.__priority = newPriority
    
    def SetVisitedStateTrue(self):
        self.__visitedState = True

class PriorityQueue():
    def __init__(self):
        self.__queue: list[Node] = []
    
    def Enqueue(self, node: Node) -> None:
        for index, item in enumerate(self.__queue):
        # Lower priority node goes first if equal then goes in alphabetical order of lael
            if node.GetPriority() < item.GetPriority() or (node.GetPriority() == item.GetPriority() and node.GetLabel() < item.GetLabel()):
                self.__queue.insert(index, node)
                return
    # If no suitable position is found, append to the end
        self.__queue.append(node)
        # if self.IsEmpty() == True: 
        #     self.__queue.append(node)
        #     return
        # for item in self.__queue:
        #     #print(item)
        #     index = self.__queue.index(item)
        #     leftList = self.__queue[:index] #
        #     rightList = self.__queue[index:]
                    
        #     if item.GetPriority() > node.GetPriority():
                
        #         leftList.append(node)
        #         self.__queue = leftList + rightList
                
        #         return
        #     elif item.GetPriority() == node.GetPriority():
        #         print('lko')
        #         self.OutputQueue()
        #         #If 2 nodes same priority go in Alphabetical order
        #         if ord(item.GetLabel())  > ord(node.GetLabel()):
        #             leftList.append(node)
        #         else:
        #             rightList.insert(1, node)
        #         self.__queue = leftList + rightList
        #         return
            
        # self.__queue.append(node)
                

        
    def Peek(self) -> Node:
        return self.__queue[0]
             
     
        
    def Dequeue(self) -> None:
        self.__queue.pop(0)
                 

    def IsEmpty(self) -> bool:
        if len(self.__queue) == 0:
            return True
        else:
            return False

    def ChangePriority(self, node: Node, priority:int) -> Node:
        #Insert into correct place delete occurence
        temp: Node = node
        self.__queue.remove(node)
        temp.SetPriority(priority)
        self.Enqueue(temp)
    
    
    
    def ReturnNodeAtIndex(self, index: int) -> Node:
        return self.__queue[index]
        
    def OutputQueue(self)-> None:
        #print(len(self.queue))
        for item in self.__queue:
            print(item.GetNodeData(), end= "")
        print()

    def GetNodeByIndex(self, index: int) -> Node:
        for node in self.__queue:
            if node.GetIndex() == index:
                return node
        #Therefore node has already been visited
        return None

    def GetQueue(self) -> list[Node]:
        return self.__queue