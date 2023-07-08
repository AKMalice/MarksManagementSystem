from django.shortcuts import render
from django.shortcuts import redirect
from dashboard.models import *
from home.models import *
from django.core.mail import send_mail
from django.db.models import Q
from datetime import datetime
import string
import random

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
        newAnnouncement.time = datetime.now()

        try:
            if request.session['username'] == "guestadmin":
                raise Exception("!Modification Of Guest Account Is Not Supported")

            newAnnouncement.save()
            announcementList = Announcement.objects.filter(Q(admin_username=request.session['username'])).order_by('-time')
            issueList = Issue.objects.filter(Q(admin_username=request.session['username']) & Q(status="pending"))
            return render(request,'dashboard/admin_dash.html',{"uni_name" : request.session['uni_name'], "success" : "Announcement Sent Sucessfully", "announcementList":announcementList if len(announcementList)>0 else None,"issueCount":len(issueList)})
        except Exception as e:
            e = str(e)
            error = "Failed To Send Announcement"
            if e[0] == '!':
                error = e[1:]
            announcementList = Announcement.objects.filter(Q(admin_username=request.session['username'])).order_by('-time')
            issueList = Issue.objects.filter(Q(admin_username=request.session['username']) & Q(status="pending"))
            return render(request,'dashboard/admin_dash.html',{"uni_name" : request.session['uni_name'],"error" : error, "announcementList":announcementList if len(announcementList)>0 else None,"issueCount":len(issueList)})

    elif request.session.has_key('user') and request.session['user'] == 'admin':
        announcementList = Announcement.objects.filter(Q(admin_username=request.session['username'])).order_by('-time')
        issueList = Issue.objects.filter(Q(admin_username=request.session['username']) & Q(status="pending"))
        return render(request,'dashboard/admin_dash.html',{"uni_name" : request.session['uni_name'], "announcementList":announcementList if len(announcementList)>0 else None,"issueCount":len(issueList)})
    else:
        return redirect('/login')

def admin_profile(request):
    if request.method == "POST":
        characters = string.ascii_letters + string.digits
        tkn = ''.join(random.choice(characters) for _ in range(20))
        newToken = PassToken()
        newToken.user_type = request.session['user']
        newToken.username = request.session['username']
        newToken.token = tkn

        try:
            if request.session['username'] == "guestadmin":
                raise Exception("!Modification Of Guest Account Is Not Supported")
            adminDetails = Admin.objects.filter(Q(username=request.session['username']))
            adminDetails = adminDetails[0]
            send_mail(
                'NOVA Password Reset Link',
                'Your Requested Link for Password Reset is : '+'https://akmalice.pythonanywhere.com/reset-password/'+tkn,
                'novamarksmanagement@gmail.com',
                [adminDetails.email],
                    fail_silently=False,
                )
            newToken.save()

            return render(request,'dashboard/admin_profile.html',{"uni_name" : request.session['uni_name'],"adminDetails":adminDetails,"success":"Reset Link Sent Successfully"})
        except Exception as e:
            e = str(e)
            error = "Something Went Wrong"
            if e[0] == '!':
                error = e[1:]
            adminDetails = Admin.objects.filter(Q(username=request.session['username']))
            adminDetails = adminDetails[0]
            return render(request,'dashboard/admin_profile.html',{"uni_name" : request.session['uni_name'],"adminDetails":adminDetails,"error":error})

    elif request.session.has_key('user') and request.session['user'] == 'admin':
        adminDetails = Admin.objects.filter(Q(username=request.session['username']))
        adminDetails = adminDetails[0]
        return render(request,'dashboard/admin_profile.html',{"uni_name" : request.session['uni_name'],"adminDetails":adminDetails})
    else:
        return redirect('/login')

def admin_faculty(request):
    if request.method == "POST":
        data = request.POST
        courseCount = Section.objects.filter(Q(admin_username=request.session['username'])).values('course_id').distinct().count()
        newFaculty = Faculty()

        newFaculty.admin_username = request.session['username']
        newFaculty.teacher_id = data.get('teacher_id').replace(" ", "")
        newFaculty.name = data.get('name')
        newFaculty.email = data.get('email')
        newFaculty.username = data.get('teacher_username')
        newFaculty.password = data.get('password')

        newUser = UserList()
        newUser.username = data.get('teacher_username')
        newUser.user_type = 'faculty'

        try:
            if request.session['username'] == "guestadmin":
                raise Exception("!Modification Of Guest Account Is Not Supported")

            newFaculty.save()
            send_mail(
                'NOVA Invitation',
                'You Have Been Invited To Join NOVA You Can Login Using the Following Credentials :\n '+'Username : '+newFaculty.username+'\n'+'Password : '+newFaculty.password+'\nLogin Here : https://akmalice.pythonanywhere.com/login',
                'novamarksmanagement@gmail.com',
                [newFaculty.email],
                 fail_silently=False,
            )
            newUser.save()

            facultyList = Faculty.objects.filter(Q(admin_username=request.session['username']))
            return render(request,'dashboard/admin_faculty.html',{"uni_name" : request.session['uni_name'] , "success" : "Faculty Added Successfully","facultyList" : facultyList,"facultyListLength" : len(facultyList),"courseCount" : courseCount})

        except Exception as e:
            Faculty.objects.filter(Q(admin_username=request.session['username']) & Q(teacher_id=newFaculty.teacher_id)).delete()
            e = str(e)
            error = "Something Went Wrong"
            if "email" in e:
                error="Email Must Be Unique"
            elif "username" in e:
                error="Username Must Be Unique"
            elif e[0] == '!':
                error = "Modification Of Guest Account Is Not Supported"

            facultyList = Faculty.objects.filter(Q(admin_username=request.session['username']))
            return render(request,'dashboard/admin_faculty.html',{"uni_name" : request.session['uni_name'] , "error" : error ,"facultyList" : facultyList,"facultyListLength" : len(facultyList),"courseCount" : courseCount})

    elif request.session.has_key('user') and request.session['user'] == 'admin':
        courseCount = Section.objects.filter(Q(admin_username=request.session['username'])).values('course_id').distinct().count()
        facultyList = Faculty.objects.filter(Q(admin_username=request.session['username']))
        return render(request,'dashboard/admin_faculty.html',{"uni_name" : request.session['uni_name'] ,"facultyList" : facultyList,"facultyListLength" : len(facultyList),"courseCount" : courseCount})
    else:
        return redirect('/login')

def admin_faculty_details(request,id):
    if request.method == "POST":
        data = request.POST
        newSection = Section()
        faculty = Faculty.objects.filter(Q(admin_username=request.session['username']) & Q(teacher_id=id))
        faculty = faculty[0]

        newSection.admin_username = request.session['username']
        newSection.teacher_id = faculty.teacher_id
        newSection.teacher_name = faculty.name
        newSection.course_id = data.get('course_id').replace(" ", "")
        newSection.course_name = data.get('course_name')
        newSection.section_name = data.get('section_name')
        newSection.year = data.get('year')
        newSection.section_id =  (newSection.year + newSection.course_id + newSection.section_name).replace(" ","")

        try:
            if request.session['username'] == "guestadmin":
                raise Exception("!Modification Of Guest Account Is Not Supported")
            newSection.save()
            sectionList = Section.objects.filter(Q(admin_username=request.session['username']) & Q(teacher_id=id) & Q(active=True))
            courseCount = sectionList.values('course_id').distinct().count()
            return render(request,'dashboard/admin_faculty_details.html',{"uni_name" : request.session['uni_name'] ,"faculty" : faculty,"success" : "Section Added Successfully", "sectionList" : sectionList, "sectionCount" : len(sectionList), "courseCount" : courseCount})
        except Exception as e:
            e = str(e)
            error = "Something Went Wrong"
            if e[0] == '!':
                error = "Modification Of Guest Account Is Not Supported"
            sectionList = Section.objects.filter(Q(admin_username=request.session['username']) & Q(teacher_id=id) & Q(active=True))
            courseCount = sectionList.values('course_id').distinct().count()
            return render(request,'dashboard/admin_faculty_details.html',{"uni_name" : request.session['uni_name'] ,"faculty" : faculty,"error":error, "sectionList" : sectionList, "sectionCount" : len(sectionList), "courseCount" : courseCount})

    elif request.session.has_key('user') and request.session['user'] == 'admin':
        faculty = Faculty.objects.filter(Q(admin_username=request.session['username']) & Q(teacher_id=id))
        faculty = faculty[0]
        sectionList = Section.objects.filter(Q(admin_username=request.session['username']) & Q(teacher_id=id) &Q(active=True))
        courseCount = sectionList.values('course_id').distinct().count()
        return render(request,'dashboard/admin_faculty_details.html',{"uni_name" : request.session['uni_name'] ,"faculty" : faculty, "sectionList" : sectionList, "sectionCount" : len(sectionList), "courseCount" : courseCount})
    else:
        return redirect('/login')

def admin_faculty_details_delete(request,id,section):
    if request.session.has_key('user') and request.session['user'] == 'admin':
        try:
            if request.session['username'] == "guestadmin":
                raise Exception("!Modification Of Guest Account Is Not Supported")
            Section.objects.filter(section_id=section).update(active=False)
            return redirect('faculty-details',id=id)
        except:
            return redirect('faculty-details',id=id)
    else:
        return redirect('/login')

def admin_students(request):
    if request.method == "POST":
        data = request.POST
        courseCount = Section.objects.filter(Q(admin_username=request.session['username'])).values('course_id').distinct().count()
        newStudent = Student()

        newStudent.admin_username = request.session['username']
        newStudent.student_id = data.get('student_id').replace(" ", "")
        newStudent.name = data.get('name')
        newStudent.email = data.get('email')
        newStudent.username = data.get('student_username')
        newStudent.password = data.get('password')

        newUser = UserList()
        newUser.username = data.get('student_username')
        newUser.user_type = 'student'

        try:
            if request.session['username'] == "guestadmin":
                raise Exception("!Modification Of Guest Account Is Not Supported")
            newStudent.save()
            send_mail(
                'NOVA Invitation',
                'You Have Been Invited To Join NOVA You Can Login Using the Following Credentials :\n '+'Username : '+newStudent.username+'\n'+'Password : '+newStudent.password+'\nLogin Here : https://akmalice.pythonanywhere.com/login',
                'novamarksmanagement@gmail.com',
                [newStudent.email],
                 fail_silently=False,
            )
            newUser.save()

            studentList = Student.objects.filter(Q(admin_username=request.session['username']))
            return render(request,'dashboard/admin_students.html',{"uni_name" : request.session['uni_name'] , "success" : "Student Added Successfully","studentList" : studentList,"studentListLength" : len(studentList),"courseCount" : courseCount})
            
        except Exception as e:
            Student.objects.filter(Q(admin_username=request.session['username']) & Q(student_id=newStudent.student_id)).delete()
            e = str(e)
            error = "Something Went Wrong"
            if "email" in e:
                error = "Email Must Be Unique"
            elif "username" in e:
                error = "Username Must Be Unique"
            elif e[0] == '!':
                error = "Modification Of Guest Account Is Not Supported"
            
            studentList = Student.objects.filter(Q(admin_username=request.session['username']))
            return render(request,'dashboard/admin_students.html',{"uni_name" : request.session['uni_name'] , "error" : error ,"studentList" : studentList,"studentListLength" : len(studentList),"courseCount" : courseCount})

    elif request.session.has_key('user') and request.session['user'] == 'admin':
        courseCount = Section.objects.filter(Q(admin_username=request.session['username'])).values('course_id').distinct().count()
        studentList = Student.objects.filter(Q(admin_username=request.session['username']))
        return render(request,'dashboard/admin_students.html',{"uni_name" : request.session['uni_name'] ,"studentList" : studentList,"studentListLength" : len(studentList),"courseCount" : courseCount})
    else:
        return redirect('/login')
    
def admin_student_details(request,id):
    if request.method == "POST":
        data = request.POST
        newClass = Classe()

        newClass.admin_username = request.session['username']
        newClass.student_id = id
        newClass.year = data.get('year')
        newClass.section_id =  (newClass.year + data.get('course_id') + data.get('section_name')).replace(" ","")

        try:
            if request.session['username'] == "guestadmin":
                raise Exception("!Modification Of Guest Account Is Not Supported")
            newClass.save()
            student = Student.objects.filter(Q(admin_username=request.session['username']) & Q(student_id=id))
            student = student[0]
            classList = Classe.objects.filter(Q(admin_username=request.session['username']) & Q(student_id=id))
            sectionList = []
            sectionListComp = []
            for Class in classList:
                sectionList.append(Section.objects.filter(Q(admin_username=request.session['username']) & Q(section_id=Class.section_id)))
            for sec in sectionList:
                if len(sec)>=1:
                    sectionListComp.append(sec[0])
            return render(request,'dashboard/admin_student_details.html',{"uni_name" : request.session['uni_name'] ,"student" : student,"classList" : classList, "courseCount" : len(classList),"sectionList" : sectionListComp,"success": "Section Added Successfully"})
        except Exception as e:
            e = str(e)
            error = "Something Went Wrong"
            if e[0] == '!':
                error = "Modification Of Guest Account Is Not Supported"
            student = Student.objects.filter(Q(admin_username=request.session['username']) & Q(student_id=id))
            student = student[0]
            classList = Classe.objects.filter(Q(admin_username=request.session['username']) & Q(student_id=id))
            sectionList = []
            sectionListComp = []
            for Class in classList:
                sectionList.append(Section.objects.filter(Q(admin_username=request.session['username']) & Q(section_id=Class.section_id)))
            for sec in sectionList:
                if len(sec)>=1:
                    sectionListComp.append(sec[0])
            return render(request,'dashboard/admin_student_details.html',{"uni_name" : request.session['uni_name'] ,"student" : student,"classList" : classList, "courseCount" : len(classList),"sectionList" : sectionListComp,"error":error})

    elif request.session.has_key('user') and request.session['user'] == 'admin':
        student = Student.objects.filter(Q(admin_username=request.session['username']) & Q(student_id=id))
        student = student[0]
        classList = Classe.objects.filter(Q(admin_username=request.session['username']) & Q(student_id=id))
        sectionList = []
        sectionListComp = []
        for Class in classList:
            sectionList.append(Section.objects.filter(Q(admin_username=request.session['username']) & Q(section_id=Class.section_id)))
        for sec in sectionList:
            if len(sec)>=1:
                sectionListComp.append(sec[0])

        return render(request,'dashboard/admin_student_details.html',{"uni_name" : request.session['uni_name'] ,"student" : student,"classList" : classList, "courseCount" : len(classList),"sectionList" : sectionListComp})
    else:
        return redirect('/login')

def admin_issues(request):
    if request.session.has_key('user') and request.session['user'] == 'admin':
        issueList = Issue.objects.filter(Q(admin_username=request.session['username']) & Q(status="pending")).order_by('-time')
        return render(request,'dashboard/admin_issues.html',{"uni_name" : request.session['uni_name'] ,"issueList" : issueList})
    else :
        return redirect('/login')

def admin_issue_details(request,student_id,issue_id):
    if request.session.has_key('user') and request.session['user'] == 'admin':
        studentDetails = Student.objects.filter(Q(admin_username=request.session['username']) & Q(student_id=student_id))
        studentDetails = studentDetails[0]
        issueDetails = Issue.objects.filter(Q(admin_username=request.session['username']) & Q(pk=issue_id))
        issueDetails = issueDetails[0]
        return render(request,'dashboard/admin_issues_student_details.html',{"uni_name" : request.session['uni_name'],"studentDetails" : studentDetails,"issueDetails" : issueDetails})
    else :
        return redirect('/login')

def admin_issue_resolved(request,student_id,issue_id):
    if request.session.has_key('user') and request.session['user'] == 'admin':
        try:
            if request.session['username'] == "guestadmin":
                raise Exception("!Modification Of Guest Account Is Not Supported")
            Issue.objects.filter(Q(admin_username=request.session['username']) & Q(pk=issue_id)).update(status="resolved")
            return redirect('issues')
        except:
            return redirect('issues')
    else:
        return redirect('/login')

def admin_issue_dismissed(request,student_id,issue_id):
    if request.session.has_key('user') and request.session['user'] == 'admin':
        try:
            if request.session['username'] == "guestadmin":
                raise Exception("!Modification Of Guest Account Is Not Supported")
            Issue.objects.filter(Q(admin_username=request.session['username']) & Q(pk=issue_id)).update(status="dismissed")
            return redirect('issues')
        except:
            return redirect('issues')
    else:
        return redirect('/login')

def faculty_dashboard(request):
    if request.session.has_key('user') and request.session['user'] == 'faculty':

        facultyDetails = Faculty.objects.filter(Q(username=request.session['username']))
        facultyDetails = facultyDetails[0]

        announcementList = Announcement.objects.filter(Q(admin_username=facultyDetails.admin_username)).order_by('-time')

        sectionList = Section.objects.filter(Q(admin_username=facultyDetails.admin_username) & Q(teacher_id=facultyDetails.teacher_id) & Q(active=True))
        courseCount = sectionList.values('course_id').distinct().count()
        sectionCount = len(sectionList)
        studentCount = 0
        for section in sectionList:
            studentCount += Section.objects.filter(Q(admin_username=facultyDetails.admin_username) & Q(section_id=section.section_id) & Q(active=True)).count()

        return render(request,'dashboard/faculty_dash.html',{"uni_name" : request.session['uni_name'],"announcementList" : announcementList,"sectionCount" : sectionCount,"courseCount" : courseCount,"studentCount" : studentCount})
    else:
        return redirect('/login')

def faculty_classes(request):
    print(request.session['user'])
    if request.session.has_key('user') and request.session['user'] == 'faculty':
        
        facultyDetails = Faculty.objects.filter(Q(username=request.session['username']))
        facultyDetails = facultyDetails[0]

        classList = Section.objects.filter(Q(admin_username=facultyDetails.admin_username) & Q(teacher_id=facultyDetails.teacher_id)).order_by('-active')

        return render(request,'dashboard/faculty-classes.html',{"uni_name" : request.session['uni_name'],"classList" : classList})
    else :
        return redirect('/login')
    
def faculty_profile(request):
    if request.method == "POST":
        characters = string.ascii_letters + string.digits
        tkn = ''.join(random.choice(characters) for _ in range(20))
        newToken = PassToken()
        newToken.user_type = request.session['user']
        newToken.username = request.session['username']
        newToken.token = tkn

        try:
            facultyDetails = Faculty.objects.filter(Q(username=request.session['username']))
            facultyDetails = facultyDetails[0]

            if request.session['username'] == "guestfaculty":
                raise Exception("!Modification Of Guest Account Is Not Supported")
            send_mail(
                'NOVA Password Reset Link',
                'Your Requested Link for Password Reset is : '+'https://akmalice.pythonanywhere.com/reset-password/'+tkn,
                'novamarksmanagement@gmail.com',
                [facultyDetails.email],
                    fail_silently=False,
                )
            newToken.save()

            return render(request,'dashboard/faculty-profile.html',{"uni_name" : request.session['uni_name'],"facultyDetails" : facultyDetails,"success":"Reset Link Sent Successfully"})
        except Exception as e:
            error = "Something Went Wrong"
            e = str(e)
            if e[0]=='!':
                error = e[1:]
            facultyDetails = Faculty.objects.filter(Q(username=request.session['username']))
            facultyDetails = facultyDetails[0]
            return render(request,'dashboard/faculty-profile.html',{"uni_name" : request.session['uni_name'],"facultyDetails" : facultyDetails,"error":error})

    elif request.session.has_key('user') and request.session['user'] == 'faculty':

        facultyDetails = Faculty.objects.filter(Q(username=request.session['username']))
        facultyDetails = facultyDetails[0]

        return render(request,'dashboard/faculty-profile.html',{"uni_name" : request.session['uni_name'],"facultyDetails" : facultyDetails})
    else :
        return redirect('/login')
    
def student_dashboard(request):

    if request.session.has_key('user') and request.session['user'] == 'student':

        studentDetails = Student.objects.filter(Q(username=request.session['username']))
        studentDetails = studentDetails[0]

        announcementList = Announcement.objects.filter(Q(admin_username=studentDetails.admin_username)).order_by('-time')

        classList = Classe.objects.filter(Q(admin_username=studentDetails.admin_username) & Q(student_id=studentDetails.student_id))
        courseCount = 0
        for classObj in classList:
            sectionObj = Section.objects.filter(Q(admin_username=studentDetails.admin_username) & Q(section_id=classObj.section_id))
            if len(sectionObj) and sectionObj[0].active == True:
                courseCount +=1

        return render(request,'dashboard/student_dash.html',{'uni_name':request.session['uni_name'],'announcementList':announcementList,'courseCount':courseCount})
    else :
        return redirect('/login')

def student_classes(request):
    if request.session.has_key('user') and request.session['user'] == 'student':

        studentDetails = Student.objects.filter(Q(username=request.session['username']))
        studentDetails = studentDetails[0]

        classList = Classe.objects.filter(Q(admin_username=studentDetails.admin_username) & Q(student_id=studentDetails.student_id))
        sectionList = []
        for classObj in classList:
            sectionObj = Section.objects.filter(Q(admin_username=studentDetails.admin_username) & Q(section_id=classObj.section_id))
            if len(sectionObj)>=1:
                sectionList.append(sectionObj[0]) 


        sectionList.sort(key=lambda x:x.active,reverse=True)

        return render(request,'dashboard/student-classes.html',{'uni_name':request.session['uni_name'],'sectionList':sectionList})
    else :
        return redirect('/login')

def student_raise_issue(request):
    if request.session.has_key('user') and request.session['user'] == 'student':
        if request.method == 'POST':
            studentDetails = Student.objects.filter(Q(username=request.session['username']))
            studentDetails = studentDetails[0]
            try:
                if request.session['username'] == "gueststudent":
                    raise Exception("!Modification Of Guest Account Is Not Supported")

                issue = Issue()
                issue.admin_username = studentDetails.admin_username
                issue.student_id = studentDetails.student_id
                issue.issue = request.POST['issue']
                issue.status = "pending"
                issue.time = datetime.now()
                issue.save()

                issueList = Issue.objects.filter(Q(admin_username=studentDetails.admin_username) & Q(student_id=studentDetails.student_id)).order_by('-time')
                pendingIssues = issueList.filter(Q(status="pending")).count()
                return render(request,'dashboard/student-raise-issue.html',{'uni_name':request.session['uni_name'],'issueList':issueList,'pendingIssues':pendingIssues,'success':'Issue Raised Successfully'})
            except Exception as e:
                error = "Something Went Wrong"
                e = str(e)
                if e[0] =='!':
                    error = e[1:]
                issueList = Issue.objects.filter(Q(admin_username=studentDetails.admin_username) & Q(student_id=studentDetails.student_id)).order_by('-time')
                pendingIssues = issueList.filter(Q(status="pending")).count()
                return render(request,'dashboard/student-raise-issue.html',{'uni_name':request.session['uni_name'],'issueList':issueList,'pendingIssues':pendingIssues,'error':error})
        else:

            studentDetails = Student.objects.filter(Q(username=request.session['username']))
            studentDetails = studentDetails[0]
            
            issueList = Issue.objects.filter(Q(admin_username=studentDetails.admin_username) & Q(student_id=studentDetails.student_id)).order_by('-time')
            pendingIssues = issueList.filter(Q(status="pending")).count()

            return render(request,'dashboard/student-raise-issue.html',{'uni_name':request.session['uni_name'],'issueList':issueList,'pendingIssues':pendingIssues})
    else:
        return redirect('login')

def student_profile(request):
    if request.method == "POST":
        characters = string.ascii_letters + string.digits
        tkn = ''.join(random.choice(characters) for _ in range(20))
        newToken = PassToken()
        newToken.user_type = request.session['user']
        newToken.username = request.session['username']
        newToken.token = tkn

        try:
            if request.session['username'] == "gueststudent":
                raise Exception("!Modification Of Guest Account Is Not Supported")
            studentDetails = Student.objects.filter(Q(username=request.session['username']))
            studentDetails = studentDetails[0]
            send_mail(
                'NOVA Password Reset Link',
                'Your Requested Link for Password Reset is : '+'https://akmalice.pythonanywhere.com/reset-password/'+tkn,
                'novamarksmanagement@gmail.com',
                [studentDetails.email],
                    fail_silently=False,
                )
            newToken.save()

            return render(request,'dashboard/student-profile.html',{'uni_name':request.session['uni_name'],'studentDetails':studentDetails,'success':'Password Reset Link Sent Successfully'})    
        except Exception as e:
            e = str(e)
            error = "Something Went Wrong"
            if e[0]=='!':
                error = e[1:]
            studentDetails = Student.objects.filter(Q(username=request.session['username']))
            studentDetails = studentDetails[0]
            return render(request,'dashboard/student-profile.html',{'uni_name':request.session['uni_name'],'studentDetails':studentDetails,'error':error})    

    elif request.session.has_key('user') and request.session['user'] == 'student':
        
        studentDetails = Student.objects.filter(Q(username=request.session['username']))
        studentDetails = studentDetails[0]
        
        return render(request,'dashboard/student-profile.html',{'uni_name':request.session['uni_name'],'studentDetails':studentDetails })    
    else :
        return redirect('/login')
