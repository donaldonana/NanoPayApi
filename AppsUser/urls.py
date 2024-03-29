from unicodedata import name
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from django.conf.urls import  url

from AppsUser import views
from drf_yasg import openapi


router = DefaultRouter()
#router.register('UserProfile', views.UserProfileViewSet)
#router.register('Compte', views.CompteViewSet)
#router.register('Transaction', views.TransactionViewSet)
#router.register('ParametreCarte', views.ParametreCarteViewSet)



urlpatterns = [

    #path('', include(router.urls)),
    path("login/", views.CustomAuthToken.as_view()),
    path("user/", views.UserCreateView.as_view(), name = "user", ),
    path('user/info/', views.UserInfoView.as_view(), name= 'UserInfo'),
    path('user/code/', views.UserCodeCreateView.as_view(), name= 'UserCode'),
    path('user/compte/permission/add/', views.AddPermissionView.as_view()),
    path('user/compte/permission/remove/', views.RemovePermissionView.as_view()),
    path('contact/add/', views.AddContactView.as_view()),
    path('contact/remove/', views.RemoveContactView.as_view()),

    
    
    
    
    
    

    path('user/conexion/<telephone>/<password>', views.UserLoginView.as_view()),
    path('contact/<telephone>', views.ContactRetreiveView.as_view()),
    path("user/delete/", views.UserDeleteView.as_view(), name = "user", ),
    
    path('contact/list/<telephone>', views.ContactListView.as_view()),
    
    path('user/compte/permission/<numCompte>', views.PermissionsListView.as_view()),
    
    
    #url(r'^user/(?P<telephone>\d+)/$', views.UserLoginView.as_view(), name= 'UserLogin'),
    
    
    
    #path("change-password/", views.ChangePasswordView.as_view()),
    path("logout/", views.Logout.as_view()),
    #path('user/{tlephone}/', views.PurchaseList.as_view()),
    #url(r'^user/(?P<telephone>\d+)/$', views.UserList.as_view()),

]
