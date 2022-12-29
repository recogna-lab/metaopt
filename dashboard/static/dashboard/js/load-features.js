// Get wrapper element
const infoElement = document.getElementById('load-info')

// Get element where information will be loaded
const renderInfo = document.getElementById('render-info')

// Create function to load dataset info
const loadInfo = (info) => {
    if (info == ''){
        renderInfo.textContent = ''
        infoElement.classList.remove('mt-2')
        
    } else {
        renderInfo.textContent = info + ' características'
        infoElement.classList.add('mt-2')
    }
}

// Get dataset select element
const datasetSelect = document.getElementById('id_dataset')

// If it has the select element
if (datasetSelect) {
    // Add listener to detect changes
    datasetSelect.addEventListener('change', (event) => {
        // Load new info on change
        loadInfo(event.target.value)
    })
}
