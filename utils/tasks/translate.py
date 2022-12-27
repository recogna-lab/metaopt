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

def task_name_icontains(q):
    q = q.lower()
    
    # names that match condition
    names = ()
    
    if q in 'otimização':
        names = names + ('optimization', )
    
    if q in 'seleção':
        names = names + ('feature_selection', )
    
    return names

def status_icontains(q):
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

def optimizer_regex(search_term):
    # Define regex to find optimizer key inside json string
    # and check if search_term is part of the value
    optimizer_regex = r'.*"optimizer":\s"[A-Z]*{}[A-Z]*".*'
    return optimizer_regex.format(search_term.upper())

def function_regex(search_term):
    # Define regex to find function key inside json string
    # and check if search_term is part of the value
    function_regex = r'.*"function":\s"[a-zA-Z]*(?i){}[a-zA-Z0-9]*".*'
    return function_regex.format(search_term)

def dataset_regex(search_term):
    # Define regex to find dataset key inside json string
    # and check if search_term is part of the value
    dataset_regex = r'.*"dataset":\s"[a-zA-Z\s]*(?i){}[a-zA-Z\s]*".*'
    return dataset_regex.format(search_term)