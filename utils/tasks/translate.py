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
        status = 'Progresso'
    elif status == 'PENDING':
        status = 'Pendente'
    
    return status

def icontains_optimization(q):
    return True if q.lower() in 'otimização' else False

def icontains_selection(q):
    return True if q.lower() in 'seleção' else False

def icontains_status(q):
    q = q.lower()
    
    # Status that match condition
    status = ()
    
    if q in 'sucesso':
        status = status + ('SUCCESS', )
    elif q in 'falha':
        status = status + ('FAILURE', )
    elif q in 'progresso':
        status = status + ('PROGRESS', )
    elif q in 'pendente':
        status = status + ('PENDING', )
    
    return status