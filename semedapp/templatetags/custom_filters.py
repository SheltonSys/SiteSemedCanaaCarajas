from django import template
from decimal import Decimal, InvalidOperation
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

register = template.Library()

@register.filter
def get_attr(obj, attr_name):
    return getattr(obj, attr_name, None)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, '')

@register.filter
def sub(value, arg):
    return value - arg

@register.filter
def br_money(value):
    try:
        # Se None ou vazio, trata como zero
        if value in [None, '', 'None']:
            value = Decimal('0.00')
        elif not isinstance(value, Decimal):
            # Substitui vírgula por ponto se necessário
            value_str = str(value).replace(",", ".")
            value = Decimal(value_str)

        # Quantize para duas casas decimais
        value = value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Formatar para o padrão brasileiro
        valor_formatado = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {valor_formatado}"
    except (InvalidOperation, TypeError, ValueError):
        return "R$ 0,00"

@register.filter
def get_dict_value(d, key):
    return d.get(key, '')
