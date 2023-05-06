"""mmsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from home import views as homeviews
from dashboard import views as dashboardviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homeviews.home,name="home-page"),
    path('login',homeviews.login,name="login"),
    path('signup',homeviews.signup,name="signup"),
    path('dashboard',dashboardviews.dashboard,name="dash"),
    path('logout',dashboardviews.logout,name="logout"),
    path('faculty',dashboardviews.admin_faculty,name="faculty"),
    path('faculty/<slug:id>',dashboardviews.admin_faculty_details,name="faculty-details"),
    path('faculty/<slug:id>/delete/<slug:section>',dashboardviews.admin_faculty_details_delete,name="delete-section"),
    path('students',dashboardviews.admin_students,name="students"),
    path('students/<int:id>',dashboardviews.admin_student_details,name="student-details"),
    path('forgotpassword',homeviews.forgotpassword,name="forgotpassword"),
    path('students/<slug:id>',dashboardviews.admin_student_details,name="student-details"),
    path('issues',dashboardviews.admin_issues,name="issues"),
    path('issues/<slug:student_id>/<int:issue_id>',dashboardviews.admin_issue_details,name="issue-details"),
    path('issues/<slug:student_id>/<int:issue_id>/resolved',dashboardviews.admin_issue_resolved,name="issue-resolved"),
    path('issues/<slug:student_id>/<int:issue_id>/dismissed',dashboardviews.admin_issue_dismissed,name="issue-dismissed"),
]   
