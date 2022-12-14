from metaopt.celery import app


@app.task(name='optimization', bind=True)
def optimization(self, user_id, message):
    output = f'Optimization task says: {message}!'
    
    return {
        'output':  output,
    }