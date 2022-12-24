import math as m

import numpy as np
import opfython.utils.exception as e
import opfython.utils.logging as log
import opytimizer.math.random as r

# Get logger for the feature selection task
logger = log.get_logger(__name__)


# Create a custom parser function based on 
# the function extracted from Opfython
def parse_loader(data):
    logger.info('Parsing data ...')

    try:
        # From third columns beyond, we should have the features
        X = data[:, 2:]

        # Second column should be the label
        Y = data[:, 1]

        # Calculate the amount of samples per class
        _, counts = np.unique(Y, return_counts=True)

        # If there is only one class
        if len(counts) == 1:
            logger.warning('Parsed data only have a single label.')

        # If there are unsequential labels
        if len(counts) != (np.max(Y)):
            raise e.ValueError('Parsed data should have sequential labels, e.g., 0, 1, ..., n-1')

        logger.info('Data parsed.')

        return X, Y.astype(int)
    except TypeError as error:
        logger.error(error)
        return None, None


# Define the Sigmoid function and some of its variations 
# used in feature selection problems; they are applied to 'sol', 
# which is the solution of an optimizer

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


# Get one of the available transfer functions through its name
def get_transfer_function(transfer_function):
    transfer_functions = globals()[transfer_function]
    return transfer_functions