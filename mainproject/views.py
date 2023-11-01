from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
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
from django.template import loader
import re
from django.shortcuts import render, redirect
from .forms import ProjectForm
from .models import Project, Tag, Catogrey

from .models import Catogrey, Project, Image
from django.db.models import Avg

from .forms import ProjectForm, PicturesForm  # Make sure to import your ProjectForm and PicturesForm

import os
from decimal import Decimal  # Import Decimal from the decimal module
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.db.models import Q
from django.shortcuts import render
from .models import Project, Tag

from django.http import HttpResponseNotFound
from django.db.models import Q, Sum
from django.shortcuts import render
from .models import Project, Tag
from django.urls import reverse
from django.db.models import Q


def my_view(request):
    user = request.user
    return HttpResponse(f"Hello, {user}!")





def home_page(req):
    latest_projects = Project.objects.order_by('start_time')[:5]
    # Select 5 featured projects
    featured_projects = Project.objects.filter(is_featured=True)[:5]

    # Calculate the average rating for each project and annotate it
    top_rated_projects = Project.objects.annotate(
        average_rating=Avg('rate__rate')
    ).exclude(average_rating=None).order_by('-average_rating')[:5]

    imgs = Image.objects.all()
    all_projects=Project.objects.all()

    # Get all categories
    categories = Catogrey.objects.all()

    # Create a dictionary to store projects for each category
    category_projects = {}
    print("Latest Projects: " + str(latest_projects))
    print("Images: " + str(imgs))

    print("all projects: " + str(all_projects))

    for category in categories:
        projects = Project.objects.filter(catogrey=category)
        category_projects[category] = projects
    print("category_projects: " + str(category_projects))


    return render(req, 'index.html', {
        'latest_projects': latest_projects,
        'imgs': imgs,
        'top_rated_projects': top_rated_projects,
        'categories': categories,
        'category_projects': category_projects,
        'all_projects':all_projects,
        'featured_projects':featured_projects
    })








@login_required
def add_project(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        pictures_form = PicturesForm(request.POST, request.FILES)

        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.creator = request.user

            # Check if an existing category was selected
            selected_category_id = request.POST.get('category')
            if selected_category_id:
                project.catogrey = Catogrey.objects.get(pk=selected_category_id)
            else:
                # If no existing category was selected, check if a new category was provided
                new_category_name = request.POST.get('newCategory')
                if new_category_name:
                    new_category, created = Catogrey.objects.get_or_create(name=new_category_name)
                    project.catogrey = new_category

            # Save the project to generate an ID
            project.save()

            # Handle selected tags
            selected_tags = request.POST.getlist('tags')
            project.tags.set(selected_tags)  # Set the selected tags for the project

            # Handle new tags
            new_tags = request.POST.getlist('newTag')
            for tag_name in new_tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                project.tags.add(tag)

            images_before = request.FILES.getlist('images_before')
            images_after = request.FILES.getlist('images_after')

            for image in images_before:
                image_obj = Image.objects.create(images_before=image, project=project)
                image_obj.save()

            for image in images_after:
                image_obj = Image.objects.create(images_after=image, project=project)
                image_obj.save()

            return HttpResponseRedirect(reverse('listproject'))
        else:
            print("Form is not valid")
    else:
        project_form = ProjectForm()
        pictures_form = PicturesForm()

    return render(request, 'mainproject/add.html', {'project_form': project_form, 'pictures_form': pictures_form})



def list_project(request):
    context={}
    projects=Project.objects.all()
    imgs=Image.objects.all()
    context['projects']=projects
    context['imgs']=imgs
    # project = get_object_or_404(Project, id=id)
    return render(request, 'mainproject/list.html', context)

@login_required

def donate(request, id):
    user = request.user
    if request.method == "POST" and 'donate' in request.POST:
        donation_amount = request.POST['donate']
        donation = Donation.objects.create(
            donation_amount=donation_amount,  # Correct field name to 'donation_amount'
            project_id=id,  # Provide the project_id
            user=user  # Assign the user object directly
        )

        return redirect('detailsproject', id)
    return render(request, "mainproject/donate.html", {'id': id, 'user': user})



def details_project(request, id):
    project = get_object_or_404(Project, id=id)
    user = request.user
    donate = project.donation_set.all().aggregate(Sum("donation_amount"))
    donations_count = len(project.donation_set.all())

    # Convert the project total_target to a float
    total_target = float(project.total_target)
    donation_average = (donate["donation_amount__sum"] if donate["donation_amount__sum"] else 0) * 100 / total_target
    all_imgs=Image.objects.all()

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

    current_project_tags = project.tags.all()
    related_projects = Project.objects.filter(tags__in=current_project_tags).exclude(id=project.id).distinct()
    related_projects = related_projects.order_by('-start_time')
    related_projects = related_projects[:4]
    print("Related Projects:")
    print(related_projects)
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
        'current_project_tags': current_project_tags,
        'related_projects': related_projects,
        'all_imgs':all_imgs

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

@login_required

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

@login_required

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

@login_required

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







def get_tag_projects(request, tag_name):
    if 'user_id' not in request.session:
        user = None
    else:
        user = request.user

    try:
        # Get similar projects based on the tag name or title
        similar_projects = Project.objects.filter(
            Q(tags__name=tag_name) | Q(title__icontains=tag_name)
        ).distinct()

        imgs = Image.objects.all()
        print(imgs)

        context = {
            'title': tag_name,  # Use tag_name as the title
            'similar_projects': similar_projects,
            'user': user,
            'imgs':imgs,
        }
        return render(request, "mainproject/search_result.html", context)
    except Tag.DoesNotExist:
        return HttpResponseNotFound("Page not found")
