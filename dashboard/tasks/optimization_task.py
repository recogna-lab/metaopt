from opytimizer import Opytimizer
from opytimizer.core import Function
from opytimizer.spaces import SearchSpace

from metaopt.celery import app
from utils import delete_logs
from utils.benchmark_functions import get_function
from utils.callbacks import ProgressCallback
from utils.optimizers import get_optimizer


class _OptimizationTask(app.Task):
    
    abstract = True
    
    def optimize(self, optimizer, function, space, agents, iterations):
        # Set optimizer, function and search space
        self.setup(optimizer, function, space, agents)
        
        # Start the optimization
        self.start(iterations)
        
        # Get optimum value and function on optimum
        best_solution, best_value = self.get_results()
        
        # Get fitness values (for convergence plot)
        fitness_values = self.get_fitness_values()
        
        # Add results and fitness values to the output        
        return {
            'best_solution': best_solution,
            'best_value': best_value,
            'fitness_values': fitness_values
        }
        
    def setup(self, optimizer, function, space, agents):
        # Get and set the optimizer object    
        self.optimizer = get_optimizer(optimizer)
        
        # Get the function object
        function = get_function(function)
        
        # Set the cost function
        self.function = Function(function)
        
        # Configure the search space
        self.setup_space(agents, space)
    
    def setup_space(self, agents, space):
        # Create search space
        self.space = SearchSpace(
            n_agents=agents,
            n_variables=space['dimension'],
            lower_bound=space['lower_bound'],
            upper_bound=space['upper_bound']
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

    def get_fitness_values(self):
        _, f = self.opytimizer.history.get_convergence('best_agent')
        
        return f.tolist()
    
    def after_return(self, *args, **kwargs):
        # Delete logs created during the execution
        delete_logs()

@app.task(name='optimization', base=_OptimizationTask, bind=True)
def optimization(self, user_id, optimizer, function, space, agents, iterations):
    return self.optimize(optimizer, function, space, agents, iterations)