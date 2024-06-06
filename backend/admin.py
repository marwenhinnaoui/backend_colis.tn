from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from rest_framework.authtoken.admin import TokenAdmin
from rest_framework.authtoken.models import Token

class CustomUserAdmin(UserAdmin):
    search_fields = ('email',)

class CustomTokenAdmin(TokenAdmin):
    search_fields = ('user__email',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Token, CustomTokenAdmin)