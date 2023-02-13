from admins.models import Languages, Translations


def translator(word: str, lang: str = None):
    if lang:
        lng_code = lang
    else:
        lng_code = Languages.objects.filter(active=True).filter(default=True).first().code

    
    for lng in Languages.objects.filter(active=True):
        trarnsl = Translations.objects.filter(value__contains=f"{ lng.code }:{ word }")
        if trarnsl.exists():
            translation = trarnsl.first().value.get(lng_code)

            return translation

    
    