from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    #return HttpResponse("Hello world")
    return render(request,'home/homepage.html',{})
# Create your views here.
