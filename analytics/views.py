from django.shortcuts import render

def admin_analytics(request):
    if request.session.has_key('user') and request.session['user'] == 'admin':
        return render(request,'analytics/admin_analytics.html',{"uni_name" : request.session['uni_name']})
    else :
        return redirect('/login')

def admin_marks(request):
    if request.session.has_key('user') and request.session['user'] == 'admin':
        return render(request,'analytics/admin_marks.html',{"uni_name" : request.session['uni_name']})
    else :
        return redirect('/login')

def faculty_uploadmarks(request):
    if request.session.has_key('user') and request.session['user'] == 'faculty':
        return render(request,'analytics/faculty-uploadmarks.html',{"uni_name" : request.session['uni_name']})
    else :
        return redirect('/login')

def faculty_analytics(request):
    if request.session.has_key('user') and request.session['user'] == 'faculty':
        return render(request,'analytics/faculty-analytics.html',{"uni_name" : request.session['uni_name']})
    else :
        return redirect('/login')