import numpy as np
from opytimizer import Opytimizer
from opytimizer.core import Function
from opytimizer.spaces import SearchSpace

from metaopt.celery import app
from utils import delete_logs
from utils.tasks.callback import ProgressCallback
from utils.tasks.optimization import Result, get_function, get_optimizer


# This is the base class for the optimization task
class _OptimizationTask(app.Task):
    
    abstract = True
    
    def run_optimization(self, optimizer, function, space, agents, 
                         iterations, executions):
        # Create results object
        results = Result()
        
        # Save the number of executions
        self.executions = executions
        
        # Run the optimization method n times:
        for curr_exec in range(self.executions):
            np.random.seed(curr_exec)

            # Set progress description
            self.set_progress_description(curr_exec + 1)
            
            # Get best solution, best value and fitness values
            execution_data = self.optimize(
                optimizer, function, space, agents, iterations
            )
            
            # Update the results object
            results.update(result=execution_data)
        
        # Return the results object as a dict
        return results.as_dict()
    
    def set_progress_description(self, curr_exec):
        if self.executions > 1:
            self.progress_description = f'Execução {curr_exec}...'
        else:
            self.progress_description = None
    
    def optimize(self, optimizer, function, space, agents, iterations):
        # Set optimizer, function and search space
        self.setup(optimizer, function, space, agents)
        
        # Start the optimization
        self.start(iterations)
        
        # Get best solution, best value and fitness values        
        best_solution, best_value, fitness_values = self.get_result()
        
        # Return execution data 
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
        np.random.seed()
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
        progress_callback = self.get_progress_callback(total=iterations)
        
        # Start optimization
        self.opytimizer.start(
            n_iterations=iterations, 
            callbacks=[progress_callback]
        )
    
    def get_result(self):
        # Get best solution
        x =  self.opytimizer.space.best_agent.position.flatten().tolist()
        
        # Get best value
        y = self.opytimizer.space.best_agent.fit.item()
        
        # Get fitness values (for convergence plot)
        f = self.get_fitness_values()

        return x, y, f

    def get_fitness_values(self):
        _, f = self.opytimizer.history.get_convergence('best_agent')
        
        return f.tolist()
    
    def get_progress_callback(self, total):
        # Return progress callback instance
        return ProgressCallback(self, total, self.progress_description)
    
    def after_return(self, *args, **kwargs):
        # Delete logs created during the execution
        delete_logs()


# This is the optimization task
@app.task(name='optimization', base=_OptimizationTask, bind=True)
def optimization(self, user_id, optimizer, function, space, agents, 
                 iterations, executions):
    # Run the optimization task as specified by the following arguments
    return self.run_optimization(
        optimizer, 
        function, 
        space, 
        agents, 
        iterations,
        executions
    )