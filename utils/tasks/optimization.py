from opytimark.markers.two_dimensional import *
from opytimizer.optimizers.evolutionary import *
from opytimizer.optimizers.science import *
from opytimizer.optimizers.swarm import *


# This helper class holds the results from multiple executions 
# of an optimization method
class Result:
    
    def __init__(self):
        self.x = None
        self.y = None
        self.f = None
        
        self.exec_data = None
    
    def update(self, x, y, f):
        if self.x is None:
            self._initialize(x, y, f)
        else:
            self._update(x, y, f)
    
    def _initialize(self, x, y, f):
        self.x = x
        self.y = y
        self.f = f
        
        self.exec_data = [
            self._get_exec_dict(x, y, f)
        ]
    
    def _update(self, x, y, f):
        self.x += x
        self.y += y
        self.f += f
        
        self.exec_data.append(
            self._get_exec_dict(x, y, f)
        )
    
    def _get_exec_dict(self, x, y, f):
        return {
            'best_solution': x.tolist(),
            'best_value': y.item(),
            'fitness_values': f.tolist()
        }
    
    def as_dict(self):
        # Get the number of executions
        count = len(self.exec_data)
        
        # Add average values to results dict
        results_dict = {
            'best_solution': (self.x / count).tolist(),
            'best_value': (self.y / count).item(),
            'fitness_values': (self.f / count).tolist()
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