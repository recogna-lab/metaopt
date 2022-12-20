import json

from celery import signals, states
from django_celery_results.models import TaskResult

from .optimization_task import optimization


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