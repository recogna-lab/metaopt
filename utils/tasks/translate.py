def task_name(name):
    if name == 'optimization':
        name = 'Otimização'
    elif name == 'feature_selection':
        name = 'Seleção de Características'
    
    return name

def task_status(status):
    if status == 'SUCCESS':
        status = 'Sucesso'
    elif status == 'FAILURE':
        status = 'Falha'
    elif status == 'PROGRESS':
        status = 'Em Progresso'
    
    return status