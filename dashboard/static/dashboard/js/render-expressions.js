// Get function select
const selectElement = document.getElementById('id_function')
        
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

// Create listener to detect changes in the select element
selectElement.addEventListener('change', (event) => {
    renderExpression(event.target.value)
})