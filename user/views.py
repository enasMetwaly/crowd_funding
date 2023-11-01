from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserProfileForm
from .models import User, UserProfile
from mainproject.models import Project,Donation

from django.contrib.auth import authenticate, login
from django.contrib import messages

from mainproject.models import Image


# Create your views here.


@login_required
def profile(request):
    user=request.user
    user_profile = UserProfile.objects.get(user=user)
    imgs = Image.objects.all()
    user_projects = Project.objects.filter(creator_id=request.user.id)
    return render(request, 'user/profile/base.html', {'user_projects': user_projects, 'donations': False,'user':user,'user_profile':user_profile,'imgs':imgs})



@login_required
def donations(request):

    user_donations = Donation.objects.filter(user=request.user)
    project_ids = user_donations.values_list('project_id', flat=True)
    projects = Project.objects.filter(id__in=project_ids)
    return render(request, 'user/profile/user_donation.html', {
        'user_donations': user_donations,
        'projects': projects,
        'donations': True,
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'user/profile/edit_profile.html', {'form': form})





@login_required
def delete_user_account(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        if request.user.check_password(password):
            request.user.delete()
            messages.success(request, "Your account has been deleted.")
            return redirect('home')  
        else:
            messages.error(request, "Incorrect password. Account not deleted.")

    return render(request, 'user/profile/confirm_delete.html')
