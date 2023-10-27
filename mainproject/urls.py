from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path
from authentication.views import home
from django.urls import path,include
from .views import *

urlpatterns = [
 
    path('add',add_project, name ='addproject' ),
    path('list',list_project, name ='listproject' ),
    path('delete/<int:id>',delete_project, name ='deleteproject' ),
    path('details/<int:id>',details_project, name ='detailsproject' ),
    path('details/<int:id>/donate',donate, name ='donate' ),
    path('aa',my_view, name ='my_view' ),
     path('<int:id>/rate', rate, name='project_rate'),

]
