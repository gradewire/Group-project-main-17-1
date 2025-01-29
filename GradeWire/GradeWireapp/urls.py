from django.urls import path
from  . import views
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('', views.index,name='index'),
    path('logout/', views.logout_view, name='logout'),  # Logout URL

    path('teacherlogin/', views.teacherLogin,name='teacherLogin'),
    path('tregister/', views.Teacher_signup_view,name='teacherRegister'),
    path('sregister/', views.Student_signup_view,name='studentRegister'),

    path('studentlogin/', views.studentLogin, name='studentLogin'),
    path('student-dashboard/', views.student_dashboard_view,name='studentDashboard'),
    path('teacher-dashboard/', views.teacher_dashboard_view,name='teacherDashboard'),
    path('adminlogin/', views.admin_login,name='adminlogin'),
    path('admin-dashboard/', views.admin_dashboard_view,name='adminDashboard'),
    path('teacher-profile/', views.teacher_profile_view,name='teacherProfile'),
    path('teacher-attendance/', views.teacher_attendance_view,name='teachStAttendance'),
    path('teacher-marks/', views.teacher_marks_view,name='teachStMarks'),
    path('teacher-stats/', views.teacher_stats_view,name='teachStStats'),
    path('teacher-details/', views.teacher_details_view,name='teachStDetails'),
    path('teacher-home/', views.teacher_home_view,name='teachHome'),
    path('admin-home/', views.admin_home_view,name='adminHome'),
    path('admin-student/', views.admin_mg_student_view,name='adminMgStudent'),
    path('admin-teacher/', views.admin_mg_teacher_view,name='adminMgTeacher'),
    path('admin-course/', views.admin_mg_course_view,name='adminMgCourse'),
    path('student-profile/', views.student_profile_view,name='studentProfile'),
    path('student-attendance/', views.student_attendance_view,name='studentAttendance'),
    path('student-grades/', views.student_grades_view,name='studentGrades'),
    path('student-home/', views.student_home_view,name='studentHome'),
    path('manage-student/', views.manage_student_view,name='ManageStudent'),
    path('manage-teacher/', views.manage_teacher_view,name='ManageTeacher'),
    path('manage-course/', views.manage_course_view,name='ManageCourse'),

    path('student-details/', views.detail_student_view,name='StudentDetail'),
    path('edit-student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('edit-teacher/<int:teacher_no>/', views.edit_teacher, name='edit_teacher'),
    path('delete-teacher/<int:teacher_no>/', views.delete_teacher, name='delete_teacher'),
    path('add-course/', views.add_course, name='add_course'),
    path('delete-course/<int:course_no>/', views.delete_course, name='delete_course'),

    path('edit-course/<int:course_no>/', views.edit_course, name='edit_course'),
    path('add-student/', views.add_student, name='add_student'),
    path('add-teacher/', views.add_teacher, name='add_teacher'),

]
