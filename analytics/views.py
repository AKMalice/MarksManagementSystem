from django.shortcuts import render
from analytics.models import *
from dashboard.models import *
from django.db.models import Q
from datetime import datetime
import csv
from django.core.files.storage import FileSystemStorage
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plot
import matplotlib.ticker as mtick
from io import BytesIO
import base64

def generate_student_analytics(adminUsername,studentId,year):
    
                sectionIdList = Classe.objects.filter(Q(admin_username=adminUsername) & Q(student_id=studentId) & Q(year=year) ).values_list('section_id',flat=True)

                courseIdList = Section.objects.filter(Q(admin_username=adminUsername) & Q(section_id__in=sectionIdList) ).values_list('course_id',flat=True)

                examList = Exam.objects.filter(Q(admin_username=adminUsername) & Q(course_id__in=courseIdList) )
                
                examIdToCourse = {}
                for exam in examList:
                    examIdToCourse[exam.id] = [exam.course_id,exam.pass_marks,exam.max_marks]
                
                examList = examList.values_list('id',flat=True)

                results = {}

                resultList = Result.objects.filter(Q(admin_username=adminUsername) & Q(exam_id__in=examList) & Q(student_id=studentId) )

                for result in resultList:
                    if results.get(examIdToCourse[result.exam_id][0]) is None:
                        results[examIdToCourse[result.exam_id][0]] = []
                    results[examIdToCourse[result.exam_id][0]].append(result.marks/examIdToCourse[result.exam_id][2]*100)
                    # print(results[examIdToCourse[result.exam_id][0]])
                    
                for course in results.keys():
                    results[course] = sum(results[course])/len(results[course])

                plot.ylim(0,100)
                plot.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100))
                plot.bar(results.keys(),results.values())
                plot.title(studentId+"\n"+year)
                plot.xlabel("Course")
                plot.ylabel("Percentage")

                buffer = BytesIO()
                plot.savefig(buffer, format='png')
                buffer.seek(0)
                image_png = buffer.getvalue()
                buffer.close()
                graphic = base64.b64encode(image_png)
                graphic = graphic.decode('utf-8')
                plot.close()

                return graphic

def admin_analytics(request):
    if request.method == "POST":
        if "exam" in request.POST:
            examDetails = request.POST['exam'].split("|")

            resultList = Result.objects.filter(Q(admin_username=request.session['username']) & Q(exam_id=examDetails[0])).values_list('marks',flat=True)
            max_marks = Exam.objects.filter(Q(admin_username=request.session['username']) & Q(id=examDetails[0])).values_list('max_marks',flat=True)[0]

            plot.hist(list(resultList),bins=max_marks//10)
            plot.title(examDetails[1]+" Histogram")
            plot.xlabel("Marks")
            plot.ylabel("Count")
            buffer = BytesIO()
            plot.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            graphic = base64.b64encode(image_png)
            graphic = graphic.decode('utf-8')
            plot.close()

            examList = Exam.objects.filter(admin_username=request.session['username'])
            return render(request,'analytics/admin_analytics.html',{"uni_name" : request.session['uni_name'],"examList":examList,"graphic":graphic})

        else:
            try:
                graphic = generate_student_analytics(request.session['username'],request.POST['student_id'],request.POST['year'])

                examList = Exam.objects.filter(admin_username=request.session['username'])
                return render(request,'analytics/admin_analytics.html',{"uni_name" : request.session['uni_name'],"graphic":graphic,"examList":examList})
            except Exception as e:
                print(str(e))
                examList = Exam.objects.filter(admin_username=request.session['username'])
                return render(request,'analytics/admin_analytics.html',{"uni_name" : request.session['uni_name'],"examList":examList,"error":"Something Went Wrong"})

    elif request.session.has_key('user') and request.session['user'] == 'admin':
        examList = Exam.objects.filter(admin_username=request.session['username'])
        return render(request,'analytics/admin_analytics.html',{"uni_name" : request.session['uni_name'],"examList":examList})
    else :
        return redirect('/login')

def admin_exams(request):
    if request.method=='POST':
        data = request.POST
        newExam = Exam()
        newExam.admin_username = request.session['username']
        newExam.name = data['name']
        newExam.course_id = data['course_id']
        newExam.max_marks = data['max_marks']
        newExam.pass_marks = data['pass_marks']
        newExam.date = data['date']

        try:
            if str(newExam.date) < str(datetime.today())[:10]:
                raise Exception("Invalid Deadline")
            if request.session['username'] == "guestadmin":
                raise Exception("!Modification Of Guest Account Is Not Supported")
            newExam.save()
            examList = Exam.objects.filter(admin_username=request.session['username'])
            upcomingExamCount=0

            for exam in examList:
                if str(exam.date) < str(datetime.today())[:10]:
                    exam.status = "Completed"
                else:
                    exam.status = "Upcoming"
                    upcomingExamCount+=1

            examList = sorted(examList,key = lambda exam: exam.date,reverse=True)

            return render(request,'analytics/admin_exams.html',{"uni_name" : request.session['uni_name'],'examList' : examList,'upcomingExamCount':upcomingExamCount,'success':"Exam Added Successfully"})
        except Exception as e:
            e = str(e)
            error = "Something Went Wrong"
            if "Invalid Deadline" in e:
                error = "Invalid Deadline"
            if e[0] == '!':
                error = e[1:]
            examList = Exam.objects.filter(admin_username=request.session['username'])
            upcomingExamCount = 0

            for exam in examList:
                if str(exam.date) < str(datetime.today())[:10]:
                    exam.status = "Completed"
                else:
                    exam.status = "Upcoming"
                    upcomingExamCount+=1

            examList = sorted(examList,key = lambda exam: exam.date,reverse=True)

            return render(request,'analytics/admin_exams.html',{"uni_name" : request.session['uni_name'],'examList' : examList,'error':error,'upcomingExamCount':upcomingExamCount})

    elif request.session.has_key('user') and request.session['user'] == 'admin':
        examList = Exam.objects.filter(admin_username=request.session['username'])
        upcomingExamCount = 0

        for exam in examList:
            if str(exam.date) < str(datetime.today())[:10]:
                exam.status = "Completed"
            else:
                exam.status = "Upcoming"
                upcomingExamCount+=1

        examList = sorted(examList,key = lambda exam: exam.date,reverse=True)

        return render(request,'analytics/admin_exams.html',{"uni_name" : request.session['uni_name'],'examList' : examList,'upcomingExamCount':upcomingExamCount})
    else :
        return redirect('/login')

def faculty_uploadmarks(request):
    if request.method == 'POST':

        try:
            data = request.POST

            facultyDetails = Faculty.objects.filter(Q(username=request.session['username']))
            facultyDetails = facultyDetails[0]

            if request.session['username'] == "guestfaculty":
                raise Exception("!Modification Of Guest Account Is Not Supported")

            check_section = Section.objects.filter(Q(admin_username=facultyDetails.admin_username) & Q(teacher_id=facultyDetails.teacher_id) & Q(section_name=data['section']) & Q(course_id=data['course_id']) & Q(course_name=data['course_name']))
            if len(check_section) != 1:
                raise Exception("!Section Does Not Exist")

            check_exam = Exam.objects.filter(Q(admin_username=facultyDetails.admin_username) & Q(course_id=data['course_id']) & Q(name=data['exam_name']))
            if len(check_exam) != 1:
                raise Exception("!Exam Schedule Does Not Exist")

            if not request.FILES['file'].name.endswith('.csv'):
                raise Exception("!Invalid File Format")

            if request.FILES['file'].size > 10485760: #10 MB
                raise Exception("!File Size Limit Exceeded")
            
            file_data = request.FILES['file'].read().decode('utf-8').split('\n')

            newUpload = Upload()
            newUpload.admin_username = facultyDetails.admin_username
            newUpload.teacher_id = facultyDetails.teacher_id
            newUpload.exam_id = check_exam[0].id
            newUpload.course_name = data['course_name']
            newUpload.exam_name = data['exam_name']
            newUpload.course_id = data['course_id']
            newUpload.section_name = data['section']
            newUpload.file_name = request.FILES['file'].name
            newUpload.date = datetime.today()

            newUpload.save()

            saved_data = []

            for line in file_data:
                line = line.split(',')
                if len(line)==2:
                    if line[1].lower() != "marks\r":
                        newResult = Result()
                        newResult.admin_username = facultyDetails.admin_username
                        newResult.exam_id = check_exam[0].id
                        newResult.student_id = line[0]
                        newResult.marks = int(line[1])
                        saved_data.append(line[0])
                        newResult.save()


            classList = Section.objects.filter(Q(admin_username=facultyDetails.admin_username) & Q(teacher_id=facultyDetails.teacher_id) &Q(active=True))

            examList = Exam.objects.filter(Q(admin_username=facultyDetails.admin_username) & Q(course_id__in = classList.values_list('course_id',flat=True)))

            uploadList = Upload.objects.filter(Q(admin_username=facultyDetails.admin_username) & Q(teacher_id=facultyDetails.teacher_id)).order_by('-date')

            sectionList = list(dict.fromkeys(classList.values_list('section_name',flat=True)))
            courseIdList = list(dict.fromkeys(classList.values_list('course_id',flat=True)))
            courseNameList = list(dict.fromkeys(classList.values_list('course_name',flat=True)))
            examNameList = list(dict.fromkeys(examList.values_list('name',flat=True)))

            return render(request,'analytics/faculty-uploadmarks.html',{"uni_name" : request.session['uni_name'],"examNameList" : examNameList,'sectionList' : sectionList,'courseIdList' : courseIdList,'courseNameList' : courseNameList,"uploadList":uploadList,"uploadCount":len(uploadList),"success" : "Marks Uploaded Successfully"})
        
        except Exception as e:
            e = str(e)
            error = "Something Went Wrong"
            if e[0] == '!':
                error = e[1:]

            facultyDetails = Faculty.objects.filter(Q(username=request.session['username']))
            facultyDetails = facultyDetails[0]
            check_exam = Exam.objects.filter(Q(admin_username=facultyDetails.admin_username) & Q(course_id=data['course_id']) & Q(name=data['exam_name']))

            Upload.objects.filter(Q(admin_username=facultyDetails.admin_username) & Q(teacher_id=facultyDetails.teacher_id) & Q(exam_id=check_exam[0].id) & Q(course_name=data['course_name']) & Q(section_name=data['section']) & Q(file_name=request.FILES['file'].name)).delete()
            for student in saved_data:
                Result.objects.filter(Q(admin_username=facultyDetails.admin_username) & Q(exam_id=check_exam[0].id) & Q(student_id=student)).delete()

            classList = Section.objects.filter(Q(admin_username=facultyDetails.admin_username) & Q(teacher_id=facultyDetails.teacher_id) &Q(active=True))

            examList = Exam.objects.filter(Q(admin_username=facultyDetails.admin_username) & Q(course_id__in = classList.values_list('course_id',flat=True)))

            uploadList = Upload.objects.filter(Q(admin_username=facultyDetails.admin_username) & Q(teacher_id=facultyDetails.teacher_id)).order_by('-date')

            sectionList = list(dict.fromkeys(classList.values_list('section_name',flat=True)))
            courseIdList = list(dict.fromkeys(classList.values_list('course_id',flat=True)))
            courseNameList = list(dict.fromkeys(classList.values_list('course_name',flat=True)))
            examNameList = list(dict.fromkeys(examList.values_list('name',flat=True)))

            return render(request,'analytics/faculty-uploadmarks.html',{"uni_name" : request.session['uni_name'],"examNameList" : examNameList,'sectionList' : sectionList,'courseIdList' : courseIdList,'courseNameList' : courseNameList,"uploadList":uploadList,"uploadCount":len(uploadList),"error" : error})

    elif request.session.has_key('user') and request.session['user'] == 'faculty':

        facultyDetails = Faculty.objects.filter(Q(username=request.session['username']))
        facultyDetails = facultyDetails[0]

        classList = Section.objects.filter(Q(admin_username=facultyDetails.admin_username) & Q(teacher_id=facultyDetails.teacher_id) &Q(active=True))

        examList = Exam.objects.filter(Q(admin_username=facultyDetails.admin_username) & Q(course_id__in = classList.values_list('course_id',flat=True)))

        uploadList = Upload.objects.filter(Q(admin_username=facultyDetails.admin_username) & Q(teacher_id=facultyDetails.teacher_id)).order_by('-date')

        sectionList = list(dict.fromkeys(classList.values_list('section_name',flat=True)))
        courseIdList = list(dict.fromkeys(classList.values_list('course_id',flat=True)))
        courseNameList = list(dict.fromkeys(classList.values_list('course_name',flat=True)))
        examNameList = list(dict.fromkeys(examList.values_list('name',flat=True)))

        return render(request,'analytics/faculty-uploadmarks.html',{"uni_name" : request.session['uni_name'],"examNameList" : examNameList,'sectionList' : sectionList,'courseIdList' : courseIdList,'courseNameList' : courseNameList,"uploadList":uploadList,"uploadCount":len(uploadList)})
    else :
        return redirect('/login')

def faculty_analytics(request):
    if request.method == "POST":
        data = request.POST
        try:
            examData=data['exam'].split("|")

            facultyDetails = Faculty.objects.filter(Q(username=request.session['username']))
            facultyDetails = facultyDetails[0]

            sectionIdList = Section.objects.filter(Q(admin_username=facultyDetails.admin_username) & Q(teacher_id=facultyDetails.teacher_id) & Q(course_id=examData[1]) &Q(section_name=examData[2])).values_list('section_id',flat=True)
            
            studentList = Classe.objects.filter(Q(admin_username=facultyDetails.admin_username) & Q(section_id__in=sectionIdList)).values_list('student_id',flat=True)
            
            resultList = Result.objects.filter(Q(student_id__in=studentList) & Q(exam_id=examData[0])).values_list('marks',flat=True)
            resultList = list(resultList)

            examDetails = Exam.objects.filter(Q(admin_username=facultyDetails.admin_username) & Q(id=examData[0]))
            examDetails = examDetails[0]

            
            plot.hist(resultList,bins=examDetails.max_marks//10)
            plot.title("Histogram\n"+examData[1]+" "+examData[2])
            plot.xlabel("Marks")
            plot.ylabel("Count")
            # plot.show()

            buffer = BytesIO()
            plot.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            graphic = base64.b64encode(image_png)
            graphic = graphic.decode('utf-8')
            plot.close()

            examList = Upload.objects.filter(Q(admin_username=facultyDetails.admin_username) & Q(teacher_id=facultyDetails.teacher_id))

            return render(request,'analytics/faculty-analytics.html',{"uni_name" : request.session['uni_name'],"examList":examList,'graphic':graphic})

        except Exception as e:
            print(str(e))
            facultyDetails = Faculty.objects.filter(Q(username=request.session['username']))
            facultyDetails = facultyDetails[0]

            examList = Upload.objects.filter(Q(admin_username=facultyDetails.admin_username) & Q(teacher_id=facultyDetails.teacher_id))

            return render(request,'analytics/faculty-analytics.html',{"uni_name" : request.session['uni_name'],"examList":examList,'error':'Something Went Wrong'})


    elif request.session.has_key('user') and request.session['user'] == 'faculty':

        facultyDetails = Faculty.objects.filter(Q(username=request.session['username']))
        facultyDetails = facultyDetails[0]

        examList = Upload.objects.filter(Q(admin_username=facultyDetails.admin_username) & Q(teacher_id=facultyDetails.teacher_id))

        return render(request,'analytics/faculty-analytics.html',{"uni_name" : request.session['uni_name'],"examList":examList})
    else :
        return redirect('/login')

def student_analytics(request):
    if request.session.has_key('user') and request.session['user'] == 'student':
        if request.method == 'POST':
            data = request.POST
            try:
                studentDetails = Student.objects.filter(Q(username=request.session['username']))
                studentDetails = studentDetails[0]

                graphic = generate_student_analytics(studentDetails.admin_username,studentDetails.student_id,data['year'])

                yearList = Classe.objects.filter(Q(admin_username=studentDetails.admin_username) & Q(student_id=studentDetails.student_id) ).values_list('year',flat=True).distinct()

                return render(request,'analytics/student-analytics.html',{'uni_name':request.session['uni_name'],'yearList':yearList,'graphic':graphic})
                
            except Exception as e:
                print(str(e))
                studentDetails = Student.objects.filter(Q(username=request.session['username']))
                studentDetails = studentDetails[0]
                yearList = Classe.objects.filter(Q(admin_username=studentDetails.admin_username) & Q(student_id=studentDetails.student_id) ).values_list('year',flat=True).distinct()
                return render(request,'analytics/student-analytics.html',{'uni_name':request.session['uni_name'],'yearList':yearList,'error':'Something Went Wrong'})

        else:
            studentDetails = Student.objects.filter(Q(username=request.session['username']))
            studentDetails = studentDetails[0]
            yearList = Classe.objects.filter(Q(admin_username=studentDetails.admin_username) & Q(student_id=studentDetails.student_id) ).values_list('year',flat=True).distinct()
            return render(request,'analytics/student-analytics.html',{'uni_name':request.session['uni_name'],'yearList':yearList})
    else :
        return redirect('/login')
    
def student_viewmarks(request):
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

        return render(request,'analytics/student-viewmarks.html',{'uni_name':request.session['uni_name'],'sectionList':sectionList,'sectionCount':len(sectionList)})
    else :
        return redirect('/login')

def student_viewmarks_course(request,course_id):
    if request.session.has_key('user') and request.session['user'] == 'student':

        studentDetails = Student.objects.filter(Q(username=request.session['username']))
        studentDetails = studentDetails[0]

        course_name = Section.objects.filter(Q(admin_username=studentDetails.admin_username) & Q(course_id=course_id))[0].course_name
        examIdList = Exam.objects.filter(Q(admin_username=studentDetails.admin_username) & Q(course_id=course_id)).values_list('id',flat=True)
        resultList = Result.objects.filter(Q(admin_username=studentDetails.admin_username) & Q(student_id=studentDetails.student_id) & Q(exam_id__in=examIdList))

        for result in resultList:
            examData = Exam.objects.filter(Q(admin_username=studentDetails.admin_username) & Q(id=result.exam_id))[0]
            result.exam_name = examData.name
            result.pass_marks = examData.pass_marks
            result.max_marks = examData.max_marks
            result.date = examData.date
            if result.marks>result.pass_marks:
                result.passed = True

        return render(request,'analytics/student-viewmarks-course.html',{'uni_name':request.session['uni_name'],'course_name': course_name,'resultList': resultList,'resultCount':len(resultList)})
    else:
        return redirect('/login')
