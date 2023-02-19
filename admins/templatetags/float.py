from django.template.defaulttags import register


@register.filter
def to_float(val):
    return float(val)
