from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (('Дополнительная информация', {
        'fields': ('avatar', 'bio', 'phone_number', 'gender'),
        }),)
    list_display = ('username', 'email', 'first_name', 'is_staff')
