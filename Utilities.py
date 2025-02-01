import math
from functools import reduce
UPPER_LIMIT_OF_EXPANSION = 100
def factorial(num: int) -> int:
    '''Returns factorial of number'''
    
    if num == 0 or num == 1:
        return 1
    return num *factorial(num-1)
def cos(x: float) -> float:
    '''Returns cosine of angle via maclaurin expanision'''

    negativeTerms = reduce(lambda x,y: x+y,[-(x**i)/factorial(i) for i in range(2,UPPER_LIMIT_OF_EXPANSION,4)])
    positiveTerms = reduce(lambda x,y: x+y,[(x**i)/factorial(i) for i in range(4,UPPER_LIMIT_OF_EXPANSION,4)])
    return 1 + negativeTerms + positiveTerms

def sin(x: float) -> float:
    '''Returns sine of angle via maclaurin expanision'''

    negativeTerms = reduce(lambda x,y: x+y,[-(x**i)/factorial(i) for i in range(3,UPPER_LIMIT_OF_EXPANSION,4)])
    positiveTerms = reduce(lambda x,y: x+y,[(x**i)/factorial(i) for i in range(5,UPPER_LIMIT_OF_EXPANSION,4)])
    return x + negativeTerms + positiveTerms

def ConvertDegreesToRadians(x: float):
    return x * math.pi/180

def IdToCharacter(id):
    return chr(id+65) 

def CharacterToId(char):
    return ord(char) - 65

if __name__ == '__main__':
    print([i for i in range(3,20,4)])

    print(IdToCharacter(0))
    print(CharacterToId('A '))