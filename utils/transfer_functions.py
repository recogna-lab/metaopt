import opytimizer.math.random as r
import math as m
import numpy as np

#Sigmoid function and it's variations for feature selection

def s1(otimization_solution):
    """ S1 Transfer Function: The original Sigmoid fuction

    Args:
        otimization_solution (np.array): The best agent's position. 
    """

    features = []

    for i in range(otimization_solution.size):
        rand = r.generate_uniform_random_number()
        
        if rand < 1.0 / (1.0 + m.exp(-1 * otimization_solution[i])):
            features.append(1)
        else:
            features.append(0)

    return np.asarray(features).astype(bool)

def s2(otimization_solution):
    """ S2 Transfer Function 

    Args:
        otimization_solution (np.array): The best agent's position. 
    """

    features = []

    for i in range(otimization_solution.size):

        rand = r.generate_uniform_random_number()
        
        if rand < (1.0 / (1.0 + m.exp(-2 * otimization_solution[i]))):
            #If the feature is selected
            features.append(1)
        else:
            features.append(0)

    return np.asarray(features).astype(bool)

def s3(otimization_solution):
    """ S3 Transfer Function 

    Args:
        otimization_solution (np.array): The best agent's position. 
    """

    features = []

    for i in range(otimization_solution.size):
        rand = r.generate_uniform_random_number()
        if rand < 1.0 / (1.0 + m.exp(-1 * otimization_solution[i] / 2)):
            features.append(1)
        else:
            features.append(0)

    return np.asarray(features).astype(bool)

def s4(otimization_solution):
    """ S4 Transfer Function 

    Args:
        otimization_solution (np.array): The best agent's position. 
    """

    features = []

    for i in range(otimization_solution.size):
        rand = r.generate_uniform_random_number()
        if rand < 1.0 / (1.0 + m.exp(-1 * otimization_solution[i] / 3)):
            features.append(1)
        else:
            features.append(0)

    return np.asarray(features).astype(bool)

def v1(otimization_solution):
    """ V1 Transfer Function

    Args:
        otimization_solution (np.array): The best agent's position. 
    """
    
    features = []

    for i, aux in enumerate(otimization_solution):
        rand = r.generate_uniform_random_number()
        if rand < m.fabs(m.erf(m.sqrt(m.pi) / 2 * (-1 * aux))):
            features.append(1)
        else:
            features.append(0)

    return np.asarray(features).astype(bool)

def v2(otimization_solution):
    """ V2 Transfer Function

    Args:
        otimization_solution (np.array): The best agent's position. 
    """

    features = []

    for i, aux in enumerate(otimization_solution):
        rand = r.generate_uniform_random_number()
        if rand < m.fabs(m.tanh(-1 * aux)):
            features.append(1)
        else:
            features.append(0)

    
    return np.asarray(features).astype(bool)

def v3(otimization_solution):
    """ V3 Transfer Function

    Args:
        otimization_solution (np.array): The best agent's position. 
    """

    features = []

    for i in range(otimization_solution.size):
        rand = r.generate_uniform_random_number()
        if rand < m.fabs(-1 * otimization_solution[i] / m.sqrt(1 + (-1 * (otimization_solution[i] * otimization_solution[i])))):
            features.append(1)
        else:
            features.append(0)

    
    return np.asarray(features).astype(bool)

def v4(otimization_solution):
    """ V4 Transfer Function

    Args:
        otimization_solution (np.array): The best agent's position. 
    """

    features = []

    for i in range(otimization_solution.size):
        rand = r.generate_uniform_random_number()
        if rand < m.fabs(2 / m.pi * m.atan(m.pi / 2 * (-1 * otimization_solution[i]))):
            features.append(1)
        else:
            features.append(0)

    return np.asarray(features).astype(bool)