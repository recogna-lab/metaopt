from celery_progress.backend import ProgressRecorder
from opytimizer.utils.callback import Callback


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