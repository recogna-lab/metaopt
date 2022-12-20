import time

from celery_progress.backend import ProgressRecorder

from metaopt.celery import app


class _OptimizationTask(app.Task):
    abstract = True
    
    def optimize(self, optimizer, function, agents, iterations):
        progress_recorder = ProgressRecorder(self)
    
        # Loop up to 50 sleeping 1 s in each iteration (simulated execution)
        for i in range(50):
            time.sleep(1)
            
            progress_recorder.set_progress(
                current=i + 1, 
                total=50, 
                description='Tarefa em execução...'
            )
            
        # Save the output
        output = f'I ran {optimizer} for {iterations} iterations!'
        
        # Return result dict
        return {
            'output':  output
        }

@app.task(name='optimization', base=_OptimizationTask, bind=True)
def optimization(self, user_id, optimizer, function, agents, iterations):
    return self.optimize(optimizer, function, agents, iterations)