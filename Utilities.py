import math
from functools import reduce
upperLimitOfExpansion = 100
def factorial(num):
    if num == 0 or num == 1:
        return 1
    return num *factorial(num-1)
def cos(x):
    #Calculating cos x via maclaurin expanision
    negativeTerms = reduce(lambda x,y: x+y,[-(x**i)/factorial(i) for i in range(2,upperLimitOfExpansion,4)])
    positiveTerms = reduce(lambda x,y: x+y,[(x**i)/factorial(i) for i in range(4,upperLimitOfExpansion,4)])
    return 1 + negativeTerms + positiveTerms

def sin(x):
    #Calculating sin x via maclaurin expanision
    negativeTerms = reduce(lambda x,y: x+y,[-(x**i)/factorial(i) for i in range(3,upperLimitOfExpansion,4)])
    positiveTerms = reduce(lambda x,y: x+y,[(x**i)/factorial(i) for i in range(5,upperLimitOfExpansion,4)])
    return x + negativeTerms + positiveTerms
if __name__ == '__main__':
    print([i for i in range(3,20,4)])
    pi = math.pi
    a=1
    
    print(cos(pi))
    print(sin(pi))