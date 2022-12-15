from metaopt.celery import app


@app.task(name='optimization', bind=True)
def optimization(self, user_id, optimizer, function, agents, iterations):
    output = f'Runnning {optimizer} for {iterations} iterations!'
    
    return {
        'output':  output,
    }