import numpy as np
from celery_progress.backend import ProgressRecorder
from opytimizer import Opytimizer
from opytimizer.core import Function
from opytimizer.optimizers.swarm import PSO
from opytimizer.spaces import SearchSpace
from opytimizer.utils.callback import Callback

from metaopt.celery import app


class _OptimizationTask(app.Task):
    abstract = True
    
    def optimize(self, _optimizer, _function, _agents, _iterations):
        # Set optimizer    
        optimizer = PSO()
        
        # Set cost function
        function = lambda x: np.sum(x ** 2)
        function = Function(function)
        
        # Set number of agents and iterations
        agents = 10
        iterations = 10
        
        # Create search space
        space = SearchSpace(
            n_agents=agents, 
            n_variables=2, 
            lower_bound=[-10, -10], 
            upper_bound=[10, 10]
        )
        
        # Create Opytimizer instance
        opytimizer = Opytimizer(space, optimizer, function)
        
        # Create progress callback
        progress_callback = self.create_progress_callback(total=iterations)
        
        # Start optimization
        opytimizer.start(n_iterations=iterations, callbacks=[progress_callback])
        
        # Get optimum value and function on optimum
        optimum_value =  opytimizer.space.best_agent.position.flatten().tolist()
        function_value = opytimizer.space.best_agent.fit.item()

        # Get errors (for convergence plot)
        _, error_values = opytimizer.history.get_convergence('best_agent')
        
        error_values = error_values.tolist()
        
        # Add results and errors to the output        
        return {
            'optimum_value': optimum_value,
            'function_value': function_value,
            'error_values': error_values
        }

    def create_progress_callback(self, total):
        # Create custom callback class for Opytimizer
        class ProgressCallback(Callback):
            
            def __init__(self, task, total):
                # Create progress recorder associated with the task
                self.progress_recorder = ProgressRecorder(task)
                
                # Save total number of iterations
                self.total = total
                
                super().__init__()
            
            # At the beginning of each iteration, record the progress
            def on_iteration_begin(self, curr_iteration, _):
                self.progress_recorder.set_progress(
                    current=curr_iteration,
                    total=self.total, 
                    description='Tarefa em execução...'
                )

        # Return custom callback instance
        return ProgressCallback(self, total)

@app.task(name='optimization', base=_OptimizationTask, bind=True)
def optimization(self, user_id, optimizer, function, agents, iterations):
    return self.optimize(optimizer, function, agents, iterations)