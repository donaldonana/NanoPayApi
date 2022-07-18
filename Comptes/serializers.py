from rest_framework import fields, serializers
from django.contrib.auth import authenticate

from Comptes import models
import NanoPayApp







class CreateCompteSerializer(serializers.Serializer):
    
    TYPE = (
    ('professionnel', 'professionnel'),
    ('depense', 'depense')
    
    ) 
    telephone = serializers.CharField(max_length = 25 )
    nomCompte = serializers.CharField()
    type = serializers.ChoiceField(choices = TYPE)
    adresse = serializers.CharField(max_length=25, required = False)

    class Meta :
        ref_name = "Compte"
        
        extra_kwargs = {'adresse': {'required': False}} 



class ParametreCarteSerializer(serializers.ModelSerializer):
    """Serializer the user profile object"""
            
    class Meta:
        ref_name = "Compte"
        
        model = models.ParametreCarte
        fields = '__all__'

        
class PermissionsSerializer(serializers.ModelSerializer):
    """Serializer the user profile object"""
            
    class Meta:
        ref_name = "Compte"

        model = models.UserProfile
        fields = ('nom', 'phone')

        

class CompteSerializer(serializers.ModelSerializer):
    """Serializer the user profile object"""
            
   
    
    class Meta:
        model = models.Compte
        ref_name = "Compte"

        fields = ('id', 'numCompte', 'nomCompte', 'principal', 'solde', 'type', 'adresse',
                  'dateCreation', 'user')
        
        
        extra_kwargs = {
            'user' : {
                'read_only' : True,
                
            }, 
        }

class CompteViewSerializer(serializers.ModelSerializer):
    """Serializer the user profile object"""
            
    parametre = ParametreCarteSerializer(read_only = True)
    permissions = NanoPayApp.serializers.PermissionsChangeSerializer(read_only = True, many = True)
    
    
    class Meta:
        model = models.Compte
        # ref_name = "Compte"

        fields = ('id', 'numCompte', 'nomCompte', 'principal', 'solde', 'type', 'adresse',
                  'dateCreation', 'user', 'parametre', 'permissions')
        
        
        extra_kwargs = {
            'user' : {
                'read_only' : True,
                
            }, 
        }
  
        

class ToggleCompteSerializer(serializers.ModelSerializer):    
    class Meta:
        model = models.Compte
        fields = ('numCompte',)  
        extra_kwargs = {'numCompte': {'required': True}}    


class QuotidientLimiteSerializer(serializers.ModelSerializer): 
    valeurLimite = serializers.IntegerField()
    class Meta:
        model = models.Compte
        fields = ('numCompte','valeurLimite')  
        extra_kwargs = {'numCompte': {'required': True}, 'valeurLimite': {'required': True}}  


class PlafondLimiteSerializer(serializers.ModelSerializer): 
    valeurPlafond = serializers.IntegerField()
    class Meta:
        model = models.Compte
        fields = ('numCompte','valeurPlafond')  
        extra_kwargs = {'numCompte': {'required': True}, 'valeurPlafond': {'required': True}}  


class CarteInitSerializer(serializers.ModelSerializer): 
    numCompte = serializers.CharField()
    class Meta:
        model =  models.ParametreCarte
        fields = '__all__'  
        extra_kwargs = {'numCompte': {'required': True},
                        'nip' : {'required': True}, 
                        'uid' : {'required': True},
                        'privatekey' : {'required': True},
                        'publickey' : {'required': True},
                        }  
        read_only_fields = ('active','PaiementQuotidientLimite','MontantPaimentQuotidient', 
            'confirmationEnAttente', 'initialized')



        