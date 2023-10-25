from django.shortcuts import render, redirect,get_object_or_404,HttpResponseRedirect
from .forms import *
from .models import *
import os 
from django.forms import inlineformset_factory



   # views.py

from django import forms
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from .models import Project, Image
from .forms import ProjectForm, PicturesForm  # Make sure to import your ProjectForm and PicturesForm

# Create the ImageFormSet using inlineformset_factory
# ImageFormSet = inlineformset_factory(Project, Image, form=PicturesForm, extra=1, can_delete=True)

def add_project(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        pictures_form = PicturesForm(request.POST, request.FILES)
        if project_form.is_valid() and pictures_form.is_valid():
            project = project_form.save(commit=False)
            project.creator = request.user  # Assign the current user as the creator
            project.save()
            for image in request.FILES.getlist('images'):
                images = pictures_form.save(commit=False)
                images.project = project
                images.save()
            return redirect('listproject')
    else:
        project_form = ProjectForm()
        pictures_form = PicturesForm(instance=Project())
    return render(request, 'mainproject/add.html', {'project_form': project_form, 'pictures_form': pictures_form})

# def add_project(request):
#     if request.method == 'POST':
#         project_form = ProjectForm(request.POST)
#         pictures_form = PicturesForm(request.POST, request.FILES)

#         if project_form.is_valid() and pictures_form.is_valid():
#             project = project_form.save(commit=False)
#             project.creator = request.user  # Assign the current user as the creator
#             project.save()
#             images = pictures_form.save(commit=False)
#             images.project = project
#             images.save()
#             # Redirect to project detail page
#             return redirect('listproject')
#     else:
#         project_form = ProjectForm()
#         pictures_form = PicturesForm()
#     print(project_form)
#     return render(request, 'mainproject/add.html', {'project_form': project_form, 'pictures_form': pictures_form})

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
    # project = get_object_or_404(Project, id=id)
    return render(request, 'mainproject/list.html', context)

# def details_project(request, id):
#     project = get_object_or_404(Project, id=id)

#     return render(request, 'mainproject/details.html', {'project': project})