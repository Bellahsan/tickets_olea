# enum.py

from django.db import models

class RoleUtilisateur(models.TextChoices):
    ADMIN = "ADMIN"
    DEVELOPPER = "DEVELOPPER"
    CLIENT = "CLIENT"
    DIRECTEUR = "DIRECTEUR"
    TESTEUR = "TESTEUR"
    EXPERT_USER = "EXPERT USER"
    DATABASE_EXPERT = "EXPERT BASE DE DONNEES"


class StatutTicket(models.TextChoices):
    ENATTENTE = "EN ATTENTE"
    ENCOURS = "EN COURS"
    TRAITE = "TRAITÉ"
    CLOTURE = "CLÔTURÉ"
