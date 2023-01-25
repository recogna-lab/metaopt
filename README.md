# MetaOPT: A Python-based Web Application for Metaheuristics

This is a web application that employs metaheuristics in optimization and feature selection.

## How to use

After getting the source code, install the requirements:

```bash
python3 -m pip install -r requirements.txt
```

To run the project, use:

```bash
python3 manage.py runserver --insecure
```

Remember to apply the migrations with:

```bash
python3 manage.py migrate
```

To load data from the fixtures, use:

```bash
python3 manage.py loaddata optimizers.json
```

For running tasks, have redis-server up and execute:

```bash
celery --app metaopt worker -l debug
```
