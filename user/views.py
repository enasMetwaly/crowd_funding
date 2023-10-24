from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import User, UserProfile

# Create your views here.


@login_required
def profile(request):
    current_user_projects = Project.objects.filter(
        creator_id=request.user.id)
    return render(request, 'profile/base.html', {'campaigns': current_user_projects, 'donations': False})
