from django.template.defaulttags import register
from django.core.files.storage import default_storage

@register.filter
def is_file(image):
    return default_storage.exists(image)

