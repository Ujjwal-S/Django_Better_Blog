from django.contrib import admin
from .models import *

class BlogAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ['title',]}
	class Media:
		js = ('tinyInject.js',)
		

admin.site.register(Blog, BlogAdmin)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Bookmark)
admin.site.register(Opinion)
