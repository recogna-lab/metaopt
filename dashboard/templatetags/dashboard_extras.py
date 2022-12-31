from django import template

register = template.Library()

def format_list(values, precision):
    format_string = f'{{0:.{precision}f}}'
    
    formatted_list = [format_string.format(x) for x in values]
    formatted_list = '; '.join(formatted_list)
    formatted_list = formatted_list.replace('.', ',')
    
    return f'[{formatted_list}]'

def replace(values, arg):

    current, new = arg.split('|')
    return str(values).replace(current, new)

register.filter('listformat', format_list)
register.filter('replace', replace)
