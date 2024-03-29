from rest_framework import fields, serializers
from django.contrib.auth import authenticate

from AppsUser import models
from AppsComptes.models import Compte, ParametreCarte

class UserSerializer(serializers.ModelSerializer):
     
    class Meta :
        model = models.UserProfile
        fields = ('id', 'phone', "code", "password")
        read_only_fields = ('code',)
        
        extra_kwargs = {
            'password' : {
                'write_only' : True,
                'style' : {
                    'input_type' : 'password'
                }
            }, 
        }
    def create(self, validated_data):
        """create the return new user"""
        
        code = "12356"
        print(validated_data)
        user = models.UserProfile.objects.create_user(
            phone =  validated_data['phone'],
            password = validated_data['password'],
            code = code
        )
        
        return user


class UserDeleteSerializer(serializers.Serializer):
    
    telephone = serializers.CharField(max_length = 25 )

class UserCodeSerializer(serializers.ModelSerializer):
    
    class Meta :
        model = models.UserProfile
        fields = ('phone', 'code')
        extra_kwargs = {'code': {'required': True}} 
   
class UserInfoSerializer(serializers.ModelSerializer):
    
    class Meta :
        model = models.UserProfile
        fields = ('id', 'phone', 'nom', 'prenom', 'dateDeNaissance',
                  'genre')

        extra_kwargs = {'nom': {'required': True}, 'prenom': {'required': True}, } 
        
        
    
    def update(self, instance, validated_data):
        models.UserProfile.objects.CreateDefaultCompte(instance)
        return super().update(instance, validated_data)
        


class UserLoginSerializer(serializers.Serializer):
    model = models.UserProfile

    """
    """
    



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
        
        extra_kwargs = {'adresse': {'required': False}} 
    

class ParametreCarteSerializer(serializers.ModelSerializer):
    """Serializer the user profile object"""
            
    class Meta:
        
        model = ParametreCarte
        fields = '__all__'

        
class PermissionsSerializer(serializers.ModelSerializer):
    """Serializer the user profile object"""
            
    class Meta:
        model = models.UserProfile
        fields = ('nom', 'phone')

        
class ContactCompteSerializers(serializers.ModelSerializer):
    """Serializer the user profile object"""
            

    
    class Meta:
        
        model = Compte
        fields = ('id', 'numCompte', 'nomCompte', 'type')
        
        
        extra_kwargs = {
            'user' : {
                'read_only' : True,
                
            }, 
        }

      
class ToggleCompteSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Compte
        fields = ('numCompte',)  
        extra_kwargs = {'numCompte': {'required': True}}    

        


class PermissionsChangeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Permissions
        fields = '__all__'        




        


class AddContactSerializers(serializers.Serializer):
    
    telephoneUser = serializers.CharField(max_length = 25)
    telephoneContact = serializers.CharField(max_length = 25)
    
    
class ContactSerializers(serializers.ModelSerializer):
    
    comptes = ContactCompteSerializers( source = "compte_set", read_only = True, many = True)
    
    class Meta:
        model = models.UserProfile
        fields = ("phone", "nom", "comptes")
      
#---------------------------------------------------------------      
      
      
class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer the user profile object"""

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        if self.context["request"].method == "PUT":
            self.fields.pop("password")
            self.fields.pop("phone")
        if "data" in kwargs.keys():  
            self.f = kwargs["data"]
            
            

    class Meta:

        model = models.UserProfile
        fields = ('id', 'phone', 'email', 'code', 'valide' , 'nom', 'prenom', 'dateDeNaissance', 'password', 'url', 'is_active', 
                  'is_staff', 'genre')
        extra_kwargs = {
            'password' : {
                'write_only' : True,
                'style' : {
                    'input_type' : 'password'
                }
            }, 
        }
        
    def create(self, validated_data):
        """create the return new user"""
        if self.f is not None:
            allowed = set(self.f.keys())
            existing = set(self.fields)
            for field_name in existing - allowed:
                validated_data[field_name] = None

        user = models.UserProfile.objects.create_user(
            email =  validated_data['email'],
            nom =  validated_data['nom'],
            phone =  validated_data['phone'],
            prenom = validated_data['prenom'],
            dateDeNaissance = validated_data['dateDeNaissance'],
            password = validated_data['password']
        )

        return user
   
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


        

    
        