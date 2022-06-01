from django.contrib import admin
from app_forum.models import News, Comments, Images


class NewsAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'created_at']
    list_filter = ['author', 'created_at']
    list_display_links = ['author', 'title', 'created_at']


class CommentsAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'text_comment', 'new']
    list_filter = ['user_name', 'new']
    list_display_links = ['user_name', 'text_comment', 'new']


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['news', 'image']
    list_display_links = ['news', 'image']


admin.site.register(News, NewsAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Images, ImagesAdmin)
