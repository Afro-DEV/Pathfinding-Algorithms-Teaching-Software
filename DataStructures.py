class Node():
    def __init__(self, label,priority, id, ):
        self.__label: str = label
        self.__priority = priority
        self.__id: int = id
        

    def OutputNode(self):
        print((f"({self.__label}, {self.__priority})"))

    def GetPriority(self):
        return self.__priority
    

    def GetNodeData(self):
        return f"({self.__label}, {self.__priority})"
    
    def GetID(self) -> int:
        return self.__id
    
    def GetLabel(self)-> str:
        return self.__label
    
    

    def SetPriority(self, newPriority):
        self.__priority = newPriority
    
   

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

    def GetNodeByID(self, index: int) -> Node:
        for node in self.__queue:
            if node.GetID() == index:
                return node
        #Therefore node has already been visited
        return None

    def GetQueue(self) -> list[Node]:
        return self.__queue
    
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
        minValue = self.__heap[0]
        #Replacing last value in the heap with the first value
        self.__heap[0] = self.__heap[-1]
        self.__heap.pop() #Removing last element
        #We Traverse down the tree from top to bottom so index will always be 0
        self.HeapifyDown(0)
        return minValue

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

    def GetLeftChildIndex(self, index) -> int:
        return 2* index + 1
        
    
    def GetRightChildIndex(self, index) -> int:
        return 2* index + 2
    
    def GetParentIndex(self, index) -> int:
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
    
    def GetHeap(self):
        return self.__heap
    
    def GetHeapLength(self):
        return len(self.__heap)

    def OutputHeap(self):
        print(self.__heap)