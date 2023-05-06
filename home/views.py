from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from dashboard.models import Admin
from dashboard.models import Student
from django.shortcuts import redirect
from dashboard.views import dashboard
import bcrypt
from django.core.mail import send_mail
from password_generator import PasswordGenerator


def forgotpassword(request):
    if request.method == "POST":
        data = request.POST
        queryset = Student.objects.filter(Q(username=data.get("username")))
        if len(queryset) == 1:
            emailAdd = queryset[0].email;
            password = "1234"
            user = queryset[0];
            curusername = user.username
            pwo = PasswordGenerator()
            pwo.excludeschars = "[$&+,:;=#|'<>.-^*()%!]" 
            newPassword=pwo.generate()
            send_mail(
            'NOVA RESET PASSWORD',
            'Here is your new password to NOVA Marks Management System \n' + 'Username : ' + user.username + '\n' + 'New password : ' + newPassword +'\n' + 'Login here : ' + 'https://akmalice.pythonanywhere.com/login',                      
            'novamarks123@gmail.com',
            [emailAdd],
            fail_silently=False,
            )
            Student.objects.filter(username = curusername).update(password = newPassword)
            return render(request,'home/forgotpassword.html',{"success" : "Email has been sent"})
        else:
            return render(request,'home/forgotpassword.html',{"error": "Invalid Username"})
    else:
      return render(request,'home/forgotpassword.html',{})

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
        if data.get("password").lower() == data.get("password"):
            return render(request,'home/signup.html',{'error':": Password Must Contain At Least One Uppercase Character"})
        if (data.get("password").isalnum()):
            return render(request,'home/signup.html',{'error':": Password Must Contain At Least One Special Character"})
        
        newAdmin = Admin()
        newAdmin.uni_name = data.get("university_name")
        newAdmin.username = data.get("username")
        newAdmin.email = data.get("email")
        newAdmin.password = data.get("password")
        # bytes = password.encode('utf-8')
        # salt = bcrypt.gensalt()
        # hashpass = bcrypt.hashpw(bytes, salt)
        # print(hashpass)
        # newAdmin.password = hashpass
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
