from django import template
from decimal import Decimal, InvalidOperation

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

@register.filter(name='br_money')
def br_money(value):
    """
    Formata um número como R$ no padrão brasileiro.
    Exemplo: 1234.56 -> 1.234,56
    """
    try:
        if value is None or value == "":
            return "0,00"

        if isinstance(value, str):
            value = value.strip().replace(".", "").replace(",", ".")

        valor = Decimal(value).quantize(Decimal("0.01"))
        return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    except (ValueError, TypeError, InvalidOperation) as e:
        print(f"⚠️ Erro em br_money: {e} | Valor recebido: {value}")
        return "0,00"

@register.filter
def get_dict_value(d, key):
    return d.get(key, '')
