from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from dashboard.models import Admin,Faculty,Student
from django.shortcuts import redirect
from dashboard.views import dashboard
from home.models import UserList
import bcrypt

def home(request):
    return render(request,'home/homepage.html',{})

def login(request):
    if request.method == "POST":
        data = request.POST
        queryset = UserList.objects.filter(Q(username=data.get("username")))
        if len(queryset) == 1:

            if queryset[0].user_type == "admin":
                user = Admin.objects.filter(Q(username=data.get("username")))
                if user[0].password == data.get("password"):
                    request.session['username'] = user[0].username
                    request.session['uni_name'] = user[0].uni_name
                    request.session['user']='admin'
                    return redirect(dashboard)
                else:
                    return render(request,'home/login.html',{"error": "Invalid Password"})

            elif queryset[0].user_type == "faculty":
                user = Faculty.objects.filter(Q(username=data.get("username")))
                uni_name = Admin.objects.filter(Q(username=user[0].admin_username))[0].uni_name
                if user[0].password == data.get("password"):
                    request.session['username'] = user[0].username
                    request.session['uni_name'] = uni_name
                    request.session['user']='faculty'
                    return redirect(dashboard)
                else:
                    return render(request,'home/login.html',{"error": "Invalid Password"})

            elif queryset[0].user_type == "student":
                user = Student.objects.filter(Q(username=data.get("username")))
                uni_name = Admin.objects.filter(Q(username=user[0].admin_username))[0].uni_name
                if user[0].password == data.get("password"):
                    request.session['username'] = user[0].username
                    request.session['uni_name'] = uni_name
                    request.session['user']='student'
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
        if data.get("password").lower() == data.get("password"):
            return render(request,'home/signup.html',{'error':": Password Must Contain At Least One Uppercase Character"})
        if (data.get("password").isalnum()):
            return render(request,'home/signup.html',{'error':": Password Must Contain At Least One Special Character"})
        
        newAdmin = Admin()
        newAdmin.uni_name = data.get("university_name")
        newAdmin.username = data.get("username")
        newAdmin.email = data.get("email")
        newAdmin.password = data.get("password")
        newUser = UserList()
        newUser.username = data.get("username")
        newUser.user_type="admin"
        # bytes = password.encode('utf-8')
        # salt = bcrypt.gensalt()
        # hashpass = bcrypt.hashpw(bytes, salt)
        # print(hashpass)
        # newAdmin.password = hashpass
        try:
            newAdmin.save()
            newUser.save()
            return render(request,'home/login.html',{"registered":"Successfuly Registered"})
        except Exception as e:
            Admin.objects.filter(Q(username=data.get("username"))).delete()
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
