from django.template.defaulttags import register


@register.filter
def cut_text(strng):
    if strng is None:
        return '--'

    if len(str(strng)) > 50:
        return strng[:50] + '...'
    
    return strng

