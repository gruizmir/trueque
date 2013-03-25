from django import template
register = template.Library()

@register.filter('mod')
def mod(value, arg):
    if value % arg == 0:
        return True
    else:
        return False