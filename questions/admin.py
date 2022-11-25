from django.contrib import admin

from .models import *


class QuestionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    fields = ['title', 'slug', 'content', 'tags', 'author', 'likes', 'dislikes', 'created_at', 'modified_at']
    readonly_fields = ('created_at', 'modified_at')


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}
    fields = ['name', 'slug']


admin.site.register(MyUser)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Comment)
admin.site.register(Tag, TagAdmin)
