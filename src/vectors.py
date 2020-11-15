import math

def dot_product(vector1,vector2):
    n = len(vector1)
    product = 0
    for i in range(n):
        product += vector1[i]*vector2[i]
    return product

def norm(vector):
    n = len(vector)
    sum_squared = 0
    for i in range(n):
        sum_squared += vector[i]**2
    return math.sqrt(sum_squared)
