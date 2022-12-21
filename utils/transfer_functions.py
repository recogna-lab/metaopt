import math as m

import numpy as np
import opytimizer.math.random as r

# Sigmoid function and some of its variations used in feature selection
# They are applied to 'sol', which is the solution outputted by an optimizer

# S1 Transfer Function: The original Sigmoid fuction
def s1(sol):
    features = []

    for i in range(sol.size):
        rand = r.generate_uniform_random_number()
        
        if rand < 1.0 / (1.0 + m.exp(-1 * sol[i])):
            features.append(1)
        else:
            features.append(0)

    return np.asarray(features).astype(bool)

# S2 Transfer Function
def s2(sol):
    features = []

    for i in range(sol.size):
        rand = r.generate_uniform_random_number()
        
        if rand < (1.0 / (1.0 + m.exp(-2 * sol[i]))):
            # If the feature is selected
            features.append(1)
        else:
            features.append(0)

    return np.asarray(features).astype(bool)

# S3 Transfer Function
def s3(sol):
    features = []

    for i in range(sol.size):
        
        rand = r.generate_uniform_random_number()
        
        if rand < 1.0 / (1.0 + m.exp(-1 * sol[i] / 2)):
            features.append(1)
        else:
            features.append(0)

    return np.asarray(features).astype(bool)

# S4 Transfer Function
def s4(sol):
    features = []

    for i in range(sol.size):
        rand = r.generate_uniform_random_number()
        
        if rand < 1.0 / (1.0 + m.exp(-1 * sol[i] / 3)):
            features.append(1)
        else:
            features.append(0)

    return np.asarray(features).astype(bool)

# V1 Transfer Function
def v1(sol):
    features = []

    for _, aux in enumerate(sol):
        rand = r.generate_uniform_random_number()
        
        if rand < m.fabs(m.erf(m.sqrt(m.pi) / 2 * (-1 * aux))):
            features.append(1)
        else:
            features.append(0)

    return np.asarray(features).astype(bool)

# V2 Transfer Function
def v2(sol):
    features = []

    for _, aux in enumerate(sol):
        rand = r.generate_uniform_random_number()
        
        if rand < m.fabs(m.tanh(-1 * aux)):
            features.append(1)
        else:
            features.append(0)
    
    return np.asarray(features).astype(bool)

# V3 Transfer Function
def v3(sol):
    features = []

    for i in range(sol.size):
        rand = r.generate_uniform_random_number()
        
        if rand < m.fabs(-1 * sol[i] / m.sqrt(1 + (-1 * (sol[i] * sol[i])))):
            features.append(1)
        else:
            features.append(0)
    
    return np.asarray(features).astype(bool)

# V4 Transfer Function
def v4(sol):
    features = []

    for i in range(sol.size):
        rand = r.generate_uniform_random_number()
        
        if rand < m.fabs(2 / m.pi * m.atan(m.pi / 2 * (-1 * sol[i]))):
            features.append(1)
        else:
            features.append(0)

    return np.asarray(features).astype(bool)