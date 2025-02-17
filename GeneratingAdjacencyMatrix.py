import time
import random

def GenerateMatrix(numberOfNodes: int,densityVal: float) -> list[list[int]]:
    '''
    Generate an adjacency matrix with random weights of size corresponding to the numberOfNodes param.
    And connectivity correponding to the densityVal param.
    '''
    matrix = [[0 for x in range(numberOfNodes)] for y in range(numberOfNodes)] # Populating an n x n matrix with only zeroes
    for i in range(numberOfNodes):
        for j in range(i+1, numberOfNodes):
            pValue = random.random() #Generates random number between 0 and 1
            if pValue < densityVal/100: # if random number is less than specified density value then we create an edge. 
                matrix[i][j] = random.randint(2,12) # Assign edge random weighting
                matrix[j][i] = matrix[i][j] # Update adjacency matrix connection going to the other way to create an undirected edge.
    return matrix

def OutputMatrix(matrix):
    for each in matrix:
        print(each)

if __name__ == "__main__":
    start_time = time.time()
    a = GenerateMatrix(5, 0)
    b = GenerateMatrix(5, 50)
    c = GenerateMatrix(10,100)
    # print(a)
    # print()
    # print(b)
    # print()
    # print(c)

    OutputMatrix(c)
    print(c[0][0])
    #print(type(a))

    #print("My program took", time.time() - start_time, "to run")
