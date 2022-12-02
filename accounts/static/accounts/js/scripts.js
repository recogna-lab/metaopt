$(function () {
    $('[data-toggle="tooltip"]').tooltip({placement: 'right'})
})

const showPassword = function() {
    const fields = []

    fields[0] = document.getElementsByName('password')[0]
    fields[1] = document.getElementsByName('confirm_password')[0]

    fields.forEach((field) => {
        if(field) {
            field.type = field.type == 'password' ? 'text' : 'password'
        }
    })
}