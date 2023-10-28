from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
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
from django.template import loader
import re
NULL = {}


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




def add_project(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        pictures_form = PicturesForm(request.POST, request.FILES)
        if project_form.is_valid() and pictures_form.is_valid():
            project = project_form.save(commit=False)
            project.creator = request.user  # Assign the current user as the creator
            project.save()
            for image_file in request.FILES.getlist('images'):
                image = Image(images=image_file, project=project)
                image.save()
            return redirect('listproject')
        
    else:
        project_form = ProjectForm()
        pictures_form = PicturesForm(instance=Project())
    return render(request, 'mainproject/add.html', {'project_form': project_form, 'pictures_form': pictures_form})


def donate(request, id):

  
        user = getUser(request)
        if request.method == "POST" and 'donate' in request.POST:
            donation_amount = request.POST['donate']
            donation = Donation.objects.create(
                donation=donation_amount,
                project_id=id,  # Provide the project_id
                user=user  # Assign the user object directly
            )

            return redirect('detailsproject', id)
        return render(request, "mainproject/details.html", {'id': id, 'user': user})












def details_project(request, id):
    project = get_object_or_404(Project, id=id)
    user=getUser(request)
    comments = project.comment_set.all()
    new_report_form = Report_form()
    reply = Reply_form()
    replies = Reply.objects.all()
    donate = project.donation_set.all().aggregate(Sum("donation"))
    donations_count = len(project.donation_set.all())
    donation_average = (donate["donation__sum"] if donate["donation__sum"] else 0)*100/project.total_target
    project_images = project.image_set.all()
    counter=[]
    for image in project_images:
        counter.append("1")
    counter.pop()
    myFormat = "%Y-%m-%d %H:%M:%S"

    today = datetime.strptime(datetime.now().strftime(myFormat), myFormat)
    end_date = datetime.strptime(project.end_time.strftime(myFormat), myFormat)
    days_diff = (end_date-today).days
    donation_average = (donate["donation__sum"] if donate["donation__sum"] else 0)*100/project.total_target
    average_rating = project.rate_set.all().aggregate(Avg('rate'))['rate__avg']

    # return user rating if found
    user_rating = 0
    current_project_tags = project.tags.all()
    related_projects = Project.objects.filter(tags__in=current_project_tags).exclude(id=project.id).distinct()
    related_projects = related_projects.order_by('-start_time')
    related_projects = related_projects[:4]
    
    if 'user_id' in request.session:
        prev_rating = Project.rate_set.get(user_id=user.id)
        prev_rating=[]

        if prev_rating:
            user_rating = prev_rating[0].rate

    if average_rating is None:
        average_rating = 0

    context={
          'current_project_tags': current_project_tags,
          'user': user,
          'days': days_diff,
          'project': project,
          'replies': replies,
          'reply_form': reply,
          'comments': comments,
          
          'user_rating': user_rating,
          'rating': average_rating*20,
          'donations': donations_count,
          'report_form': new_report_form,
          'rating_range': range(5, 0, -1),
          
          'average_rating': average_rating,
          'donation_average': donation_average,
          'related_projects': related_projects,
          'check_target': project.total_target*.25,
          
          'donation': donate["donation__sum"] if donate["donation__sum"] else 0,
          'current_project_tags':current_project_tags,
          'related_projects':related_projects,
             }
    return render(request, 'mainproject/details.html', context)


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




def delete_project(request, id):
    project = Project.objects.get(id=id)
    donate = project.donation_set.all().aggregate(Sum("donation"))
    donation = donate["donation__sum"] if donate["donation__sum"] else 0
    total_target = project.total_target

    # Check if donations are less than 25% of the total target
    if donation < total_target * 0.25:
        images = Image.objects.filter(project=project)
        for image in images:
            image_path = image.images.path
            if os.path.exists(image_path):
                os.remove(image_path)
        images.delete()
        project.delete()
        return HttpResponseRedirect('/main/list')
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
        user = getUser(request)
        if request.method == "POST":
            project = get_object_or_404(Project, pk=id)
            context = {"project": project}

            rate = request.POST.get('rate', '')

            if rate and rate.isnumeric():

                apply_rating(project, user.id, rate)

        return redirect('detailsproject', id)


def apply_rating(project, user, rating):

    prev_user_rating = project.rate_set.filter(user_id=user)
    if prev_user_rating:
        prev_user_rating[0].rate = int(rating)
        prev_user_rating[0].save()

    else:
        Rate.objects.create(
            rate=rating, projcet_id=project.id, user_id=user)
        

def create_comment(request, project_id):
        
    user = getUser(request)
    if request.method == "POST":
        if request.POST['comment']:
            comment = Comment.objects.create(
                comment=request.POST['comment'],
                project_id=project_id,
                user_id=user.id
            )
            return redirect('detailsproject', project_id)
    return render(request, "mainproject/details.html", project_id , context={"user":user})

def create_comment_reply(request, comment_id):
        
        user = getUser(request)
        if request.method == "POST":
            if request.POST['reply']:
                project = Project.objects.all().filter(comment__id=comment_id)[0]

                reply = Reply.objects.create(
                    reply=request.POST['reply'],
                    comment_id=comment_id,
                    user_id=user.id
                )
                return redirect('detailsproject', project.id)
        return render(request, "home/project-details.html", project.id)


def add_report(request, id):
    user = getUser(request)
    my_project = Project.objects.get(id=id)
    if request.method == "POST":
        Project_Report.objects.create(
            report='ip',
            project=my_project,
            user_id=user.id
        )
        return redirect('detailsproject', id)


def add_comment_report(request, comment_id):
    user = getUser(request)
    my_comment = Comment.objects.get(id=comment_id)
    project = Project.objects.all().filter(comment__id=comment_id)[0]

    if request.method == "POST":
        Comment_Report.objects.create(
            report='ip',
            comment=my_comment,
            user_id=user.id
        )
        return redirect('detailsproject', project.id)


def get_tag_projects(request, tag_id):
    if 'user_id' not in request.session:
        user = NULL
    else:
        user = getUser(request)
    context = {}
    try:
        tag = Tag.objects.get(id=tag_id)
        projects = tag.project_set.all()

        donations = []
        progress_values = []
        images = []
        for project in projects:
            donate = project.donation_set.all().aggregate(Sum("donation"))
            total_donation = donate["donation__sum"] if donate["donation__sum"] else 0
            
            progress_values.append(total_donation * 100/project.total_target)
            donations.append(total_donation)
            images.append(project.image_set.all().first().images.url)

        context = {
            'title': tag,
            'projects': projects,
            'images': images,
            'donations': donations,
            'progress_values': progress_values,
            'user':user
        }
        return render(request, "home/tag-projects.html", context)
    except Project.DoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))