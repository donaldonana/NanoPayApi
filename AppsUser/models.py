from django.db import models
from django.contrib.auth.models import AbstractBaseUser 
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from djongo import models
# from djangotoolbox.fields import EmbeddedModelField
from django.utils import timezone
import AppsComptes


# Create your models here.


class UserProfileManager(BaseUserManager):
    """manager for user profiles"""

    def create_user(self, 
        phone, 
        password ,
        code,
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
            code = code,
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
        code = None,
        nom = None,
        email = None,
        genre = None,
        prenom = None, 
        dateDeNaissance = None,):
        """create and save superuser with given detail"""
        user = self.create_user(nom = nom , 
            code = code,
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
    
    def CreateDefaultCompte(self, user):
        
        if len(user.compte_set.all()) == 0:
            nc = user.phone + '-01'

            c1 = AppsComptes.models.Compte(user = user, numCompte = nc)
            c1.nomCompte = user.get_full_name()
            params = AppsComptes.models.ParametreCarte()
            params.save()
            c1.parametre = params
            c1.save()
            user.compte_set.add(c1)
            user.save()
    

# class ObjectIdField(models.Field):
#     """docstring for ClassName"""
#     def __init__(self, *args, **kwargs):
       
        

class UserProfile(AbstractBaseUser, PermissionsMixin, models.Model):


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
    #id = models.PositiveIntegerField( blank = True, null= True)
    #_id = models.ObjectIdField(auto_created=True, unique=True, primary_key=True)
    #id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    nom = models.CharField(max_length=255, blank = True, null= True)
    code = models.CharField(max_length=20, blank = True, null= True)
    prenom = models.CharField(max_length=255, null= True, blank = True)
    phone = models.CharField(max_length=255, unique=True)
    dateDeNaissance = models.DateField(blank = True, null = True)
    genre = models.CharField(max_length=25, choices=Genre, blank = True, null= True)
    valide = models.BooleanField(default=False)
    contacts  = models.ManyToManyField('self', 
        symmetrical = False , 
        related_name = "contact", 
        blank = True)
    
    
    # abonnes   = models.ForeignKey('self', related_name = "abonne", on_delete=models.CASCADE, null = True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = "phone"

    REQUIRED_FIELDS = []

    def get_last_name(self):
        return self.nom
    
    def get_full_name(self):
        
        if self.nom and self.prenom:
            return self.nom + " " + self.prenom
        else:
            return
    


    





class Permissions(models.Model):
    emetteur = models.CharField(max_length=255)
    recepteur = models.CharField(max_length=255)
    comptes = models.CharField(max_length=255)
    
    class Meta:
        unique_together = ('emetteur', 'recepteur','comptes')
    
#-------------------------------------------------------------------------------------
    

