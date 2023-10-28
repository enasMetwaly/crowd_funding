from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('profile/', views.profile, name="user_profile"),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('delete_user_account/', views.delete_user_account, name='delete_user_account'),
    path('user_donation/', views.donations, name='donations'),

]