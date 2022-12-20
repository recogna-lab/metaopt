import numpy as np
from opytimizer import Opytimizer
from opytimizer.core import Function
from opytimizer.optimizers.swarm import PSO
from opytimizer.spaces import SearchSpace

from metaopt.celery import app
from utils.callbacks import ProgressCallback


class _OptimizationTask(app.Task):
    abstract = True
    
    def optimize(self, optimizer, function, agents, iterations):
        # Set optimizer, function and search space
        self.setup(optimizer, function, agents)
        
        # Start the optimization
        self.start(iterations)
        
        # Get optimum value and function on optimum
        optimum_value, function_value = self.get_results()
        
        # Get errors (for convergence plot)
        error_values = self.get_errors()
        
        # Add results and errors to the output        
        return {
            'optimum_value': optimum_value,
            'function_value': function_value,
            'error_values': error_values
        }
        
    def setup(self, optimizer, function, agents):
        # Set optimizer    
        self.optimizer = PSO()
        
        # Set cost function
        self.function = Function(lambda x: np.sum(x ** 2))
        
        # Create search space
        self.space = SearchSpace(
            n_agents=agents, 
            n_variables=2, 
            lower_bound=[-10, -10], 
            upper_bound=[10, 10]
        )
    
    def start(self, iterations):
        # Create Opytimizer instance
        self.opytimizer = Opytimizer(self.space, self.optimizer, self.function)
        
        # Create progress callback
        progress_callback = self.create_progress_callback(total=iterations)
        
        # Start optimization
        self.opytimizer.start(
            n_iterations=iterations, 
            callbacks=[progress_callback]
        )
    
    def create_progress_callback(self, total):
        # Return progress callback instance
        return ProgressCallback(self, total)
    
    def get_results(self):
        x =  self.opytimizer.space.best_agent.position.flatten().tolist()
        y = self.opytimizer.space.best_agent.fit.item()
        
        return x, y

    def get_errors(self):
        _, e = self.opytimizer.history.get_convergence('best_agent')
        
        return e.tolist()
        
@app.task(name='optimization', base=_OptimizationTask, bind=True)
def optimization(self, user_id, optimizer, function, agents, iterations):
    return self.optimize(optimizer, function, agents, iterations)