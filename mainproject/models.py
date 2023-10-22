from django.db import models
from django.contrib.auth.models import User
from django.conf import settings




class Catogrey(models.Model):
    
   
    name=models.CharField(max_length=100)


class Project(models.Model):

   
    title=models.CharField(max_length=100)
    details=models.CharField(max_length=100)
    total_target=models.DecimalField(max_digits=10,decimal_places=2)
    creator=models.ForeignKey(User , on_delete=models.CASCADE, blank=True, null=True)
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()
    tags=models.ManyToManyField('Tag')


class Tag(models.Model):    
    name=models.CharField(max_length=100)


class Pictures(models.Model):    
    project_name=models.ForeignKey(Project , on_delete=models.CASCADE, blank=True, null=True)
    images=models.ImageField(upload_to='images/') 


class Comments(models.Model):
    project_name=models.ForeignKey(Project , on_delete=models.CASCADE, blank=True, null=True)
    user_name=models.ForeignKey(User , on_delete=models.CASCADE, blank=True, null=True)
    text=models.TextField()
    replay=models.ForeignKey('self' , on_delete=models.CASCADE, blank=True, null=True)


class Reports(models.Model):
    REPORT_TYPES = (
        ('project', 'Project'),
        ('comment', 'Comment'),
    )
    report_type=models.CharField(max_length=10,choices=REPORT_TYPES)
    user_report=models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True)
