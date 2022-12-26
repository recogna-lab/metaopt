const initializeProgressBar = (progressURL, resultURL) => {
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
        
        // If necessary, use the lines above to see the problem
        // exception = exception
        // console.log(exception)
    }

    const onRetry = (pBarElement, pBarMessageElement, exception, retryWhen) => {
        pBarElement.style.backgroundColor = defaultBarColors.error
        
        retryWhen = new Date(retryWhen);
        retryWhen = Math.round((retryWhen.getTime() - Date.now())/1000)

        pBarMessageElement.textContent = 'Algo deu errado! Reexecutando ' +
            'tarefa em ' + retryWhen + ' segundos'
        
        // If necessary, use the lines above to see the problem
        // exception = exception
        // console.log(exception)
    }

    const onSuccess = (pBarElement, pBarMessageElement, _) => {
        pBarElement.style.backgroundColor = defaultBarColors.success
        pBarMessageElement.textContent = 'Tarefa concluída com sucesso!'
    }
    
    const onResult = (resultElement, result) => {
        bestSolution = formatArray(result.best_solution)
        bestValue = formatNumber(result.best_value)

        resultHTML = `
            <table class="table table-striped table-nowrap">
                <thead>
                    <tr>
                        <th class="th-sm"></th>
                        <th class="th-sm"></th>     
                    </tr>
                </thead>
                <tbody>
                    <tr class="col-sm">
                        <th scope="row" class="sm">Melhor solução</th>
                        <td>${bestSolution}</td>
                    </tr>
                    <tr class="col-sm">
                        <th scope="row" class="sm">Melhor valor da função</th>
                        <td>${bestValue}</td>
                    </tr>
                </tbody>
            </table>
            
            <div class="a-right p-t-15">
                <a href="${resultURL}" class="btn btn-basic btn-success btn-radius">
                    Ver mais
                </a>
            </div>
        `

        resultElement.innerHTML = resultHTML
    }

    const formatNumber = (number) => {
        number = number.toLocaleString('pt-br', options={
            minimumFractionDigits: 3, 
            maximumFractionDigits: 3
        })

        return number
    }

    const formatArray = (arr) => {
        let output = '['

        for (let i = 0; i < arr.length; i++) {
            let formattedNumber = formatNumber(arr[i])
            
            output += formattedNumber

            if (i != arr.length - 1) {
                output += '; '
            }
        }

        return output + ']'
    }
    
    document.addEventListener('DOMContentLoaded', function () {
        CeleryProgressBar.initProgressBar(progressURL, {
            progressBarMessageId: 'progress-bar-status',
            resultElementId: 'task-result',
            defaultMessages: defaultPBarMessages,
            pollInterval: 400,
            onProgress: onProgress,
            onError: onError,
            onRetry: onRetry,
            onSuccess: onSuccess,
            onResult: onResult
        })
    })
}