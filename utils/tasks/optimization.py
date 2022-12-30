from statistics import stdev

import numpy as np
from opytimark.markers.n_dimensional import *
from opytimizer.optimizers.evolutionary import *
from opytimizer.optimizers.science import *
from opytimizer.optimizers.swarm import *


# This helper class holds the results from multiple executions 
# of an optimization method
class Result:
    
    def __init__(self):
        # Just to know if result was not initialized
        self.fitness_values = None
    
    def update(self, result):
        if self.fitness_values is None:
            self._initialize(result)
        else:
            self._update(result)
    
    def _initialize(self, result):
        self.fitness_values = np.array(result['fitness_values'])
        
        self.best_solution = result['best_solution']
        self.values = [result['best_value']]
        
        self.exec_data = [result]
    
    def _update(self, result):
        self.fitness_values = np.vstack(
            (self.fitness_values, result['fitness_values'])
        )
        
        self.values.append(result['best_value'])
        
        if min(self.values) == result['best_value']:
            self.best_solution = result['best_solution']
        
        self.exec_data.append(result)
    
    def as_dict(self):
        # Get the number of executions
        count = len(self.exec_data)
        
        # Create var for avg and in case count == 1, add fitness list
        avg_fitness_values = self.fitness_values.tolist()
        
        # Create var for std and set it to None
        stdev_fitness_values = None
        
        # If there's more than one execution, compute stdev
        if count > 1:
            avg_fitness_values = np.average(self.fitness_values, axis=0)
            avg_fitness_values = avg_fitness_values.tolist()
            
            stdev_fitness_values = np.std(self.fitness_values, axis=0)
            stdev_fitness_values = stdev_fitness_values.tolist()
        
        # Add average values to results dict
        # Remeber that standard deviation requires count > 1
        results_dict = {
            'best_solution': self.best_solution,
            'best_value': min(self.values),
            'avg_value': sum(self.values) / count,
            'max_value': max(self.values),
            'stdev_value': stdev(self.values) if count > 1 else None,
            'fitness_values': avg_fitness_values,
            'stdev_fitness_values': stdev_fitness_values
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
def get_function(function, dimension):
    function_class = globals()[function]
    return function_class(dims=dimension)