from celery import shared_task


@shared_task(bind=True)
def dummy_task(self, message):
    print(f'I\'m a dummy celery task: {message}!')