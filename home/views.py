from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from dashboard.models import Admin,Faculty,Student
from django.shortcuts import redirect
from dashboard.views import dashboard
from home.models import *
import bcrypt
from django.core.mail import send_mail
from password_generator import PasswordGenerator


def forgotpassword(request):
    if request.method == "POST":
        data = request.POST

        if data.get("username") in ["guestadmin","guestfaculty","gueststudent"]:
            return render(request,'home/forgotpassword.html',{"error": "Modifications Are Not Supported On Guest Account"})

        queryset = UserList.objects.filter(Q(username=data.get("username")))
        if len(queryset) == 1:
            user = queryset[0]
            emailAdd = None
            curusername = None
            if(user.user_type == "admin"):
                user_query = Admin.objects.filter(Q(username = user.username))
                emailAdd = user_query[0].email;
                curusername = user_query[0].username;
            
            if(user.user_type == "student"):
                user_query = Student.objects.filter(Q(username = user.username))
                emailAdd = user_query[0].email;
                curusername = user_query[0].username;
            
            if(user.user_type == "faculty"):
                user_query = Faculty.objects.filter(Q(username = user.username))
                emailAdd = user_query[0].email;
                curusername = user_query[0].username;
            
            pwo = PasswordGenerator()
            pwo.excludeschars = "[$&+,:;=#|'<>.-^*()%!]" 
            newPassword=pwo.generate()
            send_mail(
            'NOVA RESET PASSWORD',
            'Here is your new password to NOVA Marks Management System \n' + 'Username : ' + user.username + '\n' + 'New password : ' + newPassword +'\n' + 'Login here : ' + 'https://akmalice.pythonanywhere.com/login',                      
            'novamarksmanagement@gmail.com',
            [emailAdd],
            fail_silently=False,
            )
            if(user.user_type == "student"):
             Student.objects.filter(username = curusername).update(password = newPassword)
            
            if(user.user_type == "faculty"):
                Faculty.objects.filter(username = curusername).update(password = newPassword)
            
            if(user.user_type == "admin"):
                Admin.objects.filter(username = curusername).update(password = newPassword)

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

def reset_password(request,token):
    if request.method == "POST":

        tokenDetails = PassToken.objects.filter(Q(token=token))[0]

        if tokenDetails.username in ["guestadmin","guestfaculty","gueststudent"]:
            return render(request,'home/reset_password.html',{"expired": "Modifications Are Not Supported On Guest Account"})

    
        if request.POST['password1']!=request.POST['password2']:
            return render(request,'home/reset_password.html',{"error":"Passwords Do Not Match"})
        elif len(request.POST['password1']) <6:
            return render(request,'home/reset_password.html',{"error":"Password Length Must Be More Than 6 Characters"})
        elif request.POST['password1'].lower() == request.POST['password1']:
            return render(request,'home/reset_password.html',{"error":"Password Must Contain At Least One Uppercase Character"})
        elif request.POST['password1'].isalnum():
            return render(request,'home/reset_password.html',{"error":"Password Must Contain At Least One Special Character"})
        
        if tokenDetails.user_type == "admin":
            user = Admin.objects.filter(Q(username=tokenDetails.username))[0]
            user.password = request.POST['password1']
            user.save()
        elif tokenDetails.user_type == "faculty":
            user = Faculty.objects.filter(Q(username=tokenDetails.username))[0]
            user.password = request.POST['password1']
            user.save()
        elif tokenDetails.user_type == "student":
            user = Student.objects.filter(Q(username=tokenDetails.username))[0]
            user.password = request.POST['password1']
            user.save()

        PassToken.objects.filter(Q(token=token)).delete()
        return render(request,'home/reset_password.html',{"success":"Password Reset Successfully"})

    else:
        tokenDetails = PassToken.objects.filter(Q(token=token))
        if len(tokenDetails) == 1:
            return render(request,'home/reset_password.html',{})
        else:
            return render(request,'home/reset_password.html',{"expired": "Your Token Has Expired"})