from django.shortcuts import render
from django.shortcuts import redirect
from dashboard.models import *
from home.models import *
from django.core.mail import send_mail
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
            issueList = Issue.objects.filter(Q(admin_username=request.session['username']) & Q(status="pending"))
            return render(request,'dashboard/admin_dash.html',{"uni_name" : request.session['uni_name'], "success" : "Announcement Sent Sucessfully", "announcementList":reversed(announcementList) if len(announcementList)>0 else None,"issueCount":len(issueList)})
        except:
            announcementList = Announcement.objects.filter(Q(admin_username=request.session['username']))
            issueList = Issue.objects.filter(Q(admin_username=request.session['username']) & Q(status="pending"))
            return render(request,'dashboard/admin_dash.html',{"uni_name" : request.session['uni_name'],"error" : "Failed To Send Announcement", "announcementList":reversed(announcementList) if len(announcementList)>0 else None,"issueCount":len(issueList)})

    elif request.session.has_key('user') and request.session['user'] == 'admin':
        announcementList = Announcement.objects.filter(Q(admin_username=request.session['username']))
        issueList = Issue.objects.filter(Q(admin_username=request.session['username']) & Q(status="pending"))
        return render(request,'dashboard/admin_dash.html',{"uni_name" : request.session['uni_name'], "announcementList":reversed(announcementList) if len(announcementList)>0 else None,"issueCount":len(issueList)})
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
            newFaculty.save()
            send_mail(
                'NOVA Invitation',
                'You Have Been Invited To Join NOVA You Can Login Using the Following Credentials :\n '+'Username : '+newFaculty.username+'\n'+'Password : '+newFaculty.password+'\nLogin Here : https://akmalice.pythonanywhere.com/login',
                'novamarks123@gmail.com',
                [newFaculty.email],
                 fail_silently=False,
            )
            newUser.save()

            facultyList = Faculty.objects.filter(Q(admin_username=request.session['username']))
            return render(request,'dashboard/admin_faculty.html',{"uni_name" : request.session['uni_name'] , "success" : "Faculty Added Successfully","facultyList" : facultyList,"facultyListLength" : len(facultyList),"courseCount" : courseCount})

        except Exception as e:
            Faculty.objects.filter(Q(admin_username=request.session['username']) & Q(teacher_id=newFaculty.teacher_id)).delete()
            e = str(e)
            if "email" in e:
                facultyList = Faculty.objects.filter(Q(admin_username=request.session['username']))
                return render(request,'dashboard/admin_faculty.html',{"uni_name" : request.session['uni_name'] , "error" : "Email Must Be Unique" ,"facultyList" : facultyList,"facultyListLength" : len(facultyList),"courseCount" : courseCount})
            elif "username" in e:
                facultyList = Faculty.objects.filter(Q(admin_username=request.session['username']))
                return render(request,'dashboard/admin_faculty.html',{"uni_name" : request.session['uni_name'] , "error" : "Username Must Be Unique" ,"facultyList" : facultyList,"facultyListLength" : len(facultyList),"courseCount" : courseCount})
            else:
                facultyList = Faculty.objects.filter(Q(admin_username=request.session['username']))
                print(e)
                return render(request,'dashboard/admin_faculty.html',{"uni_name" : request.session['uni_name'] , "error" : "Something Went Wrong" ,"facultyList" : facultyList,"facultyListLength" : len(facultyList),"courseCount" : courseCount})

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
        newSection.course_id = data.get('course_id')
        newSection.course_name = data.get('course_name')
        newSection.section_name = data.get('section_name')
        newSection.year = data.get('year')
        newSection.section_id =  (newSection.year + newSection.course_id + newSection.section_name).replace(" ","")

        try:
            newSection.save()
            sectionList = Section.objects.filter(Q(admin_username=request.session['username']) & Q(teacher_id=id) & Q(active=True))
            courseCount = sectionList.values('course_id').distinct().count()
            return render(request,'dashboard/admin_faculty_details.html',{"uni_name" : request.session['uni_name'] ,"faculty" : faculty,"success" : "Section Added Successfully", "sectionList" : sectionList, "sectionCount" : len(sectionList), "courseCount" : courseCount})
        except:
            sectionList = Section.objects.filter(Q(admin_username=request.session['username']) & Q(teacher_id=id) & Q(active=True))
            courseCount = sectionList.values('course_id').distinct().count()
            return render(request,'dashboard/admin_faculty_details.html',{"uni_name" : request.session['uni_name'] ,"faculty" : faculty,"error":"Something Went Wrong", "sectionList" : sectionList, "sectionCount" : len(sectionList), "courseCount" : courseCount})

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
            newStudent.save()
            send_mail(
                'NOVA Invitation',
                'You Have Been Invited To Join NOVA You Can Login Using the Following Credentials :\n '+'Username : '+newStudent.username+'\n'+'Password : '+newStudent.password+'\nLogin Here : https://akmalice.pythonanywhere.com/login',
                'novamarks123@gmail.com',
                [newStudent.email],
                 fail_silently=False,
            )
            newUser.save()

            studentList = Student.objects.filter(Q(admin_username=request.session['username']))
            return render(request,'dashboard/admin_students.html',{"uni_name" : request.session['uni_name'] , "success" : "Student Added Successfully","studentList" : studentList,"studentListLength" : len(studentList),"courseCount" : courseCount})
            
        except Exception as e:
            Student.objects.filter(Q(admin_username=request.session['username']) & Q(student_id=newStudent.student_id)).delete()
            e = str(e)
            if "email" in e:
                studentList = Student.objects.filter(Q(admin_username=request.session['username']))
                return render(request,'dashboard/admin_students.html',{"uni_name" : request.session['uni_name'] , "error" : "Email Must Be Unique" ,"studentList" : studentList,"studentListLength" : len(studentList),"courseCount" : courseCount})
            elif "username" in e:
                studentList = Student.objects.filter(Q(admin_username=request.session['username']))
                return render(request,'dashboard/admin_students.html',{"uni_name" : request.session['uni_name'] , "error" : "Username Must Be Unique" ,"studentList" : studentList,"studentListLength" : len(studentList),"courseCount" : courseCount})
            else:
                print(e)
                studentList = Student.objects.filter(Q(admin_username=request.session['username']))
                return render(request,'dashboard/admin_students.html',{"uni_name" : request.session['uni_name'] , "error" : "Something Went Wrong" ,"studentList" : studentList,"studentListLength" : len(studentList),"courseCount" : courseCount})

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
        except:
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
            return render(request,'dashboard/admin_student_details.html',{"uni_name" : request.session['uni_name'] ,"student" : student,"classList" : classList, "courseCount" : len(classList),"sectionList" : sectionListComp,"error":"Oops! Something Went Wrong"})

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
        issueList = Issue.objects.filter(Q(admin_username=request.session['username']) & Q(status="pending"))
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
            Issue.objects.filter(Q(admin_username=request.session['username']) & Q(pk=issue_id)).update(status="resolved")
            return redirect('issues')
        except:
            return redirect('issues')
    else:
        return redirect('/login')

def admin_issue_dismissed(request,student_id,issue_id):
    if request.session.has_key('user') and request.session['user'] == 'admin':
        try:
            Issue.objects.filter(Q(admin_username=request.session['username']) & Q(pk=issue_id)).update(status="dismissed")
            return redirect('issues')
        except:
            return redirect('issues')
    else:
        return redirect('/login')

def student_dashboard(request):
    pass

def faculty_dashboard(request):
    pass
