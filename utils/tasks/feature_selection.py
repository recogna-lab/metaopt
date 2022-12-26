import math as m
from statistics import stdev

import numpy as np
import opfython.utils.exception as e
import opfython.utils.logging as log
import opytimizer.math.random as r
from utils.tasks.optimization import Result

# Get logger for the feature selection task
logger = log.get_logger(__name__)


class ResultFS(Result):
    def __init__(self):
        super().__init__()

    def update(self, result):
        if self.best_solution is None:
            self._initialize(result)
        else:
            self._update(result)

    def _initialize(self, result):
        super()._initialize(result)

        self.precision = np.array(result['precision'])
        self.recall = np.array(result['recall'])
        self.f1_score = np.array(result['f1_score'])

        self.acc_values = [result['accuracy']]
        self.bsf_list = [result['best_selected_features']]
    
    def _update(self, result):
        super()._update(result)

        self.bsf_list.append(result['best_selected_features'])
        self.acc_values.append(result['accuracy'])

        self.precision += np.array(result['precision'])
        self.recall += np.array(result['recall'])
        self.f1_score += np.array(result['f1_score'])

    def as_dict(self):
        # Get the number of executions
        count = len(self.exec_data)

        best_acc_index = self.acc_values.index(max(self.acc_values))
        
        # Add average values to results dict
        # Remeber that standard deviation requires count > 1
        results_dict = {
            'best_solution': (self.best_solution / count).tolist(),
            'best_value': sum(self.values) / count,
            'min_value': min(self.values),
            'max_value': max(self.values),
            'stdev_value': stdev(self.values) if count > 1 else None,
            'fitness_values': (self.fitness_values / count).tolist(),
            'best_features_vector': self.bsf_list[best_acc_index],
            'accuracy': sum(self.acc_values) / count,
            'min_acc': min(self.acc_values),
            'max_acc': max(self.acc_values),
            'stdev_acc': stdev(self.acc_values) if count > 1 else None,
            'precision': (self.precision / count).tolist(),
            'recall': (self.recall / count).tolist(),
            'f1_score': (self.f1_score / count).tolist()
        }
        
        # If it has more than one execution
        if count > 1:
            # For each execution
            for i in range(count):
                # Save execution data to results dict
                k = f'exec_{i + 1}'
                results_dict[k] = self.exec_data[i]
        
        # Return results dict
        return results_dict

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