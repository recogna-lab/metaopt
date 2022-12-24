from celery_progress.backend import ProgressRecorder
from opytimizer.utils.callback import Callback


# Create custom callback class for Opytimizer
class ProgressCallback(Callback):
    
    DEFAULT_DESCRIPTION = 'Tarefa em execução...'
    
    def __init__(self, task, total, description):
        # Create progress recorder associated with the task
        self.progress_recorder = ProgressRecorder(task)
        
        # Set the progress description
        self._set_description(description)
        
        # Save total number of iterations
        self.total = total
        
        super().__init__()
    
    def _set_description(self, description):
        if description is not None:
            self.description = description
        else:
            self.description = self.DEFAULT_DESCRIPTION
    
    # At the beginning of each iteration, record the progress
    def on_iteration_begin(self, curr_iteration, _):
        self.progress_recorder.set_progress(
            current=curr_iteration,
            total=self.total, 
            description=self.description
        )