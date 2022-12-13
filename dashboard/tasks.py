from metaopt.celery import app


@app.task(name='optimization', bind=True)
def optimization(self, user_id, message):
    output = f"Optimization task says: {message}!"
    
    return {
        'output':  output,
    }

@app.task(name='feature_selection', bind=True)
def feature_selection(self, user_id, message):
    output = f"Feature Selection task says: {message}!"
    
    return {
        'output':  output,
    }