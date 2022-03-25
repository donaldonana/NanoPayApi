from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from djongo import models
# from djangotoolbox.fields import EmbeddedModelField
from django.utils import timezone

# Create your models here.


class UserProfileManager(BaseUserManager):
    """manager for user profiles"""

    def create_user(self, 
        phone, 
        password ,
        nom = None,
        email = None,
        genre = None,
        prenom = None, 
        dateDeNaissance = None,
        ):
        """create the new user profile"""
        if not phone:
            raise ValueError("User most have a phone number")

       # email = self.normalize_email(email)
        user = self.model(
            nom = nom , 
            phone = phone, 
            email = email,
            genre = genre,
            prenom = prenom,
            dateDeNaissance = dateDeNaissance,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, 
        phone, 
        password ,
        nom = None,
        email = None,
        genre = None,
        prenom = None, 
        dateDeNaissance = None,):
        """create and save superuser with given detail"""
        user = self.create_user(nom = nom , 
            phone = phone, 
            email = email,
            genre = genre,
            prenom = prenom,
            dateDeNaissance = dateDeNaissance,
            password = password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):


    TYPE = (

    ('lecteur', 'Lecteur'),
    ('auteur', 'Auteur'),
    ('visiteur', 'Visiteur'),
    ('admin', 'Admin'),

    ) 
    
    Genre = (
        ('masculin', 'Masculin'),
        ('feminin', 'Feminin')
    )

    email = models.EmailField(max_length=255, unique=True, blank = True, null= True)
    nom = models.CharField(max_length=255, blank = True, null= True)
    prenom = models.CharField(max_length=255, null= True, blank = True)
    phone = models.CharField(max_length=255, unique=True)
    dateDeNaissance = models.DateField(blank = True, null = True)
    genre = models.CharField(max_length=25, choices=Genre, blank = True, null= True)
    
    
    # abonnes   = models.ForeignKey('self', related_name = "abonne", on_delete=models.CASCADE, null = True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = "phone"

    REQUIRED_FIELDS = []

    def get_last_name(self):

        return self.nom
    

class Compte(models.Model):
    
    TYPE = (
    ('entrprise', 'Entreprise'),
    ('personel', 'Personel')
    ) 
    
    numCompte = models.IntegerField(unique=True)
    nomCompte = models.CharField(max_length=25,blank=True)
    principal  = models.BooleanField()
    solde = models.IntegerField()
    type = models.CharField(max_length=25, choices=TYPE)
    dateCreation = models.DateTimeField(default = timezone.now)
    user = models.ForeignKey(
        'UserProfile',
        on_delete=models.CASCADE,
    )
    params = models.ForeignKey(
        'ParametreCarte',
        on_delete=models.CASCADE,
    )
    
    
class Transaction(models.Model):
    
    dateHeure = models.DateTimeField(default = timezone.now)
    montant = models.IntegerField()
    compteEmetteur = models.ForeignKey(
        'UserProfile',
        related_name="emetteur",
        on_delete=models.CASCADE,
    )
    compteRecepteur  = models.ForeignKey(
        'UserProfile',
        related_name="recepteur",
        on_delete=models.CASCADE,
    )
    
class ParametreCarte(models.Model):
    paiementVerouiller = models.BooleanField()
    PaiementQuotidientLimite = models.IntegerField()
    MontantPaimentQuotidient = models.IntegerField()