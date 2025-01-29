from django.contrib.auth import authenticate, login
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from . import forms,models
from .models import Teacher,Student,Course
from django.contrib.auth.decorators import login_required
from .forms import TeacherForm
from django.contrib import messages
from django.contrib.auth.models import Group
# Create your views here.
def index(request):
    return render(request,'index.html')
def student_dashboard_view(request):
    return render(request,'stdnt_dashboard.html')

def admin_login(request):
    correct_username = 'group1'
    correct_password = '4321'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == correct_username and password == correct_password:
            return redirect('adminDashboard')
        else:
            return HttpResponse('Invalid credentials, please try again.')
    return render(request, 'admin_login.html')
       


def Teacher_signup_view(request):
    teacherForm=forms.TeacherForm()
    mydict={'teacherForm':teacherForm}
    if request.method=='POST':
        teacherForm=forms.TeacherForm(request.POST,request.FILES)
        if teacherForm.is_valid():
            teacher=teacherForm.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
        return redirect('teacherLogin')
    return render(request,'teach_register.html',context=mydict)

def is_teacher(user):
    return user.group.filter(name='TEACHER').exists()

from django.contrib import messages

from .models import Student
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Teacher  # Import the Teacher model
from django.contrib.auth.hashers import check_password

def teacherLogin(request):
    if request.method == 'POST':
        username = request.POST['teacher_id']
        password = request.POST['password']

        try:
            teacher = Teacher.objects.get(teacher_id=username)
            
            if teacher.password ==password:  # Verify password securely
                request.session['teacher_id'] = teacher.id  # Store teacher ID in session
                return redirect('teacherDashboard')
            else:
                messages.error(request, 'Invalid credentials.')
        except Teacher.DoesNotExist:
            messages.error(request, 'No teacher account found for this ID.')

    return render(request, 'teach_login.html')


@login_required
def teacher_dashboard_view(request):
    return render(request,'teach_dashboard.html')
    



from .forms import StudentForm
def Student_signup_view(request):
    if request.method == 'POST':
        # Create the form instance with POST data and file data (if any)
        studentForm = forms.StudentForm(request.POST, request.FILES)
        
        if studentForm.is_valid():
            studentForm.save()
            return redirect('studentLogin')  # Make sure 'studentlogin' is a valid URL name in your urls.py
        else:
            return render(request, 'stdnt_register.html', {'studentForm': studentForm})

    else:
        studentForm = StudentForm()

    return render(request, 'stdnt_register.html', {'studentForm': studentForm})


def is_student(user):
    return user.group.filter(name='STUDENT').exists()


from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Student  # Import the Student model
from django.contrib.auth.hashers import check_password

def studentLogin(request):
    if request.method == 'POST':
        username = request.POST.get('register_id')
        password = request.POST.get('password')

        try:
            student = Student.objects.get(register_id=username)

            # Directly compare plain-text passwords
            if student.password == password:  
                request.session['register_id'] = student.id  
                return redirect('studentDashboard')
            else:
                messages.error(request, 'Invalid credentials.')
        except Student.DoesNotExist:
            messages.error(request, 'No teacher account found for this ID.')

    return render(request, 'stdnt_login.html')

@login_required
def student_dashboard_view(request):
    return render(request,'stdnt_dashboard.html')

def manage_student_view(request):
    students = models.Student.objects.all()
    return render(request, 'admin_mg_student.html',{'student':students})

def detail_student_view(request):
    students = models.Student.objects.all()
    return render(request, 'teach_st_details.html',{'student':students})

def manage_teacher_view(request):
    teachers = models.Teacher.objects.all()
    return render(request, 'admin_mg_teacher.html',{'teacher':teachers})

def manage_course_view(request):
    courses = models.Course.objects.all()  # Get all courses from the database
    return render(request,'admin_mg_course.html', {'courses': courses})

def afterlogin_view(request):
    if is_teacher(request.user):
        accountapproval=models.Teacher.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('admin-dashboard')
        
    elif is_student(request.user):
        return redirect('student-home')
    else:
        return redirect('teacher-home')

@login_required
def admin_dashboard_view(request):
    return render(request,'admin_dashboard.html')

def teacher_profile_view(request):
    return render(request,'teacher_profile.html')

from django.shortcuts import render
from .models import Student, Attendance

def teacher_attendance_view(request):
    if request.method == 'POST':
        # Get the selected date from the form
        selected_date = request.POST.get('date')
        if not selected_date:
            return render(request, 'teach_st_attendance.html', {'error': 'Date is required'})

        # Loop through students and mark attendance
        students = Student.objects.all()
        for student in students:
            for hour in range(1, 6):  # Loop through hours 1 to 5
                is_present = request.POST.get(f'attendance-{student.register_id}-hour-{hour}') == 'on'
                
                # Ensure that attendance is created or updated for each student, hour, and date
                attendance, created = Attendance.objects.update_or_create(
                    student=student,
                    date=selected_date,
                    hour=hour,
                    defaults={'is_present': is_present},
                )

        # Update full-day attendance count for all students
        for student in students:
            student.update_full_day_attendance()

        # After processing the attendance, pass a success flag and the updated context to the template
        return render(request, 'teach_st_attendance.html', {
            'students': students,
            'hours': range(1, 6),
            'success': True  # Show success message
        })
    
    # For GET requests, render the attendance form
    students = Student.objects.all()
    context = {
        'students': students,
        'hours': range(1, 6),  # Hours 1 to 5
    }
    return render(request, 'teach_st_attendance.html', context)





from django.shortcuts import render, redirect
from .models import Student, Course
from .forms import MarksForm

def teacher_marks_view(request):
    selected_semester = request.GET.get('semester', 'semester-1')  # Default to 'semester-1'

    # Filter students based on the selected semester
    students = Student.objects.all()
    
    # Adjust filtering based on the class field (Class)
    if selected_semester in ['semester-1', 'semester-2']:
        students = students.filter(Class='1st Year')  # First-year students
    elif selected_semester in ['semester-3', 'semester-4']:
        students = students.filter(Class='2nd Year')  # Second-year students
    else:
        students = students.filter(Class='3rd Year')  # Third-year students

    # Fetch all courses from the Course model
    courses = Course.objects.all()

    # Create the form with the semester passed to it
    form = MarksForm(request.POST or None, semester=selected_semester)

    # If the form is valid, save the data
    if request.method == 'POST' and form.is_valid():
        form.save()  # Save the form data as a new Marks record
        return redirect('teachStMarks')  # Redirect after successful save

    return render(request, 'teach_st_marks.html', {
        'form': form,
        'selected_semester': selected_semester,
        'students': students,
        'courses': courses,
    })


def teacher_stats_view(request):
    return render(request,'teach_st_stats.html')

def teacher_details_view(request):
    return render(request,'teach_st_details.html')

def teacher_home_view(request):
    total_first_year = Student.objects.filter (Class="1st Year").count()
    total_second_year = Student.objects.filter(Class="2nd Year").count()
    total_third_year = Student.objects.filter(Class="3rd Year").count()

    # Context to pass to the template
    context = {
        'total_first_year': total_first_year,
        'total_second_year': total_second_year,
        'total_third_year': total_third_year,
    }

    
    return render(request,'teach_home.html',context)
from django.shortcuts import render
from .models import Student, Teacher, Course

from django.db.models import Count

from django.db.models import Count, F

from django.db.models import Count, F
from django.shortcuts import render
from .models import Student, Teacher, Course

from django.db.models import Count, F
from django.shortcuts import render
from .models import Student, Teacher, Course

def admin_home_view(request):
    # Aggregate total counts
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_courses = Course.objects.count()

    # Fetch courses and count the students in each course by matching department and course name
    courses = Course.objects.all()

    course_student_counts = []
    for course in courses:
        # Count students whose department matches the course name
        student_count = Student.objects.filter(department=course.course_name).count()
        course_student_counts.append({
            'course_name': course.course_name,
            'student_count': student_count
        })

    # Prepare data for the donut chart (Student-Teacher Ratio)
    chart_data = {
        'labels': ['Students', 'Teachers'],
        'datasets': [{
            'data': [total_students, total_teachers],
            'backgroundColor': ['#1e90ff', '#ff6347'],
        }]
    }

    # Prepare data for the bar chart (Students per course)
    course_chart_data = {
        'labels': [item['course_name'] for item in course_student_counts],  # Course names
        'datasets': [{
            'label': 'Students in each course',
            'data': [item['student_count'] for item in course_student_counts],
            'backgroundColor': 'rgba(54, 162, 235, 0.5)',
            'borderColor': 'rgba(54, 162, 235, 1)',
            'borderWidth': 1,
        }]
    }

    # Pass the data to the template
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_courses': total_courses,
        'chart_data': chart_data,  # Donut chart data
        'course_chart_data': course_chart_data  # Bar chart data
    }

    return render(request, 'admin_home.html', context)






def admin_mg_teacher_view(request):
    return render(request,'admin_mg_teacher.html')

def admin_mg_student_view(request):
    return render(request,'admin_mg_student.html')

def admin_mg_course_view(request):
    courses = Course.objects.all()  # Get all courses from the database
    return render(request,'admin_mg_course.html', {'courses': courses})

def add_course(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        course_id = request.POST.get('course_id')

        if course_name and course_id:
            # Create a new Course object and save it to the database
            new_course = Course(course_name=course_name, course_id=course_id)
            new_course.save()

            return redirect('adminMgCourse')  # Redirect to the manage courses page
        else:
            return HttpResponse("Error: Course name or ID is missing.")

    return redirect('adminMgCourse') 


def student_profile_view(request):
    return render(request,'stdnt_profile.html')

def student_grades_view(request):
    return render(request,'stdnt_grades.html')

def student_schedule_view(request):
    return render(request,'stdnt_schedule.html')

def student_home_view(request):
    return render(request,'stdnt_home.html')

def student_attendance_view(request):
    return render(request,'stdnt_attendance.html')




from django.shortcuts import render, get_object_or_404, redirect
from .models import Student,Teacher
from django.http import HttpResponse

def edit_student(request, student_id):
    # Get the student by ID
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == "POST":
        # Update the student data from the form
        student.name = request.POST.get('studentName')
        student.Class = request.POST.get('studentClass')
        student.department = request.POST.get('studentDepartment')
        student.register_id = request.POST.get('studentReg')
        student.mobile = request.POST.get('studentMobile')
        student.email = request.POST.get('studentEmail')
        student.parent = request.POST.get('studentParent')
        student.parent_no = request.POST.get('studentParentNo')
        student.password = request.POST.get('studentPassword')
        
        # Save the updated student
        student.save()
        
        return redirect('ManageStudent')  # Redirect back to the student management page
    
    return render(request, 'edit_student.html', {'student': student})



def delete_student(request, student_id):
    # Get the student by ID
    student = get_object_or_404(Student, id=student_id)
    
    # Delete the student
    student.delete()
    
    return redirect('ManageStudent')  # Redirect back to the student management page
 




def edit_teacher(request, teacher_no):
    # Get the student by ID
    teacher = get_object_or_404(Teacher, id=teacher_no)
    
    if request.method == "POST":
        # Update the teacher data from the form
        teacher.name = request.POST.get('teacherName')
        teacher.email = request.POST.get('teacherEmail')
        teacher.teacher_id = request.POST.get('teacherReg')
        teacher.mobile = request.POST.get('teacherMobile')
        teacher.password = request.POST.get('teacherPassword')
        teacher.department = request.POST.get('teacherDepartment')
       
        # Save the updated teacher
        teacher.save()
        
        return redirect('ManageTeacher')  # Redirect back to the teacher management page
    
    return render(request, 'edit_teacher.html', {'teacher': teacher})

def delete_teacher(request, teacher_no):
    # Get the teacher by ID
    teacher = get_object_or_404(Teacher, id=teacher_no)
    
    # Delete the teacher
    teacher.delete()
    
    return redirect('ManageTeacher')  # Redirect back to the teacher management page



def edit_course(request, course_no):
    # Get the course by ID
    course = get_object_or_404(Course, id=course_no)
    
    if request.method == "POST":
        # Update the course data from the form
        course.course_id = request.POST.get('courseId')

        course.course_name = request.POST.get('courseName')
       
        
        # Save the updated coourse
        course.save()
        
        return redirect('ManageCourse')  # Redirect back to the course management page
    
    return render(request, 'edit_course.html', {'course': course})

def delete_course(request, course_no):
    # Get the course by ID
    course = get_object_or_404(Course, id=course_no)
    
    # Delete the course
    course.delete()
    
    return redirect('ManageCourse')  # Redirect back to the course management page
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student

def add_student(request):
    if request.method == "POST":
        name = request.POST.get('name')
        student_class = request.POST.get('Class')
        department = request.POST.get('department')
        register_id = request.POST.get('register_id')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        parent = request.POST.get('parent')
        parent_no = request.POST.get('parent_no')

        # Check if register_id already exists
        if Student.objects.filter(register_id=register_id).exists():
            messages.error(request, "Register ID already exists. Please use a unique ID.")
            return redirect('ManageStudent')

        # Save the student if register_id is unique
        student = Student(
            name=name,
            Class=student_class,
            department=department,
            register_id=register_id,
            mobile=mobile,
            email=email,
            parent=parent,
            parent_no=parent_no,
        )
        student.save()
        messages.success(request, "Student added successfully!")
        return redirect('ManageStudent')

    return render(request, 'admin_mg_student.html')


def add_teacher(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        teacher_id = request.POST.get('teacher_id')
        mobile = request.POST.get('mobile')
        department = request.POST.get('department')
       

        # Check if teacher_id already exists
        if Teacher.objects.filter(teacher_id=teacher_id).exists():
            messages.error(request, "Register ID already exists. Please use a unique ID.")
            return redirect('ManageStudent')

        # Save the student if teacher_id is unique
        teacher = Teacher(
            name=name,
            email=email,
            teacher_id=teacher_id,
            mobile=mobile,
            department=department,
           
        )
        teacher.save()
        messages.success(request, "Teacher added successfully!")
        return redirect('ManageTeacher')

    return render(request, 'admin_mg_teacher.html')

from django.shortcuts import redirect
from django.contrib.auth import logout

def logout_view(request):
    logout(request)  # Logs the user out
    return redirect('index')  # Redirect to home page after logout

