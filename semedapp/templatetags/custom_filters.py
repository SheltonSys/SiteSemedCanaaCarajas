from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr_name):
    return getattr(obj, attr_name, None)


@register.filter
def get_item(dictionary, key):
    """
    Retorna o valor de um dicionário para uma chave específica.
    """
    return dictionary.get(key, '')
