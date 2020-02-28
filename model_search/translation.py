
from modeltranslation.translator import translator, TranslationOptions

from box.model_search.models import SearchTag


class SearchTagTranslationOptions(TranslationOptions):
    fields = ('text', )


translator.register(SearchTag, SearchTagTranslationOptions)
