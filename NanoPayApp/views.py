from ast import For
from email import message
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters , generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import mixins
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    DjangoModelPermissions,
)
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django.contrib.auth import authenticate
from NanoPayApp import serializers
from NanoPayApp import models, permissions

from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Inscription']))
class UserCreateView(generics.CreateAPIView):
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.UserSerializer
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Inscription']))
class UserCodeCreateView(generics.CreateAPIView):    
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.UserCodeSerializer
    
    def create(self, request, *args, **kwargs):
        phone = request.data["phone"]
        code = request.data["code"]
        user = get_object_or_404(models.UserProfile ,phone = phone, code = code)
        user.valide = True
        user.save()  
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {"code" : serializer.data["code"],
                    "message" : "your Acount is successfuly activate"}
        return Response(response)
        


@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Inscription']))
class UserInfoView(generics.CreateAPIView):
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.UserInfoSerializer
    
    def get_user(self, phone):
        try:
            return models.UserProfile.objects.get(phone = phone)
        except models.UserProfile.DoesNotExist:
            return HttpResponseBadRequest(status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request, *args, **kwargs):
        
        phone = request.data["phone"]
        user = get_object_or_404(models.UserProfile ,phone = phone)  
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        comptes = user.compte_set.all()
        comptes = serializers.CompteSerializer(comptes, many = True)
        response = serializer.data
        response["compte"] = comptes.data
        
        
        return Response(response)
        
        
@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Connexion']))
class UserLoginView(generics.ListAPIView):
    
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.UserLoginSerializer
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = self.kwargs["password"]
        phone = self.kwargs["telephone"]
        user = authenticate(request, username = phone , password = password)
        
        if (not user):
            
            reponse = {"detail": "Unable to authenticate with provided credentials"}
            
            return Response(
                        reponse,
                        status=status.HTTP_404_NOT_FOUND,   
                    )
        comptes = user.compte_set.all()
        comptes = serializers.CompteSerializer(comptes, many = True)
        return Response(
            data = {"id": user.id,
                    "telephone": user.phone,
                    "nom": user.nom,
                    "prenom": user.prenom,
                    "dateDeNaissance": user.dateDeNaissance,
                    "genre": user.genre,
                    "comptes": comptes.data
                    }
        )
          
           
@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Compte'],
                                    operation_description="hello world",
                                    operation_summary="hello world"))
class CompteCreateView(generics.CreateAPIView):
    """
    parameters:
        - name: name
          description: Foobar long description goes here
    """
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.CreateCompteSerializer
    
    def create(self, request, *args, **kwargs):
        phone = request.data["telephone"]
        user = get_object_or_404(models.UserProfile ,phone = phone)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        num_compte = len(user.compte_set.all())
        if num_compte >= 10:
            response = {"status" : "Bad request", 
                        "message" : "This user already have most than 10 Account"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        else :
            
            c = models.Compte(user = user)
            c.nomCompte = serializer.data.get("nomCompte")
            num_compte = num_compte + 1
            if num_compte == 10:   
                c.numCompte = user.phone +"-"+str(num_compte)
            else:
                c.numCompte = user.phone +"-0"+str(num_compte)
            c.type = serializer.data.get("type")
            if c.type in ["depense",]:
                params = models.ParametreCarte()
                params.save()               
                c.parametre = params
            c.principal = False
            c.save()
            response = {"code":  status.HTTP_200_OK,
                        "message" : "Succesful create Account"}
            
            return Response(response,)


@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Compte'],
                    operation_id= "Get_all_user_Account",
                    operation_summary="renvoie la liste des comptes d'un utilisateur"))
class UserComptesView(generics.ListAPIView):
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.CompteSerializer
    def get_queryset(self):
        phone = self.kwargs["telephone"]
        user = get_object_or_404(models.UserProfile ,phone = phone)
        return user.compte_set.all()

    
@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Compte']))   
class RetrieveComptesView(generics.RetrieveAPIView):
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.CompteSerializer
    lookup_field = "numCompte"
    def get_object(self):
        compte = get_object_or_404(models.Compte ,numCompte = self.kwargs["numCompte"])
        return compte


@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Compte']))   
class ToggleCompteView(generics.CreateAPIView):
    
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.ToggleCompteSerializer
    
    def create(self, request, *args, **kwargs):
        
        c = get_object_or_404(models.Compte ,numCompte = request.data["numCompte"])
        p = c.parametre
        if p.active == True :
            p.active = False
        else: 
            p.active = True
        p.save()
        c.save()
        
        return Response({"code": status.HTTP_201_CREATED, 
                         "message": "Carte was toggle succesfuly"})

@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Compte']))   
class QuotidientLimiteView(generics.CreateAPIView):
    
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.QuotidientLimiteSerializer
    
    def create(self, request, *args, **kwargs):
        
        c = get_object_or_404(models.Compte ,numCompte = request.data["numCompte"])
        p = c.parametre
        p.PaiementQuotidientLimite = request.data["valeurLimite"]
        p.save()
        c.save()
        
        return Response({"code": status.HTTP_201_CREATED, 
                         "message": "Paiement Quotidient Limite was set succesfuly"})
 
 
@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Compte']))          
class PaimentQuotidientView(generics.CreateAPIView):
    
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.PlafondLimiteSerializer
    
    def create(self, request, *args, **kwargs):
        
        c = get_object_or_404(models.Compte ,numCompte = request.data["numCompte"])
        p = c.parametre
        p.PaimentQuotidient = request.data["valeurPlafond"]
        p.save()
        c.save()
        
        return Response({"code": status.HTTP_201_CREATED, 
                         "message": "Montant limite was set succesfuly"})

        
@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Compte']))
class AddPermissionView(generics.CreateAPIView):
    
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.PermissionsChangeSerializer
    
    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        c = get_object_or_404(models.Compte ,numCompte = request.data["NumCompte"])
        user = get_object_or_404(models.UserProfile ,phone = request.data["TelephoneUser"])  
        
        c.permissions.add(user)
        
        c.save()
        
        return Response({"code": status.HTTP_201_CREATED, 
                         "message": "User was successfuly added"})

       
@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Compte']))       
class RemovePermissionView(generics.CreateAPIView):
    
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.PermissionsChangeSerializer
    
    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        c = get_object_or_404(models.Compte ,numCompte = request.data["NumCompte"])
        user = get_object_or_404(models.UserProfile ,phone = request.data["TelephoneUser"])  
        
        c.permissions.remove(user)
        
        c.save()
        
        return Response({"code": status.HTTP_201_CREATED, 
                         "message": "User was successfuly removed"})

        
@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Compte']))    
class PermissionsListView(generics.ListAPIView):
    
    serializer_class = serializers.PermissionsSerializer
    
    def get_queryset(self):
        numCompte = self.kwargs["numCompte"]
        compte = get_object_or_404(models.Compte ,numCompte = numCompte)
        return compte.permissions.all()





class ContactRetreiveView(generics.ListAPIView):
    
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.UserLoginSerializer
    def list(self, request, *args, **kwargs):
        
        user = get_object_or_404(models.UserProfile ,phone = self.kwargs["telephone"])  
        comptes = user.compte_set.all()
        comptes = serializers.CompteSerializer(comptes, many = True)
        return Response({
                    "nom": user.nom,
                    "telephone": user.phone,
                    "comptes": comptes.data
                    }
        )



    

#################################################################




class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating user profile"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    #permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter, )
    search_fields = ('nom', 'email','phone',)
    filter_fields = ('phone',)
    parser_classes = (MultiPartParser,FormParser) 

    def get_user(self, id):
        try:
            return models.UserProfile.objects.get(id=id)
        except models.UserProfile.DoesNotExist:
            return HttpResponseBadRequest(status=status.HTTP_404_NOT_FOUND)
        
class UserList(generics.ListAPIView):
    serializer_class = serializers.UserProfileSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        phone = self.kwargs['telephone']
        return models.UserProfile.objects.filter(phone=phone)
        
class CustomAuthToken(ObtainAuthToken, CreateAPIView):

    parser_classes = (MultiPartParser,FormParser) 
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'telephone': user.phone
        })

class Logout(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def delete(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        response = {
                "status": "success",
                "message": "successfully logout",
            }
        return Response(response , status=status.HTTP_200_OK)
    
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    parser_classes = (MultiPartParser,FormParser) 

    serializer_class = serializers.ChangePasswordSerializer
    model = models.UserProfile
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
      
class CompteViewSet(viewsets.ModelViewSet):
    """Handle creating and updating user profile"""
    serializer_class = serializers.CompteSerializer
    queryset = models.Compte.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ('solde', 'type','numCompte',)
    filterset_fields = ('user__nom',)
    ordering_fields = ('solde', 'id',)
    parser_classes = (MultiPartParser,FormParser)
    
    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""

        serializer.save(user=self.request.user)
        
    
        
class ParametreCarteViewSet(viewsets.ModelViewSet):
    """Handle creating and updating user profile"""
    serializer_class = serializers.ParametreCarteSerializer
    queryset = models.ParametreCarte.objects.all()
    authentication_classes = (TokenAuthentication,)
    
    parser_classes = (MultiPartParser,FormParser)
    
    
        
        
