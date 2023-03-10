from django.shortcuts import render
from django.shortcuts import redirect
from dashboard.models import Announcement
from dashboard.models import Faculty
from django.db.models import Q

def dashboard(request):
    if request.session.has_key('user'):
        if request.session['user'] == 'admin':
            return admin_dashboard(request)
        elif request.session['user'] == 'student':
            return student_dashboard(request)
        elif request.session['user'] == 'faculty':
            return faculty_dashboard(request)
    else:
        return redirect('/login')

def logout(request):
    try:
        del request.session['user']
        return redirect('/login')
    except:
        return redirect('/login')


def admin_dashboard(request):
    if request.method == "POST":
        data = request.POST
        newAnnouncement = Announcement()

        newAnnouncement.admin_username = request.session['username']
        newAnnouncement.note = data.get('note')

        try:
            newAnnouncement.save()
            announcementList = Announcement.objects.filter(Q(admin_username=request.session['username']))
            return render(request,'dashboard/admin_dash.html',{"uni_name" : request.session['uni_name'], "success" : "Announcement Sent Sucessfully", "announcementList":reversed(announcementList) if len(announcementList)>0 else None})
        except:
            announcementList = Announcement.objects.filter(Q(admin_username=request.session['username']))
            return render(request,'dashboard/admin_dash.html',{"uni_name" : request.session['uni_name'],"error" : "Failed To Send Announcement", "announcementList":reversed(announcementList) if len(announcementList)>0 else None})

    elif request.session.has_key('username'):
        announcementList = Announcement.objects.filter(Q(admin_username=request.session['username']))
        return render(request,'dashboard/admin_dash.html',{"uni_name" : request.session['uni_name'], "announcementList":reversed(announcementList) if len(announcementList)>0 else None})
    else:
        return redirect('/login')

def admin_faculty(request):
    if request.method == "POST":
        data = request.POST
        newFaculty = Faculty()

        newFaculty.admin_username = request.session['username']
        newFaculty.teacher_id = data.get('teacher_id')
        newFaculty.name = data.get('name')
        newFaculty.email = data.get('email')
        newFaculty.username = data.get('teacher_username')
        newFaculty.password = data.get('password')

        try:
            newFaculty.save()
            facultyList = Faculty.objects.filter(Q(admin_username=request.session['username']))
            return render(request,'dashboard/admin_faculty.html',{"uni_name" : request.session['uni_name'] , "success" : "Faculty Added Successfully","facultyList" : facultyList,"facultyListLength" : len(facultyList)})
        except Exception as e:
            e = str(e)
            if "teacher_id" in e:
                facultyList = Faculty.objects.filter(Q(admin_username=request.session['username']))
                return render(request,'dashboard/admin_faculty.html',{"uni_name" : request.session['uni_name'] , "error" : "Teacher ID Must Be Unique" ,"facultyList" : facultyList,"facultyListLength" : len(facultyList)})
            elif "email" in e:
                facultyList = Faculty.objects.filter(Q(admin_username=request.session['username']))
                return render(request,'dashboard/admin_faculty.html',{"uni_name" : request.session['uni_name'] , "error" : "Email Must Be Unique" ,"facultyList" : facultyList,"facultyListLength" : len(facultyList)})
            elif "username" in e:
                facultyList = Faculty.objects.filter(Q(admin_username=request.session['username']))
                return render(request,'dashboard/admin_faculty.html',{"uni_name" : request.session['uni_name'] , "error" : "Username Must Be Unique" ,"facultyList" : facultyList,"facultyListLength" : len(facultyList)})
            else:
                facultyList = Faculty.objects.filter(Q(admin_username=request.session['username']))
                return render(request,'dashboard/admin_faculty.html',{"uni_name" : request.session['uni_name'] , "error" : "Something Went Wrong" ,"facultyList" : facultyList,"facultyListLength" : len(facultyList)})

    elif request.session.has_key('user') and request.session['user'] == 'admin':
        facultyList = Faculty.objects.filter(Q(admin_username=request.session['username']))
        return render(request,'dashboard/admin_faculty.html',{"uni_name" : request.session['uni_name'] ,"facultyList" : facultyList,"facultyListLength" : len(facultyList)})
    else:
        return redirect('/login')


def student_dashboard(request):
    pass


def faculty_dashboard(request):
    pass
