from django.shortcuts import render, redirect,get_object_or_404,HttpResponseRedirect
from .forms import *
from .models import *
import os 
from django.forms import inlineformset_factory
from django.db.models import Avg, Sum
from datetime import datetime
from django.urls import reverse
from django import forms
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
NULL={}



def getUser(request):
    user_id = request.user.id
    if user_id is not None:
        User = get_user_model()
        try:
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist:
            return None
    return None

@login_required
def my_view(request):
    user = request.user
    return HttpResponse(f"Hello, {user.id}!")




def add_project(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        pictures_form = PicturesForm(request.POST, request.FILES)
        if project_form.is_valid() and pictures_form.is_valid():
            project = project_form.save(commit=False)
            project.creator = request.user  # Assign the current user as the creator
            project.save()
            for image_file  in request.FILES.getlist('images'):
                image = Image(images=image_file, project=project)
                image.save()

            return redirect('listproject')
    else:
        project_form = ProjectForm()
        pictures_form = PicturesForm(instance=Project())
    return render(request, 'mainproject/add.html', {'project_form': project_form, 'pictures_form': pictures_form})



def donate(request, id):
    if 'user_id' in request.session:
        # Redirect to the login page if the user is not authenticated
        return redirect('login')
    else:
        user = getUser(request)
        if request.method == "POST" and 'donate' in request.POST:
            donation_amount = request.POST['donate']
            
            # Create a Donation object and provide the project_id
            donation = Donation.objects.create(
                donation=donation_amount,
                project_id=id,  # Provide the project_id
                user=user  # Assign the user object directly
            )
            
            return redirect('detailsproject', id)
        return render(request, "mainproject/details.html", {'id': id, 'user': user})


def details_project(request, id):
    project = get_object_or_404(Project, id=id)
    return render(request, 'mainproject/details.html', {'project': project})

def delete_project(request, id):
    project = Project.objects.get(id=id)
    images = Image.objects.filter(project=project)
    for image in images:
        image_path = image.images.path
        if os.path.exists(image_path):
            os.remove(image_path)
    images.delete()
    project.delete()
    return HttpResponseRedirect('/main/list')

def list_project(request):
    context={}
    projects=Project.objects.all()
    imgs=Image.objects.all()
    context['projects']=projects
    context['imgs']=imgs
    return render(request, 'mainproject/list.html', context)

