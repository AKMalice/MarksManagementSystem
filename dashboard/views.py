from django.shortcuts import render
from django.shortcuts import redirect

def admin_dashboard(request):
    if request.session.has_key('username'):
        del request.session['username']
        return render(request,'dashboard/admin_dash.html',{"uni_name" : request.session['uni_name']})
    else:
        return redirect('/login')
