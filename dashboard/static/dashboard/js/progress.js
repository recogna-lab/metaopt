const initializeProgressBar = (progressURL, resultURL) => {
    // Create custom pbar colors
    const defaultBarColors = {
        success: '#76ce60',
        progress: '#68a9ef',
        error: '#dc4f63'
    }

    // Create custom pbar messages
    const defaultPBarMessages = {
        waiting: 'Esperando a tarefa iniciar...',
        started: 'Tarefa iniciando...'
    }

    // Function that will be executed during progress
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

    // Function that will be executed when an error happens
    const onError = (pBarElement, pBarMessageElement, exception, _) => {
        pBarElement.style.backgroundColor = defaultBarColors.error

        if (exception == 'Task terminated') {
            pBarMessageElement.textContent = 'A tarefa foi cancelada.'
        } else {
            pBarMessageElement.textContent = 'Algo deu errado! Recarregue ' + 
                'a página ou execute a tarefa novamente.'
        }
    }

    const onTaskError = (pBarElement, pBarMessageElement, exception) => {
        onError(pBarElement, pBarMessageElement, exception)
    }

    // Function that will be executed when retry happens
    const onRetry = (pBarElement, pBarMessageElement, exception, retryWhen) => {
        pBarElement.style.backgroundColor = defaultBarColors.error
        
        retryWhen = new Date(retryWhen);
        retryWhen = Math.round((retryWhen.getTime() - Date.now())/1000)

        pBarMessageElement.textContent = 'Algo deu errado! Reexecutando ' +
            'tarefa em ' + retryWhen + ' segundos'
    }

    // Function that will be executed when success happens
    const onSuccess = (pBarElement, pBarMessageElement, _) => {
        pBarElement.style.backgroundColor = defaultBarColors.success
        pBarMessageElement.textContent = 'Tarefa concluída com sucesso!'
    }
    
    // Function that will be executed to show the results
    const onResult = (resultElement, result) => {
        // Hide the revoke button if necessary
        hideRevokeButton()

        // If task was terminated, exit function
        if (result == 'Task terminated') {
            return
        }
        
        // Extract result
        const [first, second, third] = extractResults(result)

        // Create HTML table with result
        resultHTML = `
            <table class="table table-sm striped table-nowrap">
                <thead>
                    <tr>
                        <th class="th-sm"></th>
                        <th class="th-sm"></th>     
                    </tr>
                </thead>
                <tbody>
                    <tr class="col-sm">
                        <th scope="row" class="sm">${first.label}</th>
                        <td>${first.value}</td>
                    </tr>
        `

        if (result.best_features_vector){
            resultHTML +=`
                    <tr class="col-sm">
                        <th scope="row" class="sm">${third.label}</th>
                        <td>${third.value}</td>
                    </tr>
            `
        }

        resultHTML += `
                    <tr class="col-sm">
                        <th scope="row" class="sm">${second.label}</th>
                        <td>${second.value}</td>
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

    const hideRevokeButton = () => {
        // Get revoke button
        const revokeButton = document.getElementById('revoke_task')

        // Hide it, there's no reason to show it anymore
        if (revokeButton) {
            revokeButton.style.display = 'none'
        }
    }

    // Helper function to extract results
    const extractResults = (result) => {
        let first = {}
        let second = {}
        let third = {}

        if (result.best_features_vector) {
            first.label = 'Melhor vetor de características'
            first.value = formatBooleanArray(result.best_features_vector)

            second.label = 'Melhor acurácia'
            second.value = formatNumber(result.best_acc)  
            
            third.label = 'Quantidade selecionada'
            third.value = result.number_of_features

        } else {
            first.label = 'Melhor solução'
            first.value = formatArray(result.best_solution)

            second.label = 'Melhor valor da função'
            second.value = formatNumber(result.best_value)
        }

        return [first, second, third]
    }

    const formatBooleanArray = (arr) => {
        let output = '['

        for (let i = 0; i < arr.length; i++) {
            output += arr[i].toString()

            if (i != arr.length - 1) {
                output += ', '
            }
        }

        return output + ']'
    }
    
    // Helper function to format number
    const formatNumber = (number) => {
        number = number.toLocaleString('pt-br', options={
            minimumFractionDigits: 3, 
            maximumFractionDigits: 3
        })

        return number
    }

    // Helper function to format array
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
    
    // When DOM content is already loaded, initialize pbar
    document.addEventListener('DOMContentLoaded', function () {
        // Initialize celery pbar
        CeleryProgressBar.initProgressBar(progressURL, {
            progressBarMessageId: 'progress-bar-status',
            resultElementId: 'task-result',
            defaultMessages: defaultPBarMessages,
            pollInterval: 400,
            onProgress: onProgress,
            onError: onError,
            onTaskError: onTaskError,
            onRetry: onRetry,
            onSuccess: onSuccess,
            onResult: onResult
        })
    })
}