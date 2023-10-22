from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View
# Create your views here.



def Home(req):
    return render(req,'index.html',{})
