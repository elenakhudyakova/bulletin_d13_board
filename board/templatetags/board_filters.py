from django import template

from board.models import Category

register = template.Library()


@register.filter()
def get_name(categories_dict: dict, pk: int):
    obj = categories_dict.get(pk, None)
    if obj:
        return obj.name
