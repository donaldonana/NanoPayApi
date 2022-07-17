from unicodedata import name
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from django.conf.urls import  url

from Comptes import views
from drf_yasg import openapi


router = DefaultRouter() 

urlpatterns = [ 

    path('user/compte/<telephone>', views.UserComptesView.as_view(), name= 'Comptes'),
    path('user/compte/', views.CompteCreateView.as_view(), name= 'UserCompte'),
    path('user/compte/info/<numCompte>', views.RetrieveComptesView.as_view()),
    path('user/compte/carte/toggle/', views.ToggleCompteView.as_view(), name= 'ToggleCarte'),
    path('user/compte/carte/limite/', views.QuotidientLimiteView.as_view()),
    path('user/compte/carte/plafond/', views.PaimentQuotidientView.as_view()),
    path('carte/init/', views.CarteInitCreateAPIView.as_view()),
    



     
	

]