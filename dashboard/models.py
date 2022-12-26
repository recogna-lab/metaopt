from ast import literal_eval

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django_celery_results.models import TaskResult

from utils import dump_json, load_json
from utils.tasks import translate


class Optimizer(models.Model):
    
    acronym = models.CharField(
        max_length=10,
        verbose_name='Acronym',
        help_text='Short name for the optimizer'
    )
    
    name = models.CharField(
        max_length=50,
        verbose_name='Name',
        help_text='Name of the optimizer'
    )
    
    def __str__(self):
        return f'{self.name} ({self.acronym})'
    
    class Meta:
        ordering = ('name', )

class Function(models.Model):
    
    short_name = models.CharField(
        max_length=50,
        verbose_name='Short Name',
        help_text='Short name for the function'
    )
    
    name = models.CharField(
        max_length=50,
        verbose_name='Name',
        help_text='Name of the function'
    )
    
    latex_expression = models.CharField(
        max_length=255,
        verbose_name='Latex Expression',
        help_text='Latex expression for the function'
    )
    
    search_space = models.TextField(
        verbose_name='Search Space',
        help_text='JSON representation of the search space'
    )
    
    optimal_result = models.TextField(
        verbose_name='Optimal Result',
        help_text='JSON representation of the optimal result'
    )
    
    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        ordering = ('name', )

class Dataset(models.Model):
    
    name = models.CharField(
        max_length=50,
        verbose_name='Name',
        help_text='Name of the dataset'
    )

    file_name = models.CharField(
        max_length=50,
        verbose_name='File Name',
        help_text='File name of the dataset'
    )

    features = models.IntegerField(
        verbose_name='Features',
        help_text='Number of features of the dataset'
    )
    
    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        ordering = ('name', )

class TransferFunction(models.Model):

    name = models.CharField(
        max_length=50,
        verbose_name='Name',
        help_text='Name of the Transfer Function'
    )
    
    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        ordering = ('name', )

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
    
    class Meta:
        ordering = ('-task__date_created', )


def get_dataset_info(filename):
    try:
        dataset = Dataset.objects.get(file_name = filename)

        print(dataset)

        return dataset

    except Dataset.DoesNotExist:
        return None

def get_all_datasets_names():

    try:
        dataset = Dataset.objects.all()
        return dataset
    
    except Dataset.DoesNotExist:
        return None

# Get a single task via user task
def get_task(user_id, task_id):
    try:
        UserTask.objects.get(
            user__id=user_id, 
            task__task_id=task_id
        )
        
        task = TaskResult.objects.get(
            task_id=task_id
        )
        
        return format_task(task=task)
    except UserTask.DoesNotExist:
        return None

# Get all tasks via user task
def get_all_tasks(user_id):
    user_tasks = UserTask.objects.filter(user__id=user_id)
    user_tasks = user_tasks.values_list('task__task_id')
    
    tasks = TaskResult.objects.filter(task_id__in=user_tasks)
    tasks = tasks.order_by('-date_created')
    
    for task in tasks:
        task = format_task(task)
    
    return tasks

# Get all tasks that contain a certain word
def get_tasks_filter(user_id, search):
    user_tasks = UserTask.objects.filter(user__id=user_id)
    user_tasks = user_tasks.values_list('task__task_id')

    tasks = TaskResult.objects.filter(task_id__in=user_tasks)
    tasks = tasks.order_by('-date_created')
    tasks_filtered = tasks.filter(
        Q(
            Q(task_name__icontains = search) |
            Q(status__icontains = search) |
            Q(task_kwargs__icontains = search)
        )
    )

    for task in tasks_filtered:
        task = format_task(task)

    return tasks_filtered
    
# Format task before getting it
def format_task(task):
    task.task_name = translate.task_name(task.task_name)
    task.status = translate.task_status(task.status)
    task.task_kwargs = load_json(task.task_kwargs)

    if task.result is not None:
        task.result = load_json(task.result)
    
    return task

# Before saving a task result instance
@receiver(pre_save, sender=TaskResult)
def format_task_kwargs(sender, instance, **kwargs):        
    # Retrieve task named arguments as dict 
    task_kwargs_dict = literal_eval(instance.task_kwargs)
    task_kwargs_dict = task_kwargs_dict.replace('\'', '"')
    task_kwargs_dict = load_json(task_kwargs_dict)

    # Correctly save named arguments as json 
    instance.task_kwargs = dump_json(task_kwargs_dict)

# After saving a task result instance
@receiver(post_save, sender=TaskResult)
def save_user_task(sender, instance, created, **kwargs):
    # Return if instance already existed before save
    if not created:
        return

    # Retrieve task named arguments
    task_kwargs_dict = load_json(instance.task_kwargs)
    
    # Get the user id
    user_id = task_kwargs_dict['user_id']

    # Retrieve the user and save it with the task
    user = User.objects.filter(pk=user_id).first()
    user_task = UserTask(user=user, task=instance)
    user_task.save()