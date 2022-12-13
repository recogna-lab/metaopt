from metaopt.celery import app


@app.task(name='dummy_task', bind=True)
def dummy_task(self, user_id, message):
    output = f"I'm a dummy celery task: {user_id}!"
    print(output) 
    return output