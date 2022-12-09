from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_results.models import TaskResult


class UserTask(models.Model):

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    
    task = models.OneToOneField(
        TaskResult, 
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.user} {self.task}' 

@receiver(post_save, sender=TaskResult)
def save_user_task(sender, instance, **kwargs):
    # Get the user with id = 1 only for testing
    user = User.objects.filter(pk=1).first()
    
    user_task = UserTask(user=user, task=instance)
    user_task.save()