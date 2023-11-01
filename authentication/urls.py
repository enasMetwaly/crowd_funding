from django.urls import include,path
from .views import *
from django.contrib import admin
from django.urls import path, include
# from core import views as core_views
from . import views



urlpatterns=[
    path('login',login,name='login'),
    path('logout',Logout,name='logout'),
    path('register',register,name='register'),
    path('oauth/', include('social_django.urls', namespace='social')),  # <-- here

    path('settings/', SettingsView.as_view(), name='settings'),
    path('settings/password/', password, name='password'),
    # path('secure-page/',secure_view, name='secure-page'),

    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),

    # path('account_activation_complete/', account_activation_complete, name='account_activation_complete'),

]
