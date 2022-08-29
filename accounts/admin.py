from django.contrib import admin
from .models import Profile, User, UserSession

admin.site.register(Profile)
admin.site.register(User)
admin.site.register(UserSession)