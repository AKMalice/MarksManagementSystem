from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request,'home/homepage.html',{})

def login(request):
    return render(request,'home/login.html',{})

def signup(request):
    return render(request,'home/signup.html',{})
