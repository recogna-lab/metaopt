from metaopt.celery import app


@app.task(name='dummy_task', bind=True)
def dummy_task(self, message):
    output = f"I'm a dummy celery task: {message}!"
    print(output) 
    return output