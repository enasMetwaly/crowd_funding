from django.shortcuts import render
<<<<<<< HEAD

# Create your views here.
=======
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View
# Create your views here.



def Home(req):
    return render(req,'index.html',{})
>>>>>>> aece48664883fc6151c0b1504aa1355af1558de9
