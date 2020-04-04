from .admin import * 

admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(PostComment, PostCommentAdmin)
