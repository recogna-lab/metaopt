# metaopt - Metaheuristic Optimization App

This is a web app for running metaheuristic optimization tasks.

## Reminders

To run the project, use:

```bash
python3 manage.py runserver --insecure
```

For the tasks, have redis-server up and run:

```bash
celery --app metaopt worker -l info
```