const element = document.getElementById('id_dataset')
const infoElement = document.getElementById('load-info')
const renderInfo = document.getElementById('render-info')

const loadInfo = (info) => {
    if (info == ''){
        renderInfo.textContent = ''
        infoElement.classList.remove('mt-2')
        
    } else {
        renderInfo.textContent = info + ' características'
        infoElement.classList.add('mt-2')
    }
}

element.addEventListener('change', (event) => {
    loadInfo(event.target.value)
})
