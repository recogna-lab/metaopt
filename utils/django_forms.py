from re import compile

from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()

def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)

def strong_password(password):
    regex = compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    
    if not regex.match(password):
        raise ValidationError(
            (
                'A senha deve conter pelo menos uma letra maiúscula, '
                'uma letra minúscula e um dígito numérico. No mais, a senha '
                'deve conter pelo menos 8 caracteres.'
            ),
            code='invalid'
        )