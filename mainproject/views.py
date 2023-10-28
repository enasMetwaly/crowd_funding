from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404,HttpResponseRedirect
from .forms import *
from .models import *
import os
from django.forms import inlineformset_factory
from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path
from django.urls import path,include
from .views import *


   # views.py

from django import forms
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from .models import Project, Image
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .forms import *
from .models import *
import os
from django.forms import inlineformset_factory
from django.db.models import Avg, Sum
from datetime import datetime

from django.shortcuts import render, redirect

from django.http import HttpResponse
NULL = {}


from .forms import ProjectForm, PicturesForm  # Make sure to import your ProjectForm and PicturesForm

import os
from decimal import Decimal  # Import Decimal from the decimal module
from django.http import HttpResponseRedirect

def my_view(request):
    user = request.user
    return HttpResponse(f"Hello, {user}!")


def add_project(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        pictures_form = PicturesForm(request.POST, request.FILES, instance=Project())  # Pass an instance of the project
        if project_form.is_valid() and pictures_form.is_valid():
            project = project_form.save(commit=False)
            project.creator = request.user
            project.save()

            images_before = request.FILES.getlist('images_before')
            images_after = request.FILES.getlist('images_after')

            for image in images_before:
                image_obj = Image.objects.create(images_before=image,
                                                 project=project)  # Create an Image object for "before" image
                image_obj.save()

            for image in images_after:
                image_obj = Image.objects.create(images_after=image,
                                                 project=project)  # Create an Image object for "after" image
                image_obj.save()

            return render(request, 'mainproject/list.html', {'images_before': images_before, 'images_after': images_after})
        else:
            print("Form is not valid")
    else:
        project_form = ProjectForm()
        pictures_form = PicturesForm(instance=Project())
    return render(request, 'mainproject/add.html', {'project_form': project_form, 'pictures_form': pictures_form})


def delete_project(request, id):
    project = Project.objects.get(id=id)
    images = Image.objects.filter(project=project)
    for image in images:
        image_path = image.images.path
        if os.path.exists(image_path):
            os.remove(image_path)
    images.delete()
    project.delete()
    return HttpResponseRedirect('/mainproject/list')

def list_project(request):
    context={}
    projects=Project.objects.all()
    imgs=Image.objects.all()
    context['projects']=projects
    context['imgs']=imgs
    # project = get_object_or_404(Project, id=id)
    return render(request, 'mainproject/list.html', context)


def donate(request, id):
    user = request.user
    if request.method == "POST" and 'donate' in request.POST:
        donation_amount = request.POST['donate']
        donation = Donation.objects.create(
            donation_amount=donation_amount,  # Correct field name to 'donation_amount'
            project_id=id,  # Provide the project_id
            user=user  # Assign the user object directly
        )

        return render(request, "mainproject/details2.html", {'project_id': id})
    return render(request, "mainproject/donate.html", {'id': id, 'user': user})



def details_project(request, id):
    project = get_object_or_404(Project, id=id)
    user = request.user
    donate = project.donation_set.all().aggregate(Sum("donation_amount"))
    donations_count = len(project.donation_set.all())

    # Convert the project total_target to a float
    total_target = float(project.total_target)
    donation_average = (donate["donation_amount__sum"] if donate["donation_amount__sum"] else 0) * 100 / total_target
    imgs = Image.objects.filter(project_id=id)
    for img in imgs:
        print(img.images_before)
        print(img.images_before)
    image_count = len(imgs)

    myFormat = "%Y-%m-%d %H:%M:%S"
    today = datetime.strptime(datetime.now().strftime(myFormat), myFormat)
    end_date = datetime.strptime(project.end_time.strftime(myFormat), myFormat)
    days_diff = (end_date - today).days

    average_rating = project.rate_set.all().aggregate(Avg('rate'))['rate__avg']

    # Return user rating if found
    user_rating = 0


    if 'user_id' in request.session:
        prev_rating = Rate.objects.filter(project=project, user=user)
        if prev_rating:
            user_rating = prev_rating[0].rate

    if average_rating is None:
        average_rating = 0

    comments = project.comment_set.all()
    new_report_form = Report_form()
    reply = Reply_form()
    replies = Reply.objects.all()


    context = {
        'project': project,
        'donation': donate["donation_amount__sum"] if donate["donation_amount__sum"] else 0,
        'donations': donations_count,
        'check_target': total_target * 0.25,
        'days': days_diff,
        'rating': average_rating * 20,
        'user_rating': user_rating,
        'rating_range': range(5, 0, -1),
        'average_rating': average_rating,
        'donation_average': donation_average,
        'user': user,
        'project_imgs': imgs,  # Add project images to the context
        'images_before': [img.images_before for img in imgs],  # List of images_before
        'images_after': [img.images_after for img in imgs],  # List of images_after
        'image_count': image_count,
        'replies': replies,
        'reply_form': reply,
        'comments': comments,
        'report_form': new_report_form,

    }
    print(context['images_before'])
    return render(request, 'mainproject/details2.html', context)
#


def delete_project(request, id):
    project = Project.objects.get(id=id)
    donate = project.donation_set.all().aggregate(Sum("donation_amount"))
    donation = donate["donation_amount__sum"] if donate["donation_amount__sum"] else Decimal('0')
    total_target = Decimal(str(project.total_target))  # Convert project.total_target to Decimal

    # Check if donations are less than 25% of the total target
    if donation < total_target * Decimal('0.25'):
        images = Image.objects.filter(project=project)

        for image in images:
            # Remove the images_before file
            if image.images_before:
                image_path_before = image.images_before.path
                if os.path.exists(image_path_before):
                    os.remove(image_path_before)

            # Remove the images_after file
            if image.images_after:
                image_path_after = image.images_after.path
                if os.path.exists(image_path_after):
                    os.remove(image_path_after)

        images.delete()
        project.delete()

        return HttpResponseRedirect('/project/list')
    else:
        # Don't delete the project, maybe show a message or redirect
        # to a different view to handle the case where donations are too high.
        return HttpResponse("Donations are greater than or equal to 25% of the total target.")

def list_project(request):
    context = {}
    projects = Project.objects.all()
    imgs = Image.objects.all()
    context['projects'] = projects
    context['imgs'] = imgs
    return render(request, 'mainproject/list.html', context)


def rate(request, id):
    user = request.user
    if request.method == "POST":
            project = get_object_or_404(Project, pk=id)
            context = {"project": project}

            rate = request.POST.get('rate', '')

            if rate and rate.isnumeric():

                apply_rating(project, user.id, rate)

    return redirect('detailsproject', id)


def apply_rating(project, user, rating):

    # If User rated the same project before --> change rate value
    prev_user_rating = project.rate_set.filter(user_id=user)
    if prev_user_rating:
        prev_user_rating[0].rate = int(rating)
        prev_user_rating[0].save()

    # first time to rate this project
    else:
        Rate.objects.create(
            rate=rating, projcet_id=project.id, user_id=user)


def create_comment(request, project_id):
    user = request.user
    if request.method == "POST":
        if request.POST['comment']:
            comment = Comment.objects.create(
                comment=request.POST['comment'],
                project_id=project_id,
                user_id=user.id
            )
            return redirect('detailsproject', project_id)
    return render(request, "mainproject/details2.html", project_id, context={"user": user})


def create_comment_reply(request, comment_id):
    user = request.user
    if request.method == "POST":
        if request.POST['reply']:
            project = Project.objects.all().filter(comment__id=comment_id)[0]

            reply = Reply.objects.create(
                reply=request.POST['reply'],
                comment_id=comment_id,
                user_id=user.id
            )

            return redirect('detailsproject', project.id)
    return render(request, "mainproject/details2.html", project.id)


def add_report(request, project_id):
    user = request.user
    my_project = Project.objects.get(id=project_id)
    if request.method == "POST":
        Project_Report.objects.create(
            report='ip',
            project=my_project,
            user_id=user.id
        )
        return redirect('detailsproject', project_id)


def add_comment_report(request, comment_id):
    user = request.user
    my_comment = Comment.objects.get(id=comment_id)
    project = Project.objects.all().filter(comment__id=comment_id)[0]

    if request.method == "POST":
        Comment_Report.objects.create(
            report='ip',
            comment=my_comment,
            user_id=user.id
        )
        return redirect('detailsproject', project.id)