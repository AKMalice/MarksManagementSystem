from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from dashboard.models import Admin
from django.shortcuts import redirect
from dashboard.views import dashboard

def home(request):
    return render(request,'home/homepage.html',{})

def login(request):
    if request.method == "POST":
        data = request.POST
        queryset = Admin.objects.filter(Q(username=data.get("username")))
        if len(queryset) == 1:
            if queryset[0].password == data.get("password"):
                request.session['username'] = queryset[0].username
                request.session['uni_name'] = queryset[0].uni_name
                request.session['user']='admin'
                return redirect(dashboard)
            else:
                return render(request,'home/login.html',{"error": "Invalid Password"})
        else:
            return render(request,'home/login.html',{"error": "Invalid Username"})

    else:
        return render(request,'home/login.html',{"registered": None})

def signup(request):

    if request.method == "POST":
        data = request.POST
        if data.get("password") != data.get("confirm_password"):
            return render(request,'home/signup.html',{'error':": Passwords Do Not Match"})
        if len(data.get("password")) <6:
            return render(request,'home/signup.html',{'error':": Password Length Must Be More Than 6 Characters"})
        
        newAdmin = Admin()
        newAdmin.uni_name = data.get("university_name")
        newAdmin.username = data.get("username")
        newAdmin.email = data.get("email")
        newAdmin.password = data.get("password")
        try:
            newAdmin.save()
            return render(request,'home/login.html',{"registered":"Successfuly Registered"})
        except Exception as e:
            e = str(e)
            if "uni_name" in e:
                return render(request,'home/signup.html',{'error':": University Name Already Exists"})
            elif "username" in e:
                return render(request,'home/signup.html',{'error':": Username Already Exists"})
            elif "email" in e:
                return render(request,'home/signup.html',{'error':": Email Already Exists"})
            else:
                return render(request,'home/signup.html',{'error':": An Unkown Error Occurred"})

    else:
        return render(request,'home/signup.html',{'error': None})
