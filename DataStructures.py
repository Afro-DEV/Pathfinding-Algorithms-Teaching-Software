class Node():
    def __init__(self, label,priority, id):
        self.__label: str = label
        self.__priority = priority
        #The Id property is a numerical value corresponding to the label of a Node
        #E.g A--> 0, B --> 1, C--> 2....
        self.__id: int = id
        

    def OutputNode(self):
        #Output the nodes label followed by curent priority 
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
        # Lower priority node goes first if priority equal then goes in alphabetical order of label
            if node.GetPriority() < item.GetPriority() or (node.GetPriority() == item.GetPriority() and node.GetLabel() < item.GetLabel()):
                self.__queue.insert(index, node)
                return
    # If no suitable position is found, append to the end
        self.__queue.append(node)
        
                

        
    def Peek(self) -> Node:
        '''Returns value at the  front of the queue without removal.'''
        return self.__queue[0]
             
     
        
    def Dequeue(self) -> None:
        '''Removes Item at the front of the priority queue'''
        self.__queue.pop(0)
                 

    def IsEmpty(self) -> bool:
        if len(self.__queue) == 0:
            return True
        else:
            return False

    def ChangePriority(self, node: Node, priority:int) -> Node:
        '''Change Priority of node by removing instance of node and inserting a new
            instance of the node with the new priority '''
        temp: Node = node
        self.__queue.remove(node)  # Removing node of old priority
        temp.SetPriority(priority)
        self.Enqueue(temp) # Adding node with the new priority 
    
    
    
    def ReturnNodeAtIndex(self, index: int) -> Node:
        return self.__queue[index]
        
    def OutputQueue(self)-> None:
        for item in self.__queue:
            print(item.GetNodeData(), end= "")
        print()

    def GetNodeByID(self, id: int) -> Node:
        '''Gets the node object by ID'''
        for node in self.__queue:
            if node.GetID() == id:
                return node
        #Node not in queue
        return None

    def GetQueue(self) -> list[Node]:
        return self.__queue
    
class MinHeap:
    def __init__(self):
        self.__heap = []

    def Insert(self, item):
        self.__heap.append(item)
        index = self.HeapLength() -1
        #Moves item up tree to its correct position to maintain the minheap property
        self.HeapifyUp(index)
    
    def HeapifyUp(self, index):
        if self.HasParent(index) and self.Parent(index)> self.__heap[index]:
            self.SwapValues(self.GetParentIndex(index), index) #If parent is greater than child then incorrect position so swap the parent and child node
            index = self.GetParentIndex(index)
            #Recursively heapify the index up the Binary tree until it is in the correct position
            self.HeapifyUp(index)

    def HeapifyDown(self, index):
        smallest = index # Initialise smallest as the index of the current node
        
        #Check if left or right child is the smallest node found
        if self.HasLeftChild(index) and self.__heap[smallest] > self.LeftChild(index):
            smallest = self.GetLeftChildIndex(index)
        if self.HasRightChild(index) and self.__heap[smallest] > self.RightChild(index):
            smallest = self.GetRightChildIndex(index)
        
        #If smallest value is not the current node swap and heapify down the tree
        if(smallest!= index): #left or right child of current node is smaller than node we are currently at
            self.SwapValues(index, smallest)
            #Recursively move down the tree moving the smallest node to the correct place on tree
            self.HeapifyDown(smallest) #Heapify down from the new position of the current node

    def RemoveMinValue(self):
        if self.IsEmpty():
            raise ValueError('Empty Heap')
        #Store minimum value from root of heap
        minValue = self.__heap[0]
        #Replace root of the heap with the last element
        self.__heap[0] = self.__heap[-1]
        self.__heap.pop() #Removing last element from heap
        #Restore heap property by traversing down from the root
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
        '''Returns the index of the left child node which is always 2* node index + 1'''
        return 2* index + 1
        
    
    def GetRightChildIndex(self, index) -> int:
        '''Returns the index of the right child node  which is always 2* node index + 2'''
        return 2* index + 2
    
    def GetParentIndex(self, index) -> int:
        '''Returns the parent index which is always the floor division by 2 of the node index -1'''
        return (index-1)//2

    #The Has__ functions work by checking if computed index for left child, right child  or parent node index is between 0 and the length of the heap.
    def HasLeftChild(self, index):
        return self.GetLeftChildIndex(index) < self.HeapLength()

    def HasRightChild(self, index):
        return self.GetRightChildIndex(index) < self.HeapLength()

    def HasParent(self, index):
        return self.GetParentIndex(index) >=0

    def SwapValues(self, index1, index2):
        '''Swaps the values of the 2 nodes in the heap at the respective indexes.'''
        temp = self.__heap[index1]
        self.__heap[index1] = self.__heap[index2]
        self.__heap[index2] = temp

    def IsEmpty(self):
        return self.HeapLength() == 0
    
    def GetHeap(self) -> list:
        return self.__heap
    
    def HeapLength(self) -> int:
        return len(self.__heap)

    def OutputHeap(self):
        print(self.__heap)


class Stack():
    def __init__(self):
        self.__stack = []
        self.__pointer = -1  #Pointer -1 indicates empty stack

    def Push(self, data):
        """
        Push an item onto the Stack

        :param data: The data to be pushed onto the stack.
        """
        self.__pointer +=1
        self.__stack.append(data)
    
    def Pop(self) -> any:
        """
        Pop the top item off the stack.

        :return: The data from the top of the stack or Empty Stack
        """
        if self.IsEmptyStack():
            return 'Empty Stack'
        topOfStack = self.__stack[self.__pointer]
        self.__pointer -=1
        return topOfStack
    
    def OutputStack(self):
        print(self.__stack)
    
    def IsEmptyStack(self):
        return self.__pointer == -1
    
class LinkedListNode():
    def __init__(self, data, parent=None):
        self.__data = data
        #Parent attribute links the current node to previous node in list.
        self.__parent = parent 
    
    def GetData(self):
        return self.__data
    
    def GetParent(self):
        return self.__parent 



if __name__ == '__main__':
    minheap = MinHeap()
    
    minheap.Insert(10)
    minheap.Insert(4)
    minheap.Insert(9)
    minheap.Insert(1)
    minheap.Insert(7)

    minheap.OutputHeap()
    minheap.RemoveMinValue()
    minheap.OutputHeap()


    