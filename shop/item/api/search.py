import re
from django.db.models import Q
from django.conf import settings 


def filter_search(items, query):
    search_query = query.get('q')
    if search_query:
        search_query = search_query.lower()
        # for f in settings.SEARCH_FIELDS:
        #   items = items.filter(**{f'{f}__icontains':search_query})
        # items = items.filter(
        #     # Q(title__icontains=search_query) |
        #     # Q(description__icontains=search_query) | 
        #     # Q(code__icontains=search_query) #|
        #     Q(**{'code__icontains':search_query}) #|
        # ).distinct()
        entry_query = get_query(search_query, [f for f in settings.SEARCH_FIELDS])
        items = items.filter(entry_query)
    return items


def normalize_query(query_string):
    normspace = re.compile(r'\s{2,}').sub
    findterms = re.compile(r'"([^"]+)"|(\S+)').findall
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 


def get_query(query_string, search_fields):
    query = None 
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None 
        for field_name in search_fields:
            q = Q(**{f"{field_name}__icontains": term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


