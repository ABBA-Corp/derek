from django.template.defaulttags import register


@register.filter
def to_float(val):
    if ',' in str(val):
        return str(val).replace(',', '.')
    else:
        return val
