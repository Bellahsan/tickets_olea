from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from website.models import CustomUser
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin



class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'linkedin_url', 'profile_image', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'role', 'linkedin_url', 'profile_image')}),  # Include profile image here
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'linkedin_url', 'profile_image'),  # Include profile image here
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)


class CustomAdminSite(admin.AdminSite):
    index_template = 'admin/index.html'

    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        return super(CustomAdminSite, self).index(request, extra_context)

custom_admin_site = CustomAdminSite(name='custom_admin')
custom_admin_site.register(CustomUser, CustomUserAdmin)
custom_admin_site.register(Group, GroupAdmin) 