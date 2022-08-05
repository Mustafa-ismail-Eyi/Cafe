from django import template
register = template.Library()
@register.filter
def get_by_index(l, i):
    return l[i]

@register.filter
def get_foods(l,i):
    return [foods for foods in l if foods.order_id.id==i]