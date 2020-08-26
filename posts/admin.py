from django.contrib import admin

from .models import Post, Group, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "pub_date", "author")
    search_fields = ("text",)
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"


class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "author",)
    search_fields = ("text",)
    empty_value_display = "-Как он это сделал?-"


admin.site.register(Group)
admin.site.register(Comment, CommentAdmin)

admin.site.register(Post, PostAdmin)
