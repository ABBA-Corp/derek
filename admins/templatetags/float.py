from django.template.defaulttags import register


@register.filter
def to_floatt(val):
    return float(val)
