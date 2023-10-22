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
    # path('', HomeView.as_view(), name='home'),
    path('', home, name='home'),

    # # Login and Logout
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    #
    path('settings/', SettingsView.as_view(), name='settings'),
    path('settings/password/', password, name='password'),
    # path('secure-page/',secure_view, name='secure-page'),

    # path('account_activation_sent/', account_activation_sent, name='account_activation_sent'),
    # path('activate/<uidb64>/<token>/', activate, name='activate'),
    # Email confirmation
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),

    # path('account_activation_complete/', account_activation_complete, name='account_activation_complete'),

]
