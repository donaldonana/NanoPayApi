from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls import  url

from NanoPayApp import views


router = DefaultRouter()
router.register('UserProfile', views.UserProfileViewSet)
# router.register('Compte', views.CompteViewSet)
# router.register('Transaction', views.TransactionViewSet)
# router.register('ParametreCarte', views.ParametreCarteViewSet)



urlpatterns = [

    path('', include(router.urls)),
    path("login/", views.CustomAuthToken.as_view()),
    # path("change-password/", views.ChangePasswordView.as_view()),
    path("logout/", views.Logout.as_view()),
    #path('user/{tlephone}/', views.PurchaseList.as_view()),
    url(r'^user/(?P<telephone>\d+)/$', views.UserList.as_view()),

]
