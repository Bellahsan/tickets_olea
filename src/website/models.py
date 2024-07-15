
# Create your models here.

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from shared.enum import RoleUtilisateur, StatutTicket

from ticketsolea import settings


class AuthGroup(Group):
    #
    libelle = models.CharField(max_length=150)
    code = models.CharField(max_length=50)


class User(AbstractUser):
    #
    role = models.CharField(max_length=50, choices=RoleUtilisateur.choices, default=RoleUtilisateur.ADMIN)
    groups = models.ManyToManyField(AuthGroup, related_name='website_users', blank=True, verbose_name='groups')
    user_permissions = models.ManyToManyField(Permission, related_name='website_users_permissions', blank=True, verbose_name='user permissions')

    def is_admin(self):
        return self.role == RoleUtilisateur.ADMIN

    def is_developer(self):
        return self.role == RoleUtilisateur.DEVELOPPER

    def is_client(self):
        return self.role == RoleUtilisateur.CLIENT

    def is_directeur(self):
        return self.role == RoleUtilisateur.DIRECTEUR

    def is_tester(self):
        return self.role == RoleUtilisateur.TESTEUR

    def is_expert_user(self):
        return self.role == RoleUtilisateur.EXPERT_USER

    def is_database_expert(self):
        return self.role == RoleUtilisateur.DATABASE_EXPERT


class TypeTicket(models.Model):
    #
    libelle = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.libelle

    class Meta:
        db_table = 'type_tickets'
        verbose_name = "Type de ticket"
        verbose_name_plural = "Types de tickets"


class Ticket(models.Model):
    #
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_tickets') # user qui cée la ticket
    code = models.CharField(max_length=10, unique=True) # code unique
    #
    type_ticket = models.ForeignKey(TypeTicket, on_delete=models.CASCADE, null=True, blank=True) # clé étranger vers model TypeTicket
    #
    title = models.CharField(max_length=200) # titre général
    description = models.TextField() # description
    attachments = models.FileField(upload_to='attachments/', blank=True, null=True) # attachements (image, fichier ect...)
    traite_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='tickets_traites', null=True, blank=True) # user qui traite la ticket
    status = models.CharField(max_length=50, choices=StatutTicket.choices, default=StatutTicket.ENATTENTE) # état de la ticket
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'ticket'
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"