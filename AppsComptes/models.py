from django.db import models
 
from djongo import models
from AppsUser.models import UserProfile, Permissions
from django.utils import timezone

class Compte(models.Model):
    
    TYPE = (
    ('professionnel', 'professionnel'),
    ('depense', 'depense')
    
    ) 
    
    numCompte = models.CharField(max_length = 25 , unique=True)
    nomCompte = models.CharField(max_length=25, blank=True, null = True)
    adresse = models.CharField(max_length=25, blank=True, null = True)
    principal  = models.BooleanField(default=True)
    solde = models.IntegerField(default=0)
    type = models.CharField(max_length=25, choices=TYPE, default="depense")  
    dateCreation = models.DateTimeField(default = timezone.now)
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
    )
    parametre = models.ForeignKey(
        'ParametreCarte',
        on_delete=models.CASCADE,
        blank=True, null = True
    )
    permissions = models.ManyToManyField(
        Permissions,
        blank=True, null = True
    )


class ParametreCarte(models.Model):
     
    active = models.BooleanField(default=False)
    PaiementQuotidientLimite = models.IntegerField(default=10)
    MontantPaimentQuotidient = models.IntegerField(default=10000)
    confirmationEnAttente = models.IntegerField(default=0)
    uid = models.CharField(max_length = 25 ,  blank=True, null=True)
    privatekey = models.CharField(max_length = 25 , blank=True, null=True)
    publickey = models.CharField(max_length = 25 , blank=True, null = True)
    nip = models.CharField(max_length = 25 , blank=True, null = True)
    initialized = models.BooleanField(default=False)