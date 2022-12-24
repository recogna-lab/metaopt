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
    
    def update(self, x, y, f):
        if self.best_solution is None:
            self._initialize(x, y, f)
        else:
            self._update(x, y, f)
    
    def _initialize(self, x, y, f):
        self.best_solution = np.array(x)
        self.fitness_values = np.array(f)
        
        self.best_value = y
        self.min_value = y
        self.max_value = y
        
        self.values = [y]
        
        self.exec_data = [
            self._get_exec_dict(x, y, f)
        ]
    
    def _update(self, x, y, f):
        self.best_solution += np.array(x)
        self.fitness_values += np.array(f)
        
        self.best_value += y
        self.min_value = min(self.min_value, y)
        self.max_value = max(self.max_value, y)
        
        self.values.append(y)
        
        self.exec_data.append(
            self._get_exec_dict(x, y, f)
        )
    
    def _get_exec_dict(self, x, y, f):
        return {
            'best_solution': x,
            'best_value': y,
            'fitness_values': f
        }
    
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