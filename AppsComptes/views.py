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
from AppsComptes import serializers
from NanoPayApp import permissions
from NanoPayApp.models import UserProfile

from AppsComptes import models

from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# from TwioloTest import SendCode



def get_user(phone):
    try:
        return UserProfile.objects.get(phone = phone)
    except UserProfile.DoesNotExist:
        return None

def get_compte(ncompte):
    try:
        return models.Compte.objects.get(numCompte = ncompte)
    except:
        return None


@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Compte'],
                    operation_id= "Get_all_user_Account",
                    ref_name = "Compte",

                    operation_summary="renvoie la liste des comptes d'un utilisateur"))
class UserComptesView(generics.ListAPIView):
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.CompteSerializer
    # def get_queryset(self):
    #     phone = self.kwargs["telephone"]
    #     user = get_object_or_404(models.UserProfile ,phone = phone)
    #     return user.compte_set.all()
    def list(self, request, *args, **kwargs):
        phone = self.kwargs["telephone"]
        user = get_user(phone)
        if(not user):
            return Response({"success" : False, "data":None, "detail" : "Not Found"},
            status = status.HTTP_200_OK)
        comptes = user.compte_set.all()
        comptes = serializers.CompteSerializer(comptes, many = True)
        reponse = {"success":True, "data": comptes.data}
        
        return Response(reponse)


        

@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Compte'],
                                    operation_summary="Créer Un compte supplémentaire"))
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
        
        user = get_user(phone)
        if(not user):
            return Response({"success" : False, "data":None, "detail" : "Not Found"},
            status = status.HTTP_200_OK)
        # user = get_object_or_404(models.UserProfile ,phone = phone)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        num_compte = len(user.compte_set.all())
        if num_compte >= 10 or num_compte <= 0:
            response = {"success" : False,
                        "data" : None, 
                        "detail" : "This user already have most than 10 Account Or not already have the first Account"}
            return Response(response, status=status.HTTP_200_OK)
        
        else :
            
            c = models.Compte(user = user)
            c.nomCompte = serializer.data.get("nomCompte")
            num_compte = num_compte + 1
            if num_compte == 10:   
                c.numCompte = user.phone +"-"+str(num_compte)
            else:
                c.numCompte = user.phone +"-0"+str(num_compte)
            c.type = serializer.data.get("type")
            c.adresse = serializer.data.get("adresse")
            if c.type in ["depense",]:
                params = models.ParametreCarte()
                params.save()               
                c.parametre = params
            c.principal = False
            c.save()
            response = {"success":  True,
                        "data" : None}
            
            return Response(response,)



@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Compte'],
                        operation_summary="Renvoie les informations lié à un compte"))   
class RetrieveComptesView(generics.ListAPIView):
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.CompteViewSerializer
    lookup_field = "numCompte"
    
    def list(self, request, *args, **kwargs):
        c = get_compte(self.kwargs["numCompte"])
        if(not c):
            return Response({"success" : False, "data":None, "detail" : "Not Found"},
            status = status.HTTP_200_OK)
        serializer = self.get_serializer(c)
        return Response({"success":True,"data":serializer.data})




@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Compte'],
                        operation_summary="permet d’activé/desactive une carte"))   
class ToggleCompteView(generics.CreateAPIView):
    
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.ToggleCompteSerializer
    
    def create(self, request, *args, **kwargs):
        
        c = get_compte(request.data["numCompte"])
        if(not c):
            return Response({"succes" : False, "data":None, "detail" : "Not Found"},
            status = status.HTTP_200_OK)
        p = c.parametre
        if p.active == True :
            p.active = False
        else: 
            p.active = True
        p.save()
        c.save()
        
        return Response({"succes": True, 
                         "message": None})



@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Carte'],
                    operation_summary=" Permet de modifier la valeur du nombre limite de paiement sans confirmation du compte"))   
class QuotidientLimiteView(generics.CreateAPIView):
    
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.QuotidientLimiteSerializer
    
    def create(self, request, *args, **kwargs):
        
        c = get_compte(request.data["numCompte"])
        if(not c):
            return Response({"succes" : False, "data":None, "detail" : "Not Found"},
            status = status.HTTP_200_OK)
        p = c.parametre
        p.PaiementQuotidientLimite = request.data["valeurLimite"]
        p.save()
        c.save()
        
        return Response({"sucess": True, 
                         "data": None})


@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Carte'],
                    operation_summary="Permet de modifier la valeur du plafond (montant maximal par opération)  de paiement sans confirmation du compte"))          
class PaimentQuotidientView(generics.CreateAPIView):
    
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.PlafondLimiteSerializer
    
    def create(self, request, *args, **kwargs):
        
        c = get_compte(request.data["numCompte"])
        if(not c):
            return Response({"succes" : False, "data":None, "detail" : "Not Found"},
            status = status.HTTP_200_OK)
        p = c.parametre
        p.PaimentQuotidient = request.data["valeurPlafond"]
        p.save()
        c.save()
        
        return Response({"sucess": True,
                         "data": None})

@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Carte'],
                    operation_summary="Permet de modifier la valeur du plafond (montant maximal par opération)  de paiement sans confirmation du compte"))          
class CarteInitCreateAPIView(generics.CreateAPIView):
    
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.CarteInitSerializer
    
    def create(self, request, *args, **kwargs):

        c = get_compte(request.data["numCompte"])
        if(not c):
            return Response({"succes" : False, "data":None, "detail" : "Not Found"},
            status = status.HTTP_200_OK)

        if c.parametre.initialized == True:
            return Response({"succes" : False, "data":None, "detail" : "Initialization already done"},
            status = status.HTTP_200_OK)

        else : 
            p = c.parametre
            p.nip = request.data["nip"]
            p.uid = request.data["uid"]
            p.publickey = request.data["publickey"]
            p.privatekey = request.data["privatekey"]
            p.initialized = True
            p.save()
            c.save()

        
        return Response({"sucess": True,
                         "data": None})