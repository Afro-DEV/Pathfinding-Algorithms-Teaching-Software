import time
import random

#Main function I will be using
def matrix(n: int,d: float) -> list[list[int]]:
    
    matrix = [[0 for x in range(n)] for y in range(n)]
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
    a = matrix(5, 0)
    b = matrix(5, 50)
    c = matrix(5,100)
    print(a)
    print()
    print(b)
    print()
    print(c)
    #print(type(a))

    #print("My program took", time.time() - start_time, "to run")
