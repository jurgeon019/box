from .admin import * 

admin.site.register(Post, PostAdmin)
admin.site.register(PostMarker, PostMarkerAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(PostComment, PostCommentAdmin)
