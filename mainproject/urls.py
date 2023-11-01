from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page ),
     path('add', views.add_project, name='addproject'),
    path('list', views.list_project, name='listproject'),
    path('delete/<int:id>', views.delete_project, name='deleteproject'),
    path('details/<int:id>', views.details_project, name='detailsproject'),
    path('details/<int:id>/donate', views.donate, name='donate'),
    path('<int:id>/rate', views.rate, name='project_rate'),
    path('<int:project_id>/comment', views.create_comment, name='create_comment'),
    path('<int:project_id>/report', views.add_report, name='create_report'),
    path('<int:comment_id>/report_comment',views.add_comment_report, name='create_comment_report'),
    path('<int:comment_id>/reply', views.create_comment_reply, name='create_comment_reply'),
    path('projects/tag/<str:tag_name>/', views.get_tag_projects, name='get_tag_projects')

]
