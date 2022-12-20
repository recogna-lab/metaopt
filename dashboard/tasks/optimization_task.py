import numpy as np
from opytimizer import Opytimizer
from opytimizer.core import Function
from opytimizer.optimizers.swarm import PSO
from opytimizer.spaces import SearchSpace

from metaopt.celery import app


class _OptimizationTask(app.Task):
    abstract = True
    
    def optimize(self, _optimizer, _function, _agents, _iterations):        
        optimizer = PSO()
        
        function = lambda x: np.sum(x ** 2)
        function = Function(function)
        
        agents = 10
        iterations = 10
        
        space = SearchSpace(
            n_agents=agents, 
            n_variables=2, 
            lower_bound=[-10, -10], 
            upper_bound=[10, 10]
        )

        opt = Opytimizer(space, optimizer, function)
        
        opt.start(n_iterations=iterations)
        
        # Get results
        optimum_value =  opt.space.best_agent.position.flatten().tolist()
        function_value = opt.space.best_agent.fit.item()

        # Get errors
        _, error_values = opt.history.get_convergence('best_agent')
        
        error_values = error_values.tolist()
        
        # Create output dict
        output = {
            'optimum_value': optimum_value,
            'function_value': function_value,
            'error_values': error_values
        }
        
        return output

@app.task(name='optimization', base=_OptimizationTask, bind=True)
def optimization(self, user_id, optimizer, function, agents, iterations):
    return self.optimize(optimizer, function, agents, iterations)