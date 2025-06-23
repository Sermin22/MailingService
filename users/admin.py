from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# admin.site.register(CustomUser, UserAdmin)
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'phone_number',
        'is_active',
        'is_staff',
        'is_superuser',
        'avatar',
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
