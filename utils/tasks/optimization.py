from statistics import stdev

import numpy as np
from opytimark.markers.two_dimensional import *
from opytimizer.optimizers.evolutionary import *
from opytimizer.optimizers.science import *
from opytimizer.optimizers.swarm import *


# This helper class holds the results from multiple executions 
# of an optimization method
class Result:
    
    def __init__(self):
        # Just to know if result was not initialized
        self.best_solution = None
    
    def update(self, result):
        if self.best_solution is None:
            self._initialize(result)
        else:
            self._update(result)
    
    def _initialize(self, result):
        self.best_solution = np.array(result['best_solution'])
        self.fitness_values = np.array(result['fitness_values'])
        
        self.best_value = result['best_value']
        self.min_value = result['best_value']
        self.max_value = result['best_value']
        
        self.values = [result['best_value']]
        
        self.exec_data = [result]
    
    def _update(self, result):
        self.best_solution += np.array(result['best_solution'])
        self.fitness_values += np.array(result['fitness_values'])
        
        self.best_value += result['best_value']
        self.min_value = min(self.min_value, result['best_value'])
        self.max_value = max(self.max_value, result['best_value'])
        
        self.values.append(result['best_value'])
        
        self.exec_data.append(result)
    
    def as_dict(self):
        # Get the number of executions
        count = len(self.exec_data)
        
        # Add average values to results dict
        # Remeber that standard deviation requires count > 1
        results_dict = {
            'best_solution': (self.best_solution / count).tolist(),
            'best_value': self.best_value / count,
            'min_value': self.min_value,
            'max_value': self.max_value,
            'stdev_value': stdev(self.values) if count > 1 else None,
            'fitness_values': (self.fitness_values / count).tolist()
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


# Get optimizer class through its acronym 
def get_optimizer(optimizer):
    optimizer_class = globals()[optimizer]
    return optimizer_class()


# Get function class through its short name 
def get_function(function):
    function_class = globals()[function]
    return function_class()