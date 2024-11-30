import time
import random
import numpy as np

def matrix2(n,d):
    
    matrix = np.array([[float('inf') for x in range(n)] for y in range(n)])
    for i in range(n):
        matrix[i][i] = 0
        for j in range(n):
            pValue = random.random() #Generates random number between 0 and 1
            if pValue < d/100 and matrix[i][j] != 0: # if we are assigning an edge
                if matrix[j][i] == float('inf') or 0:
                    matrix[i][j] = random.randint(2,12)
                matrix[j][i] = matrix[i][j]

    for i in range(n):
        #print('=========================')
        #print(i)
        #print('==========================')
        for j in range(n):
            pass
            #print(matrix[i][j])
            



    

    return matrix

def matrix(n,d):
    
    matrix = np.array([[0 for x in range(n)] for y in range(n)])
    for i in range(n):
        matrix[i][i] = 0
        for j in range(n):
            pValue = random.random() #Generates random number between 0 and 1
            if pValue < d/100: # if we are assigning an edge
                if matrix[j][i] == 0 and i !=j and matrix[i][j] == 0:
                    matrix[i][j] = random.randint(2,12)
                matrix[j][i] = matrix[i][j]

#Neater function
def matrix3(n,d):
    
    matrix = np.array([[0 for x in range(n)] for y in range(n)])
    for i in range(n):
        matrix[i][i] = 0
        for j in range(i+1, n):
            pValue = random.random() #Generates random number between 0 and 1
            if pValue < d/100: # if we are assigning an edge
                if i !=j and matrix[i][j] == 0:
                    matrix[i][j] = random.randint(2,12)
                matrix[j][i] = matrix[i][j]
    return matrix

if __name__ == "__main__":
    start_time = time.time()
    a = matrix3(5, 0)
    b = matrix3(5, 50)
    c = matrix3(5,100)
    print(a)
    print()
    print(b)
    print()
    print(c)
    #print(type(a))

    #print("My program took", time.time() - start_time, "to run")
