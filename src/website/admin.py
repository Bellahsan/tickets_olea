from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group, Permission
from .models import TypeTicket, Ticket

from admin_custom.admin import custom_admin_site

admin.site = custom_admin_site
admin.site.site_header = 'TICKETS OLEA'

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'last_name', 'first_name', 'is_active', 'is_superuser')
    list_filter = ('username', 'last_name', 'first_name', 'is_active', 'is_superuser')
    search_fields = ('username', 'is_active', 'is_superuser')
    list_per_page = 10
    inlines = []

    superuser_fieldsets = (
        (None, {"fields": ("username", "password", "first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    staff_fieldsets = (
        (None, {"fields": ("username", "password", "first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    superuser_add_fieldsets = (
        (None, {"fields": ("username", "password1", "password2", "first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    staff_add_fieldsets = (
        (None, {"fields": (
            "username", "password1", "password2", "first_name", "last_name", "email",
        )}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            if request.user.is_superuser:
                return self.superuser_add_fieldsets
            else:
                return self.staff_add_fieldsets

        if request.user.is_superuser:
            return self.superuser_fieldsets
        else:
            return self.staff_fieldsets

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.is_superuser:
            queryset = queryset
        else:
            queryset = queryset.filter(is_superuser=False)

        return queryset

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


class TypeTicketAdmin(admin.ModelAdmin):
    list_per_page = 5
    list_display = ('code', 'libelle', 'created_at', 'updated_at')
    list_filter = ('code', 'libelle',)
    search_fields = ('code',)


class TicketAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_filter = ('created_at', 'created_by', 'traite_par', 'status')
    list_display = ('code', 'title', 'description', 'created_at', 'created_by', 'traite_par', 'status')
    search_fields = ('code', 'title', 'description', 'created_at', 'created_by', 'traite_par', 'status')


admin.site.register(User, CustomUserAdmin)
admin.site.register(TypeTicket, TypeTicketAdmin)
admin.site.register(Ticket, TicketAdmin)
