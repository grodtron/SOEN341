from django import template

register = template.Library()

@register.inclusion_tag('shopping-cart/tags/add-button.html')
def shopping_cart_add_button(course_id):
    return {"id":course_id}

