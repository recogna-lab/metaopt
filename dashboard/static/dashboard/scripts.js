const initializeProgressBar = (progressURL) => {
    const defaultBarColors = {
        success: '#76ce60',
        progress: '#68a9ef'
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

    const onSuccess = (pBarElement, pBarMessageElement, _) => {
        pBarElement.style.backgroundColor = defaultBarColors.success
        pBarMessageElement.textContent = 'Tarefa concluída com sucesso!'
    }

    document.addEventListener('DOMContentLoaded', function () {
        CeleryProgressBar.initProgressBar(progressURL, {
            progressBarMessageId: 'progress-bar-status',
            defaultMessages: defaultPBarMessages,
            onProgress: onProgress,
            onSuccess: onSuccess
        })
    })
}