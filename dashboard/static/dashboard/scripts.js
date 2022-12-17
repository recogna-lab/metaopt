const initializeProgressBar = (progressURL) => {
    const defaultBarColors = {
        success: '#76ce60',
        progress: '#68a9ef',
        error: '#dc4f63'
    }

    const defaultPBarMessages = {
        waiting: 'Esperando a tarefa iniciar...',
        started: 'Tarefa iniciando...'
    }

    const onProgress = (pBarElement, pBarMessageElement, progress) => {
        pBarElement.style.backgroundColor = defaultBarColors.progress
        pBarElement.style.width = progress.percent + '%'

        let description = progress.description || ''
        
        if (progress.current == 0) {
            if (progress.pending === true) {
                pBarMessageElement.textContent = defaultPBarMessages.waiting
            } else {
                pBarMessageElement.textContent = defaultPBarMessages.started
            }
        } else {
            pBarMessageElement.textContent = progress.current + ' de ' +
                progress.total + ' iterações. ' + description
        }
    }

    const onError = (pBarElement, pBarMessageElement, exception, _) => {
        pBarElement.style.backgroundColor = defaultBarColors.error
        pBarMessageElement.textContent = 'Algo deu errado! Recarregue ' + 
            'a página ou execute a tarefa novamente.'
        
        // exception = exception || ''
        // console.log(exception)
    }

    const onRetry = (pBarElement, pBarMessageElement, exception, retryWhen) => {
        pBarElement.style.backgroundColor = defaultBarColors.error
        
        retryWhen = new Date(retryWhen);
        retryWhen = Math.round((retryWhen.getTime() - Date.now())/1000)

        pBarMessageElement.textContent = 'Algo deu errado! Reexecutando ' +
            'tarefa em ' + retryWhen + ' segundos'
        
        // exception = exception || ''
        // console.log(exception)
    }

    const onSuccess = (pBarElement, pBarMessageElement, _) => {
        pBarElement.style.backgroundColor = defaultBarColors.success
        pBarMessageElement.textContent = 'Tarefa concluída com sucesso!'
    }

    document.addEventListener('DOMContentLoaded', function () {
        CeleryProgressBar.initProgressBar(progressURL, {
            progressBarMessageId: 'progress-bar-status',
            defaultMessages: defaultPBarMessages,
            onProgress: onProgress,
            onError: onError,
            onRetry: onRetry,
            onSuccess: onSuccess
        })
    })
}