$(function() {
    const elements = $('[data-bs-toggle="tooltip"]')
    let elementsArray = [...elements]

    elementsArray.forEach((e) => {
        if(e.classList.contains('tooltip-left')) {
            $(e).tooltip({placement: 'left'})
        } else {
            $(e).tooltip({placement: 'right'})
        }
    })
})

const showPassword = function() {
    // First, let's change the input type
    const fields = []

    fields[0] = document.getElementsByName('password')[0]
    fields[1] = document.getElementsByName('confirm_password')[0]

    fields.forEach((field) => {
        if(field) {
            field.type = field.type == 'password' ? 'text' : 'password'
        }
    })

    // Now, let's change the button text
    const button = document.getElementById('show-btn')

    if(button.textContent.trim() == 'Mostrar senha') {
        button.textContent = 'Esconder senha'
    } else {
        button.textContent = 'Mostrar senha'
    }
}