from modeltranslation.translator import (
    translator, TranslationOptions, register
)
from box.blog.models import *


# @register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = (
        "meta_title",
        "meta_descr",
        "meta_key",
        "title",
        "content",
        "slug",  
        "alt",
    )



# @register(Post)
class PostCategoryTranslationOptions(TranslationOptions):
    fields = (
        "meta_title",
        "meta_descr",
        "meta_key",
        "title",
        "content",
        "slug",  
        "alt",
    )




 