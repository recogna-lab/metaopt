from django.shortcuts import render


def custom_page_not_found(request, exception):
    response = render(request, 'global/pages/error.html', context={
        'status_code': 404,
        'error_type': 'Página não encontrada',
        'error_message': (
            'Você pode ter digitado incorretamente o endereço da página.'
        )
    })
    response.status_code = 404
    return response

def custom_server_error(request):
    response = render(request, 'global/pages/error.html', context={
        'status_code': 500,
        'error_type': 'Erro interno no servidor',
        'error_message': (
            'A página não pode ser exibida. Há um erro de execução no servidor.'
        )
    })
    response.status_code = 500
    return response

def custom_permission_denied(request, exception):
    response = render(request, 'global/pages/error.html', context={
        'status_code': 403,
        'error_type': 'Acesso negado',
        'error_message': (
            'Você não possui permissão para acessar essa página.'
        )
    })
    response.status_code = 403
    return response

def custom_bad_request(request, exception):
    response = render(request, 'global/pages/error.html', context={
        'status_code': 400,
        'error_type': 'Requisição incorreta',
        'error_message': (
            'O servidor não conseguiu atender sua requisição.'
        )
    })
    response.status_code = 400
    return response

def custom_csrf_failure(request, reason):
    response = render(request, 'global/pages/error.html', context={
        'status_code': 403,
        'error_type': 'Verificação CSRF falhou',
        'error_message': (
            'O envio do formulário não pôde ser feito de modo seguro. '
            'Tente realizar a operação novamente.'
        )
    })
    response.status_code = 403
    return response