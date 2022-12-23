def translate_task_name(task_name):
    if task_name == 'optimization':
        task_name = 'Otimização'
    elif task_name == 'feature_selection':
        task_name = 'Seleção de Características'
    
    return task_name

def translate_task_status(status):
    if status == 'SUCCESS':
        status = 'Sucesso'
    elif status == 'FAILURE':
        status = 'Falha'
    elif status == 'PROGRESS':
        status = 'Em Progresso'
    
    return status