from django.contrib import admin
from .models import User, AuthGroup, TypeTicket, Ticket

# Register your models here.


@admin.register(AuthGroup)
class AuthGroupAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'code')
    search_fields = ('libelle', 'code')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    search_fields = ('username', 'email', 'role')


@admin.register(TypeTicket)
class TypeTicketAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'code', 'created_at', 'updated_at')
    search_fields = ('libelle', 'code')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'created_by', 'status', 'created_at')
    search_fields = ('code', 'title', 'created_by__username')
    list_filter = ('status', 'type_ticket', 'created_by')