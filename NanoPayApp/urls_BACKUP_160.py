from unicodedata import name
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls import  url

from NanoPayApp import views


router = DefaultRouter()
router.register('UserProfile', views.UserProfileViewSet)
<<<<<<< HEAD
# router.register('Compte', views.CompteViewSet)
# router.register('Transaction', views.TransactionViewSet)
# router.register('ParametreCarte', views.ParametreCarteViewSet)
=======
#router.register('Compte', views.CompteViewSet)
#router.register('Transaction', views.TransactionViewSet)
#router.register('ParametreCarte', views.ParametreCarteViewSet)
>>>>>>> 920db4667ca19caac7dcd64945aab3857da20435



urlpatterns = [

<<<<<<< HEAD
    path('', include(router.urls)),
    path("login/", views.CustomAuthToken.as_view()),
    # path("change-password/", views.ChangePasswordView.as_view()),
    path("logout/", views.Logout.as_view()),
=======
    #path('', include(router.urls)),
    #path("login/", views.CustomAuthToken.as_view()),
    path("user/", views.UserCreateView.as_view(), name = "user", ),
    path('user/info/', views.UserInfoView.as_view(), name= 'UserInfo'),
    path('user/conexion/<telephone>/<password>', views.UserLoginView.as_view(), name= 'UserLogin'),
    #url(r'^user/(?P<telephone>\d+)/$', views.UserLoginView.as_view(), name= 'UserLogin'),
    
    
    
    #path("change-password/", views.ChangePasswordView.as_view()),
    #path("logout/", views.Logout.as_view()), UserInfoView
>>>>>>> 920db4667ca19caac7dcd64945aab3857da20435
    #path('user/{tlephone}/', views.PurchaseList.as_view()),
    #url(r'^user/(?P<telephone>\d+)/$', views.UserList.as_view()),

]
