from django.shortcuts import render
from django.http import HttpResponseBadRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters , generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import mixins
from rest_framework import generics
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

from NanoPayApp import serializers
from NanoPayApp import models, permissions


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating user profile"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    #permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('nom', 'email',)
    parser_classes = (MultiPartParser,FormParser)

    def get_user(self, id):
        try:
            return models.UserProfile.objects.get(id=id)
        except models.UserProfile.DoesNotExist:
            return HttpResponseBadRequest(status=status.HTTP_404_NOT_FOUND)
        
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class Logout(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def delete(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """

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
        
        
class TransactionViewSet(viewsets.ModelViewSet):
    """Handle creating and updating user profile"""
    serializer_class = serializers.TransactionSerializer
    queryset = models.Transaction.objects.all()
    authentication_classes = (TokenAuthentication,)
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ('dateHeure',)
    filterset_fields = ('compteEmetteur__nom',)
    ordering_fields = ('dateHeure', 'id',)
    parser_classes = (MultiPartParser,FormParser)
    
    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""

        serializer.save(compteEmetteur=self.request.user)
        
        
class ParametreCarteViewSet(viewsets.ModelViewSet):
    """Handle creating and updating user profile"""
    serializer_class = serializers.ParametreCarteSerializer
    queryset = models.ParametreCarte.objects.all()
    authentication_classes = (TokenAuthentication,)
    
    parser_classes = (MultiPartParser,FormParser)
    
    
        
        
