from django import template

register = template.Library()

@register.filter
def format_cpf(value):
    if value and len(value) == 11:
        return f"{value[:3]}.{value[3:6]}.{value[6:9]}-{value[9:]}"
    return value



from django import template

register = template.Library()

MESES_PT = {
    "January": "Janeiro",
    "February": "Fevereiro",
    "March": "Março",
    "April": "Abril",
    "May": "Maio",
    "June": "Junho",
    "July": "Julho",
    "August": "Agosto",
    "September": "Setembro",
    "October": "Outubro",
    "November": "Novembro",
    "December": "Dezembro"
}

@register.filter
def traduzir_mes(value):
    return MESES_PT.get(value, value)


@register.filter
def dict(d, key):
    return d.get(key, '')