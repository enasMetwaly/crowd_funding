from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# from apps.authentication.models import Register
from django.contrib.auth.models import User

# from django import forms
# from django.utils import timezone
# from django.db import models

# from django.db import models
# from pkg_resources import require
# # from apps.authentication.models import Register
# # from django.core.validators import MaxValueValidator, MinValueValidator


class Catogrey(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


# class Project(models.Model):
#     title = models.CharField(max_length=100)
#     details = models.TextField()
#     total_target = models.FloatField()
#     start_time = models.DateTimeField(default=timezone.now)
#     end_time = models.DateTimeField(default=timezone.now)
#     is_featured = models.BooleanField(default=False)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     user = models.ForeignKey(Register, on_delete=models.CASCADE)
#     tag = models.ManyToManyField(Tag,null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)



class Project(models.Model):
    title = models.CharField(max_length=100)
    details = models.CharField(max_length=100)
    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    tags = models.ManyToManyField('Tag')
    # images=models.ManyToManyField('Pictures')
    catogrey = models.ForeignKey(Catogrey, on_delete=models.CASCADE, blank=True, null=True)
    is_featured = models.BooleanField(default=False)


class Tag(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name




class Image(models.Model):
    images_before = models.ImageField(upload_to="imgs_before/")
    images_after = models.ImageField(upload_to="imgs_after/", blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

# (venv) PS C:\Users\Enas\Desktop\django\dajanoProject\crowdfunding> python manage.py makemigrations
# CommandError: Conflicting migrations detected; multiple leaf nodes in the migration graph: (0002_comment_comment_report_donation_image_project_report_a
# nd_more, 0002_initial in mainproject).
# To fix them run 'python manage.py makemigrations --merge'




class Comment(models.Model):
    comment = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f'comment by {self.user.first_name} on {self.project.title} project.')


class Donation(models.Model):
    donation_amount = models.FloatField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)



class Project_Report(models.Model):
    REPOT_DATA = [('ip', 'inappropriate'), ('ags', 'aggressive')]
    report = models.CharField(
        max_length=200,
        choices=REPOT_DATA,
        default='ip',
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Comment_Report(models.Model):
    REPOT_DATA = [('ip', 'inappropriate')]
    report = models.CharField(
        max_length=200,
        choices=REPOT_DATA,
        default='ip',
    )
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Reply(models.Model):
    reply = models.CharField(max_length=30)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Rate(models.Model):
    rate = models.IntegerField()
    projcet = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


# # Create your models here.


# class Tag(models.Model):
#     name = models.CharField(max_length=100,null=True, blank=True)

#     def __str__(self):
#         return self.name



#     def __str__(self):
#         return self.title


# class Image(models.Model):
#     images = models.ImageField(upload_to="")
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, default=None)