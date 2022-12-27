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


# Get all tasks that contain a certain word
def filter_tasks(user_id, search_term):
    # Get task_id of all tasks that belong to the user
    user_tasks = UserTask.objects.filter(user__id=user_id)
    user_tasks = user_tasks.values_list('task__task_id')

    # Get the task information using task ids
    tasks = TaskResult.objects.filter(task_id__in=user_tasks)
    tasks = tasks.order_by('-date_created')
    
    # Select the desired fields in a dict
    tasks = select_task_fields(tasks)
    
    # Create query variables (with query that has no matches)
    opt_query = Q(task_name='batman')
    selection_query = Q(task_name='batman')
    status_query = Q(task_name='batman')
    
    # If term contains optimization letters, add opt tasks
    if translate.icontains_optimization(search_term):
        opt_query = Q(task_name='optimization')
    
    # If term contains selection letters, add fs tasks
    if translate.icontains_selection(search_term):
        selection_query = Q(task_name='feature_selection')
    
    # Get tuple with status that contains search term
    status = translate.icontains_status(search_term)
    status_query = Q(status__in=status)
    
    # Define regex to find optimizer substring and check search term
    optimizer_regex = r'.*"optimizer":\s"[a-zA-Z]*{}[a-zA-Z]*".*'
    optimizer_regex = optimizer_regex.format(search_term.upper())
    
    # Create optimizer query
    optimizer_query = Q(task_kwargs__regex=optimizer_regex)
    
    # Filter tasks using the search word
    filtered_tasks = tasks.filter(
        Q(
            opt_query |
            selection_query |
            status_query |
            optimizer_query
        )
    )
    
    for task in filtered_tasks:
        task = format_task(task)
    
    return filtered_tasks

# Get all tasks via user task
def get_all_tasks(user_id):
    # Get user_tasks with user_id
    user_tasks = UserTask.objects.filter(user__id=user_id)
    
    # Get the task_id from all of the user tasks
    user_tasks = user_tasks.values_list('task__task_id')
    
    # Get the task information from the tasks with matching id
    tasks = TaskResult.objects.filter(task_id__in=user_tasks)
    tasks = tasks.order_by('-date_created')

    # Select the desired fields in a dict
    tasks = select_task_fields(tasks)
    
    # Format tasks
    for task in tasks:
        task = format_task(task)
    
    # Return formatted tasks
    return tasks

# Get a single task via user task
def get_task(user_id, task_id):
    try:
        # Check if user owns the task
        UserTask.objects.get(
            user__id=user_id, 
            task__task_id=task_id
        )
        
        # Get task information
        task = TaskResult.objects.filter(
            task_id=task_id
        )
        
        # Select the desired fields in a dict
        task = select_task_fields(task)
        
        # Return formatted task
        return format_task(task=task.first())
    except UserTask.DoesNotExist:
        return None

def select_task_fields(task_qs):
    # Select the desired values
    return task_qs.values(
        'task_id',
        'task_name',
        'task_kwargs',
        'status',
        'result',
        'date_created',
        'date_done'        
    )

# Format task before getting it
def format_task(task):
    task['task_name'] = translate.task_name(task['task_name'])
    task['status'] = translate.task_status(task['status'])
    task['task_kwargs'] = load_json(task['task_kwargs'])

    if task['result'] is not None:
        task['result'] = load_json(task['result'])
    
    return task

def get_dataset_info(filename):
    try:
        return Dataset.objects.get(file_name = filename)
    except Dataset.DoesNotExist:
        return None

def get_all_datasets_names():
    try:
        return Dataset.objects.all()
    except Dataset.DoesNotExist:
        return None


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