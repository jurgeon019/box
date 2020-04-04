from django.db.models import Manager 



class ActiveManager(object):
    use_for_related_fields = True
    def all(self, *args, **kwargs):
        return super().get_queryset().filter(is_active=True)

class PostCommentManager(ActiveManager):
    pass 


class PostManager(ActiveManager):
    pass 


class PostCategoryManager(ActiveManager):
    pass 

