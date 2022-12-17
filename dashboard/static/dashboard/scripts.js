const initializeProgressBar = (progressURL) => {
    const defaultProgressBarMessages = {
        waiting: 'Esperando a tarefa iniciar...',
        started: 'Tarefa iniciando...'
    }

    document.addEventListener('DOMContentLoaded', function () {
        CeleryProgressBar.initProgressBar(progressURL, {
            defaultMessages: defaultProgressBarMessages
        })
    })
}