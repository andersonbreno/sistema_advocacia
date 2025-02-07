from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})

@register.filter(name='attr')
def attr(obj, attr_name):
    """Retorna o valor de um atributo do objeto"""
    return getattr(obj, attr_name, '')
