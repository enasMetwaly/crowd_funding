from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserProfileForm
from .models import User, UserProfile
from mainproject.models import Project

from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.


# @login_required
def profile(request):
    user=request.user
    print(user)
    user_projects = Project.objects.filter(creator_id=request.user.id)
    # return render(request, 'user/profile/base.html')

    return render(request, 'user/profile/base.html', {'projects': user_projects, 'donations': False,'user':user})

@login_required
# def donations(request):
#     user_donations = Donation.objects.filter(
#     donator_id=request.user.id)
#     projects  = Project.objects.all()
#     return render(request, 'profile/base.html', {'user_donations': user_donations,
#                                                  'projects': projects, 'donations': True})
#

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
            # Password is correct, proceed with account deletion
            request.user.delete()
            messages.success(request, "Your account has been deleted.")
            return redirect('home')  # Redirect to the homepage or a suitable URL
        else:
            messages.error(request, "Incorrect password. Account not deleted.")

    return render(request, 'user/profile/confirm_delete.html')
