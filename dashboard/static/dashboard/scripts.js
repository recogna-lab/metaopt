const initializeProgressBar = (progressURL) => {
    const defaultPBarMessages = {
        waiting: 'Esperando a tarefa iniciar...',
        started: 'Tarefa iniciando...'
    }

    const onProgress = (pBarElement, pBarMessageElement, progress) => {
        pBarElement.style.backgroundColor = '#68a9ef' 
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

    document.addEventListener('DOMContentLoaded', function () {
        CeleryProgressBar.initProgressBar(progressURL, {
            progressBarMessageId: 'progress-bar-status',
            defaultMessages: defaultPBarMessages,
            onProgress: onProgress
        })
    })
}