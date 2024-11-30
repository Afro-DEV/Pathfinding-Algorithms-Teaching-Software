from DataStructures import Node, PriorityQueue
import generatingmatix as g

nodeLabels = {i: chr(65+i) for i in range(11)}
def dijkstras(sourceNodeIndex, adjacencyMatrix):
    numNodes = len(adjacencyMatrix)
    distances = [float('inf')] * numNodes
    distances[sourceNodeIndex] = 0
    #visited = [False] * numNodes
    nodesToBeVisited: list[Node] = PriorityQueue()
    visitedNodes: list[Node]= []
    for i in range(numNodes):
        priority = distances[i]
        nodesToBeVisited.Enqueue(Node(nodeLabels[i], priority, i,False))
        
    #nodesToBeVisited.queue[sourceNode].SetPriority(0)
    #sourceNode = nodesToBeVisited.ReturnNodeAtIndex(sourceNodeIndex)
    #nodesToBeVisited.ChangePriority(sourceNode, 0)
    nodesToBeVisited.OutputQueue()

    
    #nodesToBeVisited.ChangePriority(, 0)
    #nodesToBeVisited.OutputQueue()
    while not nodesToBeVisited.IsEmpty():
        currentNode: Node = nodesToBeVisited.Peek()
        nodesToBeVisited.Dequeue()
        currentIndex = currentNode.GetIndex()
        # if currentNode.GetVisitedState():
        #     print('hi')
        #     #Skip node if already visited
        #     continue
        
        # currentNode.SetVisitedStateTrue()
        #-------------------------
        # if visited[currentIndex]:
        #     continue
        
        # # Mark the node as visited
        # visited[currentIndex] = True
        #--------------------------------
        # if currentNode in visitedNodes:
        #     print('hi')
        #     continue
        visitedNodes.append(currentNode)
        

        for neighbourIndex in range(numNodes):
            weight = adjacencyMatrix[currentIndex][neighbourIndex]
            
            #neighbourNode of type None when neighbourNode has already been visited
            neighbourNode: Node = nodesToBeVisited.GetNodeByIndex(neighbourIndex)
            if weight > 0 and neighbourNode != None:
                newDistance = distances[currentIndex] + weight
                

                if newDistance < distances[neighbourIndex]:
                    distances[neighbourIndex] = newDistance
                    nodesToBeVisited.ChangePriority(neighbourNode,newDistance)
        
    print(distances)
    for i in range(numNodes):
        print(f"Shortest distance to {nodeLabels[i]} is {distances[i]}")
    
    for i in range(numNodes):
        visitedNodes[i].OutputNode()

        



        #-------------------------
        #index = list(labels.keys())[list(labels.values()).index(currentNode.GetLabel())]
        #print(index)
        # for i in range(len(adjacencyMatrix[currentNode.GetIndex()])):
        #     if adjacencyMatrix[currentNode.GetIndex()][i] < currentNode.GetPriority() and adjacencyMatrix[currentNode.GetIndex()][i] != 0:
        #         currentNode.SetPriority(adjacencyMatrix[currentNode.GetIndex()][i])
        # visitedNodes.append(currentNode)
        #-------------------------
    # print('hi')
    # for each in visitedNodes:
    #      each.OutputNode()
        
    
if __name__== '__main__':
    a = g.matrix(4,5)
    matrix = [[ 0, 10,  5,],
    [10,  0, 12],
    [ 5, 12,  0,]]


    demo = [[0,5,3,0],
            [5,0,0,2],
            [3,0,0,0],
            [0,2,0,0]]
    
    test = [[0,4,3,7,0,0,0],
            [4,0,0,1,0,4,0],
            [3,0,0,3,5,0,0],
            [7,1,3,0,2,2,7],
            [0,0,5,2,0,0,2],
            [0,4,0,2,0,0,4],
            [0,0,0,7,2,4,0]]
    
    #print(a)
    # dijkstras(0, demo)
    #dijkstras(0, demo)
    # dijkstras(2, demo)
    # dijkstras(3, demo)
    dijkstras(0, test)