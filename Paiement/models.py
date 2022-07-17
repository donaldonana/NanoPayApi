from django.db import models
 
from djongo import models
from NanoPayApp.models import UserProfile
from Comptes.models import Compte
from django.utils import timezone

 

# Create your models here.


class Transaction(models.Model):

    TYPE = (
    ('Paiement', 'Paiement'),
    ('Transfert', 'Transfert'),
    ('Facture', 'Facture')

    
    ) 
    
    senderPhone = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
         related_name = "sender"
    )
    senderNumCompte = models.ForeignKey(
        Compte,
        on_delete=models.CASCADE,
    )
    receiverPhone = models.ForeignKey(
        UserProfile,
        to_field='phone',
        on_delete=models.CASCADE,
    )
    type = models.CharField(max_length=25, choices=TYPE, default="depense")  
    DateTransaction = models.DateTimeField(default = timezone.now)
    montant = models.IntegerField()
   


class WaitingTransactions(models.Model):

    TYPE = (
    ('Paiement', 'Paiement'),
    ('Transfert', 'Transfert'),
    ('Facture', 'Facture')

    
    ) 
    
    senderPhone = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
         related_name = "Waitsender"
    )
    senderNumCompte = models.ForeignKey(
        Compte,
        on_delete=models.CASCADE,
    )
    receiverPhone = models.ForeignKey(
        UserProfile,
        to_field='phone',
        on_delete=models.CASCADE,
    )
    type = models.CharField(max_length=25, choices=TYPE, default="depense")  
    DateTransaction = models.DateTimeField(default = timezone.now)
    montant = models.IntegerField()