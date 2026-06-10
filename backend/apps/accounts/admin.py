from django.contrib import admin

from .models import Role, User, UserRole

admin.site.register(Role)
admin.site.register(User)
admin.site.register(UserRole)
