from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea 
from .models import *

# Register your models here.
class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'username', 'first_name',)
    list_filter = ('email', 'username', 'first_name', 'is_active', 'is_staff')
    ordering = ('-date_joined',)
    list_display = ('email', 'email_verified', 'profile', 'username', 'first_name', 'last_name', 'display',
                    'is_active', 'is_staff', 'date_joined', 'last_login')
    fieldsets = (
        (None, {'fields': ('profile', 'email', 'username', 'first_name','last_name','password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'role', 'position', 'display', 'email_verified')}),
        ('Personal', {'fields': ('bio',)}),
    )
    formfield_overrides = {
        User.bio: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('profile', 'email', 'first_name', 'last_name', 'bio', 'role', 'position', 'display', 'username', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
         ),
    )

admin.site.register(User, UserAdminConfig)

admin.site.register(WebInfo)