import json

from metaopt.celery import app


@app.task(name='dummy_task', bind=True)
def dummy_task(self, user_id, message):
    output = f"Dummy task says: {message}!"
    
    return {
        'output':  output,
    }