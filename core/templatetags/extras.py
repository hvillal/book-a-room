from django import template

register = template.Library()


@register.filter(name='total_price')
def total_price(price, nights):
    return price * nights
