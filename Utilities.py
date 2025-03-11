import math
from functools import reduce
UPPER_LIMIT_OF_EXPANSION = 100
NODELABELS = {i: chr(65+i) for i in range(26)} #Dictionary to access a node label from ID e.g 0 -> A, 1 -> B...

def factorial(num: int) -> int:
    '''Returns factorial of an integer'''
    
    if num == 0 or num == 1:
        return 1
    return num *factorial(num-1)

def cos(x: float) -> float:
    '''Returns cosine of angle(in radians) via Maclaurin expansion'''

    negativeTerms = reduce(lambda x,y: x+y,[-(x**i)/factorial(i) for i in range(2,UPPER_LIMIT_OF_EXPANSION,4)]) #Calculating positive terms in Maclaurin expansion
    positiveTerms = reduce(lambda x,y: x+y,[(x**i)/factorial(i) for i in range(4,UPPER_LIMIT_OF_EXPANSION,4)])#Calculating positive terms in Maclaurin expansion
    return 1 + negativeTerms + positiveTerms

def sin(x: float) -> float:
    '''Returns sine of angle(in radians) via Maclaurin expansion'''

    negativeTerms = reduce(lambda x,y: x+y,[-(x**i)/factorial(i) for i in range(3,UPPER_LIMIT_OF_EXPANSION,4)])  #Calculating negative terms in Maclaurin expansion
    positiveTerms = reduce(lambda x,y: x+y,[(x**i)/factorial(i) for i in range(5,UPPER_LIMIT_OF_EXPANSION,4)])#Calculating positive terms in Maclaurin expansion
    return x + negativeTerms + positiveTerms

def ConvertDegreesToRadians(x: float) -> float:
    return x * math.pi/180

def ConvertKilometresToMiles(length: float) -> float:
    '''Converts Kilometres To Miles Correct to one decimal place'''
    return round(length / 1.609, 1)

def IdToCharacter(id: int) -> str:
    '''
    Converts an numeric Integer to respective alphabetic character
    For example 0-> A, 1-> B, 2-> C....
    '''
    return chr(id+65) 

def CharacterToId(char: str) -> int:
    '''
    Converts an alphabetic character to its respective id
    For example A -> 0, B-> 1, C-> 2...
    '''
    return ord(char) - 65

if __name__ == '__main__':
    print([i for i in range(3,20,4)])

    print(IdToCharacter(0))
    print(CharacterToId('A '))