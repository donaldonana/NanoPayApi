from rest_framework import fields, serializers
from django.contrib.auth import authenticate

from NanoPayApp import models

class UserSerializer(serializers.ModelSerializer):
     
    class Meta :
        model = models.UserProfile
        fields = ('id', 'phone', "password")
        
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
        

        user = models.UserProfile.objects.create_user(
            phone =  validated_data['phone'],
            password = validated_data['password']
        )

        return user
         
class UserInfoSerializer(serializers.ModelSerializer):
    
    class Meta :
        model = models.UserProfile
        fields = ('id', 'phone', 'nom', 'prenom', 'dateDeNaissance',
                  'genre')
        


class UserLoginSerializer(serializers.Serializer):
    model = models.UserProfile

    """
    """
    password = serializers.CharField(required=True)


      
      
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
        
        
class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication object"""

    email = serializers.CharField()
    password = serializers.CharField(style = {'input_type' : 'password' }, trim_whitespace = False)

    def validate(self, attrs):
        """Validate and authentiate the user"""

        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request = self.context.get('request'), username = email , password = password)

        if not user:
            msg = ('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user

        return attrs
    
        