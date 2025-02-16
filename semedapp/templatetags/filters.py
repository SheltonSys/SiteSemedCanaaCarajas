from django import template

register = template.Library()

@register.filter
def format_cpf(value):
    if value and len(value) == 11:
        return f"{value[:3]}.{value[3:6]}.{value[6:9]}-{value[9:]}"
    return value
