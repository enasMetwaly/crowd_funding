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
    path('<int:id>/rate', rate, name='project_rate'),
    path('<int:id>/comment', create_comment, name='create_comment'),

    path('<int:id>/report', add_report, name='create_report'),
    path('<int:id>/report_comment', add_comment_report, name='create_comment_report'),
    path('<int:id>/reply', create_comment_reply, name='create_comment_reply'),

    path('projects/tag/<int:tag_id>', get_tag_projects, name='get_tag'),
]
