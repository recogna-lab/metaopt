import json
import time

from celery import signals, states
from celery_progress.backend import ProgressRecorder
from django_celery_results.models import TaskResult

from metaopt.celery import app


@app.task(name='optimization', bind=True)
def optimization(self, user_id, optimizer, function, agents, iterations):
    progress_recorder = ProgressRecorder(self)
    
    # Loop up to 10 sleeping 1 s in each iteration (simulated execution)
    for i in range(20):
        time.sleep(1)
        progress_recorder.set_progress(i + 1, 20)
        
    # Save the output
    output = f'I ran {optimizer} for {iterations} iterations!'
    
    # Return result dict
    return {
        'output':  output,
    }