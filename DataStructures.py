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
            raise ValueError('Empty Heap')
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

import random
def GetRandomTuple():
    return (random.randint(1,10), random.randint(10,30))

class Stack():
    def __init__(self):
        self.__stack = []
        self.__pointer = -1

    def Push(self, data):
        self.__pointer +=1
        self.__stack.append(data)
    
    def Pop(self):
        topOfStack = self.__stack[self.__pointer]
        self.__pointer -=1
        return topOfStack
    
    def OutputStack(self):
        print(self.__stack)
    
    def IsEmptyStack(self):
        return self.__pointer == -1


        

def ListReversal(array):
    stack = Stack()
    newarr = []
    for each in array:
        stack.Push(each)
    
    while not stack.IsEmptyStack():
        newarr.append(stack.Pop())
    print(newarr)


if __name__ == '__main__':
    ListReversal([3,5,6,7,19])
    
    # minheap.Insert(10)
    # minheap.Insert(4)
    # minheap.Insert(9)
    # minheap.Insert(1)
    # minheap.Insert(7)

    # minheap.OutputHeap()
    # minheap.RemoveMinValue()
    # minheap.OutputHeap()


    