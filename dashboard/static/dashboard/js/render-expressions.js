// Get wrapper element
const wrapperElement = document.getElementById('expression-wrapper') 

// Get render expression element
const renderElement = document.getElementById('render-expression')

// Create function to render expressions
const renderExpression = (expression) => {
    if (expression == '') {
        // If no expression, remove class to wrapper
        wrapperElement.classList.remove('form-group')
    } else {
        // If it has expression, remove class to wrapper
        wrapperElement.classList.add('form-group')
    }

    // Place the value in the render element
    renderElement.textContent = expression
    
    // Render the expression
    MathJax.startup.promise.then(() => {
        MathJax.typesetClear([renderElement])
        MathJax.typeset([renderElement])
    })
}

// Get function select
let selectElement = document.getElementById('id_function')

// If it has no function select
if (!selectElement) {
    // Get the transfer function select instead
    selectElement = document.getElementById('id_transfer_function')
}

// Create listener to detect changes in the select element
selectElement.addEventListener('change', (event) => {
    if (window.MathJax) {
        renderExpression(event.target.value)
    }
})







