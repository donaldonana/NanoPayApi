from ast import For
from email import message
from tempfile import tempdir
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


from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from AppsUser import serializers
from AppsUser import models, permissions
from AppsComptes.models import Compte
import AppsComptes
# from TwioloTest import SendCode



def get_user(phone):
    try:
        return models.UserProfile.objects.get(phone = phone)
    except models.UserProfile.DoesNotExist:
        return None

def get_compte(ncompte):
    try:
        return Compte.objects.get(numCompte = ncompte)
    except:
        return None



@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Inscription']))
class UserCreateView(generics.CreateAPIView):
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.UserSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() :

            print("\n---------------------------------\n")
            print(serializer.validated_data)

            serializer.save()
            # SendCode(serializer.data["phone"])
            response = {"success" : "True"}
            response["data"] = serializer.data
            return Response(response)           
        else :
            return Response({"success":"False", "data":None, "detail":"Credential Already use"}, status = status.HTTP_200_OK)
           
        

@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Inscription']))
class UserDeleteView(generics.CreateAPIView):
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.UserDeleteSerializer
    def create(self, request, *args, **kwargs):
        
        phone = request.data["telephone"]
        user = get_user(phone)
        if(not user):
            return Response({"success" : False, "data":None, "detail" : "Not Found"},
            status = status.HTTP_200_OK)
        user.delete()
        # comptes = user.compte_set.all()
        response = {"success" : "True", "data":None}
       
        
        return Response(response)
        
        
        

@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Inscription']))
class UserCodeCreateView(generics.CreateAPIView):    
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.UserCodeSerializer
    
    def create(self, request, *args, **kwargs):
        phone = request.data["phone"]
        code = request.data["code"]
        user = get_user(phone)
        if(not user):
            return Response({"succes" : True, "data":None, "detail" : "Not Found"},
            status = status.HTTP_200_OK)
        if(user.code != code):
            return Response({"succes" : True, "data":None, "detail" : "Not Found"},
            status = status.HTTP_200_OK)
        user.valide = True
        user.save()  
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {"succes" : True,
                    "data":None,}
        return Response(response)
        


@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Inscription']))
class UserInfoView(generics.CreateAPIView):
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.UserInfoSerializer
    
    def get_user(self, phone):
        try:
            return models.UserProfile.objects.get(phone = phone)
        except models.UserProfile .DoesNotExist:
            return Response({"succes" : True, "data":None, "detail" : "Not Found"},
                            status = status.HTTP_200_OK)
        
    def create(self, request, *args, **kwargs):
        
        phone = request.data["phone"]
        user = get_user(phone)
        if(not user):
            return Response({"succes" : False, "data":None, "detail" : "Not Found"},
            status = status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        nc = user.phone + '-01'
        c = user.compte_set.get(user_id = user.id, numCompte = nc)
        c.nomCompte = user.get_full_name()
        c.save()
        comptes = user.compte_set.all()
        comptes = AppsComptes.serializers.CompteSerializer(comptes, many = True)
        temp = serializer.data
        temp["compte"] = comptes.data
        response = {"success" : "True"}
        response["data"] = temp
        
        
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
            
            reponse = {"success" : False,
                       "data" : None,
                       "detail": "Unable to authenticate with provided credentials"}
            
            return Response(
                        reponse,
                        status=status.HTTP_200_OK,   
                    )
        comptes = user.compte_set.all()
        comptes = AppsComptes.serializers.CompteSerializer(comptes, many = True)
        return Response(
            data = {
                    "sucess" : True,
                    "data" : {
                        "id": user.id,
                    "telephone": user.phone,
                    "nom": user.nom,
                    "prenom": user.prenom,
                    "dateDeNaissance": user.dateDeNaissance,
                    "genre": user.genre,
                    "comptes": comptes.data
                    }
                    
                    }
        )
          
   

    


        
@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Compte'],
                operation_summary="Permet d’ajouter un utilisateur dans les autorisations de paiement"))          

class AddPermissionView(generics.CreateAPIView):
    
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.PermissionsChangeSerializer
    
    def create(self, request, *args, **kwargs):
        
        c=get_object_or_404(AppsComptes.models.Compte  ,numCompte = request.data["comptes"])
        r=get_object_or_404(models.UserProfile ,phone = request.data["recepteur"])
        e=get_object_or_404(models.UserProfile ,phone = request.data["emetteur"])
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() :
            serializer.save() 
            p=get_object_or_404(models.Permissions ,  comptes = c.numCompte , emetteur = e.phone , recepteur = r.phone )
            c.permissions.add(p)
            c.save()
            reponse = {"success" : True , "data" : None}
            return Response(reponse)
        else:
            return Response({"success" : False, "data" : None, "detail" : "Already exist"},
                            status=status.HTTP_200_OK)

       
@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Compte'],
                operation_summary="Permet de retirer  un utilisateur dans les autorisations de paiement"))             
class RemovePermissionView(generics.CreateAPIView):
    
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.PermissionsChangeSerializer
    
    def create(self, request, *args, **kwargs):
        
        c=get_object_or_404(AppsComptes.models.Compte ,numCompte = request.data["comptes"])
        r=get_object_or_404(models.UserProfile ,phone = request.data["recepteur"])
        e=get_object_or_404(models.UserProfile ,phone = request.data["emetteur"])
        p=get_object_or_404(models.Permissions ,  comptes = c.numCompte , emetteur = e.phone , recepteur = r.phone )
        p.delete()
        c.permissions.remove(p)
        c.save()
        return Response({"succes": True, 
                         "data": None})

        
@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Compte'],
                operation_summary="Renvoie la liste des permissions associé à un compte professionnel"))             
                      
class PermissionsListView(generics.ListAPIView):
    
    serializer_class = serializers.PermissionsChangeSerializer
    
    # def get_queryset(self):
    #     numCompte = self.kwargs["numCompte"]
    #     compte = get_object_or_404(models.Compte ,numCompte = numCompte)
    #     return compte.permissions.all()
    
    def list(self, request, *args, **kwargs):
        numCompte = self.kwargs["numCompte"]
        try:
            p=models.Permissions.objects.filter(comptes=self.kwargs["numCompte"])
            p = serializers.PermissionsChangeSerializer(p, many=True)
            if len(p.data) == 0:
               return Response({"succes": False, "data" : None},
                            status = status.HTTP_200_OK)
            return Response({"succes" : True , "data": p.data})
        except models.Permissions.DoesNotExist:
            return Response({"succes": False, "data" : None},
                            status = status.HTTP_200_OK)

        
    





class ContactRetreiveView(generics.ListAPIView):
    """_Recherche et renvoie le contacts de l'utilisateur chercher accompagné de ses comptes._

    Args:
        generics (_type_): _description_

    Returns:
        _type_: _description_
    """
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.UserLoginSerializer
    def list(self, request, *args, **kwargs):
        
        user = get_object_or_404(models.UserProfile ,phone = self.kwargs["telephone"])
        #if user in   
        comptes = user.compte_set.all()
        comptes = AppsComptes.serializers.CompteSerializer(comptes, many = True)
        return Response({
                    "succes" : True,
                    "data" : {
                        "nom": user.nom,
                        "telephone": user.phone,
                        "comptes": comptes.data
                    }
                    
                    }
        )


class AddContactView(generics.CreateAPIView):
    
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.AddContactSerializers
    
    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(models.UserProfile ,phone = request.data["telephoneUser"])
        contacts = get_object_or_404(models.UserProfile ,phone = request.data["telephoneContact"]) 
        
        user.contacts.add(contacts)
        
        user.save()
        
        return Response({"success": True, 
                         "data": None})
        
class RemoveContactView(generics.CreateAPIView):
    
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.AddContactSerializers
    
    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(models.UserProfile ,phone = request.data["telephoneUser"])
        contacts = get_object_or_404(models.UserProfile ,phone = request.data["telephoneContact"]) 
        
        user.contacts.remove(contacts)
        
        user.save()
        
        return Response({"success": True, 
                         "message": None})
    
    
class ContactListView(generics.ListAPIView):
     
    serializer_class = serializers.ContactSerializers
    # def get_queryset(self):
    #     user = get_object_or_404(models.UserProfile ,phone = self.kwargs["telephone"])
    #     return user.contacts.all()
    
    def list(self, request, *args, **kwargs):
        phone = self.kwargs["telephone"]
        user = get_user(phone)
        if(not user):
            return Response({"succes" : False, "data":None, "detail" : "Not Found"},
            status = status.HTTP_404_NOT_FOUND)
        contacts = user.contacts.all()
        contacts = serializers.ContactSerializers(contacts, many = True)
        reponse = {"sucess":True, "data": contacts.data}
        
        return Response(reponse)
    

#################################################################


        
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
      

    
    
        
        
