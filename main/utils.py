from admins.models import Languages, Translations
from .serializers import BasedModelSerializer

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

    
# search for api
def search_func(query, queryset, fields):
    if query == '':
        return queryset

    langs = Languages.objects.filter(active=True)
    query_str = ''
    if langs.exists():
        for lang in langs:
            query_str += f'"$.{lang.code}",'

        end_set = set()
        for field in fields:
            qs = queryset.extra(where=[f'LOWER({field} ::varchar) LIKE %s'], params=[f'%{query.lower()}%'])
            for item in qs:
                end_set.add(item)

        return list(end_set)
                

    return []
                
        