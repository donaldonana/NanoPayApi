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
from NanoPayApp import serializers
from NanoPayApp import models, permissions

from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# from TwioloTest import SendCode



def get_user(phone):
    try:
        return models.UserProfile.objects.get(phone = phone)
    except models.UserProfile.DoesNotExist:
        return None



@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Inscription']))
class UserCreateView(generics.CreateAPIView):
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.UserSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() :
            serializer.save()
            # SendCode(serializer.data["phone"])
            response = {"success" : "True"}
            response["data"] = serializer.data
            return Response(response)           
        else :
            return Response({"succes":"False", "data":None, "detail":"Credential Already use"}, status = status.HTTP_400_BAD_REQUEST)
           
        

@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Inscription']))
class UserDeleteView(generics.CreateAPIView):
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.UserInfoSerializer
    def create(self, request, *args, **kwargs):
        
        phone = self.kwargs["telephone"]
        user = get_user(phone)
        if(not user):
            return Response({"succes" : False, "data":None, "detail" : "Not Found"},
            status = status.HTTP_404_NOT_FOUND)
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
            status = status.HTTP_404_NOT_FOUND)
        if(user.code != code):
            return Response({"succes" : True, "data":None, "detail" : "Not Found"},
            status = status.HTTP_404_NOT_FOUND)
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
        except models.UserProfile .DoesNotExist:
            return Response({"succes" : True, "data":None, "detail" : "Not Found"},
                            status = status.HTTP_404_NOT_FOUND)
        
    def create(self, request, *args, **kwargs):
        
        phone = request.data["phone"]
        user = get_user(phone)
        if(not user):
            return Response({"succes" : True, "data":None, "detail" : "Not Found"},
            status = status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        comptes = user.compte_set.all()
        comptes = serializers.CompteSerializer(comptes, many = True)
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
                        status=status.HTTP_404_NOT_FOUND,   
                    )
        comptes = user.compte_set.all()
        comptes = serializers.CompteSerializer(comptes, many = True)
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
            return Response({"succes" : True, "data":None, "detail" : "Not Found"},
            status = status.HTTP_404_NOT_FOUND)
        # user = get_object_or_404(models.UserProfile ,phone = phone)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        num_compte = len(user.compte_set.all())
        if num_compte >= 10:
            response = {"succes" : False,
                        "data" : None, 
                        "detail" : "This user already have most than 10 Account"}
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
            response = {"succes":  True,
                        "data" : None}
            
            return Response(response,)


@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Compte'],
                    operation_id= "Get_all_user_Account",
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
            return Response({"succes" : True, "data":None, "detail" : "Not Found"},
            status = status.HTTP_404_NOT_FOUND)
        comptes = user.compte_set.all()
        comptes = serializers.CompteSerializer(comptes, many = True)
        reponse = {"sucess":True, "data": comptes.data}
        
        return Response(reponse)
    
@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Compte'],
                        operation_summary="Renvoie les informations lié à un compte"))   
class RetrieveComptesView(generics.RetrieveAPIView):
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.CompteSerializer
    lookup_field = "numCompte"
    def get_object(self):
        compte = get_object_or_404(models.Compte ,numCompte = self.kwargs["numCompte"])
        return compte
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"success":True,"data":serializer.data})

@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Compte'],
                        operation_summary="permet d’activé/desactive une carte"))   
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
        
        return Response({"succes": True, 
                         "message": None})


@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Compte'],
                    operation_summary=" Permet de modifier la valeur du nombre limite de paiement sans confirmation du compte"))   
class QuotidientLimiteView(generics.CreateAPIView):
    
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.QuotidientLimiteSerializer
    
    def create(self, request, *args, **kwargs):
        
        c = get_object_or_404(models.Compte ,numCompte = request.data["numCompte"])
        p = c.parametre
        p.PaiementQuotidientLimite = request.data["valeurLimite"]
        p.save()
        c.save()
        
        return Response({"sucess": True, 
                         "data": None})
 
 
@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Compte'],
                    operation_summary="Permet de modifier la valeur du plafond (montant maximal par opération)  de paiement sans confirmation du compte"))          
class PaimentQuotidientView(generics.CreateAPIView):
    
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.PlafondLimiteSerializer
    
    def create(self, request, *args, **kwargs):
        
        c = get_object_or_404(models.Compte ,numCompte = request.data["numCompte"])
        p = c.parametre
        p.PaimentQuotidient = request.data["valeurPlafond"]
        p.save()
        c.save()
        
        return Response({"sucess": True,
                         "data": None})

        
@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Compte'],
                operation_summary="Permet d’ajouter un utilisateur dans les autorisations de paiement"))          

class AddPermissionView(generics.CreateAPIView):
    
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.PermissionsChangeSerializer
    
    def create(self, request, *args, **kwargs):
        
        get_object_or_404(models.Compte ,numCompte = request.data["comptes"])
        get_object_or_404(models.UserProfile ,phone = request.data["recepteur"])
        get_object_or_404(models.UserProfile ,phone = request.data["emetteur"])
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() :
            serializer.save() 
            reponse = {"success" : True , "data" : None}
            return Response(reponse)
        else:
            return Response({"success" : False, "data" : None, "detail" : "Already exist"},
                            status=status.HTTP_400_BAD_REQUEST)

       
@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Compte'],
                operation_summary="Permet de retirer  un utilisateur dans les autorisations de paiement"))             
class RemovePermissionView(generics.CreateAPIView):
    
    parser_classes = (MultiPartParser,FormParser) 
    serializer_class = serializers.PermissionsChangeSerializer
    
    def create(self, request, *args, **kwargs):
        
        c=get_object_or_404(models.Compte ,numCompte = request.data["comptes"])
        r=get_object_or_404(models.UserProfile ,phone = request.data["recepteur"])
        e=get_object_or_404(models.UserProfile ,phone = request.data["emetteur"])
        p=get_object_or_404(models.Permissions ,  comptes = c.numCompte , emetteur = e.phone , recepteur = r.phone )
        p.delete()
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
            return Response({"succes" : True , "data": p.data})
        except models.Permissions.DoesNotExist:
            return Response({"succes": False, "data" : None},
                            status = status.HTTP_404_NOT_FOUND)

        
    





class ContactRetreiveView(generics.ListAPIView):
    """_Recherche et renvoie le contact de l'utilisateur chercher accompagné de ses comptes._

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
        comptes = serializers.CompteSerializer(comptes, many = True)
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
        contact = get_object_or_404(models.UserProfile ,phone = request.data["telephoneContact"]) 
        
        user.contacts.add(contact)
        
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
        contact = get_object_or_404(models.UserProfile ,phone = request.data["telephoneContact"]) 
        
        user.contacts.remove(contact)
        
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
            return Response({"succes" : True, "data":None, "detail" : "Not Found"},
            status = status.HTTP_404_NOT_FOUND)
        contacts = user.contacts.all()
        contacts = serializers.ContactSerializers(contacts, many = True)
        reponse = {"sucess":True, "data": contacts.data}
        
        return Response(reponse)
    

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
    
    
        
        
