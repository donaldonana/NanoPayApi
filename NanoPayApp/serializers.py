from rest_framework import serializers

from NanoPayApp import models

      
class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer the user profile object"""

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        if self.context["request"].method == "PUT":
            self.fields.pop("password")
            self.fields.pop("phone")
            
            

    class Meta:

        model = models.UserProfile
        fields = ('id', 'phone', 'email', 'nom', 'prenom', 'dateDeNaissance', 'password', 'url', 'is_active', 
                  'is_staff', 'genre')
        extra_kwargs = {
            'password' : {
                'write_only' : True,
                'style' : {
                    'input_type' : 'password'
                }
            }, 
        }
   
class ChangePasswordSerializer(serializers.Serializer):
    model = models.UserProfile

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
class CustomAuthTokenSerializer(serializers.Serializer):
    model = models.UserProfile

    """
    Serializer for Obtain Token.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class CompteSerializer(serializers.ModelSerializer):
    """Serializer the user profile object"""
            

    class Meta:
        
        model = models.Compte
        fields = '__all__'
        
        extra_kwargs = {
            'user' : {
                'read_only' : True,
                
            }, 
        }
        
class TransactionSerializer(serializers.ModelSerializer):
    """Serializer the user profile object"""
            

    class Meta:
        
        model = models.Transaction
        fields = '__all__'
        
        extra_kwargs = {
            'compteEmetteur' : {
                'read_only' : True,
                
            }, 
            
        }
        
        
class ParametreCarteSerializer(serializers.ModelSerializer):
    """Serializer the user profile object"""
            

    class Meta:
        
        model = models.ParametreCarte
        fields = '__all__'
        
        
        