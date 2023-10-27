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
    path('<int:project_id>/comment', create_comment, name='create_comment'),

    path('<int:project_id>/report', add_report, name='create_report'),

    path('<int:comment_id>/report_comment', add_comment_report, name='create_comment_report'),

    path('<int:comment_id>/reply', create_comment_reply, name='create_comment_reply'),

]
