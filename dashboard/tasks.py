import json
import time

from celery import signals, states
from celery_progress.backend import ProgressRecorder
from django_celery_results.models import TaskResult

from metaopt.celery import app


@app.task(name='optimization', bind=True)
def optimization(self, user_id, optimizer, function, agents, iterations):
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
        'output':  output,
    }


@signals.before_task_publish.connect
def create_pending_task(headers=None, body=None, **kwargs):
    # Check if there is a task obj in headers
    if 'task' not in headers:
        return
    
    hostname = headers['origin'].split('@')[1]
    
    # Create task with status=PENDING
    TaskResult.objects.store_result(
        content_encoding = 'utf-8',
        content_type = 'application/json',
        task_id=headers['id'],
        status = states.PENDING,
        result = None,
        task_name = headers['task'],
        task_args = json.dumps(headers['argsrepr']),
        task_kwargs = json.dumps(headers['kwargsrepr']),
        worker = f'celery@{hostname}'
    )