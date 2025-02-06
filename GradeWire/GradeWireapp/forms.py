from django import forms
from django.contrib.auth.models import User
from . import models


class TeacherForm(forms.ModelForm):
    class Meta:
        model=models.Teacher
        fields='__all__'


from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'Class', 'department', 'register_id', 'mobile', 'email', 'parent', 'parent_no', 'password']  




from django import forms
from .models import Marks, Student, Course

from django import forms
from .models import Marks, Student, Course,Subject

class MarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = ['semester', 'registerId', 'exam_name', 'subject', 'internalMarks', 'externalMarks']

    SEMESTER_CHOICES = [
        ('semester-1', 'Semester 1'),
        ('semester-2', 'Semester 2'),
        ('semester-3', 'Semester 3'),
        ('semester-4', 'Semester 4'),
        ('semester-5', 'Semester 5'),
        ('semester-6', 'Semester 6'),
    ]
    EXAM_CHOICES = [
        ('internal-1', 'Internal Exam 1'),
        ('internal-2', 'Internal Exam 2'),
        ('model', 'Model Exam'),
        ('sem-exam', 'Semester Exam'),
    ]

    semester = forms.ChoiceField(choices=SEMESTER_CHOICES)
    exam_name = forms.ChoiceField(choices=EXAM_CHOICES)
    registerId = forms.ModelChoiceField(queryset=Student.objects.all(), required=True)
    course = forms.ModelChoiceField(queryset=Course.objects.all(), required=True)
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), required=True)
    internalMarks = forms.IntegerField(min_value=0, max_value=100, required=True)
    externalMarks = forms.IntegerField(min_value=0, max_value=100, required=True)

    def __init__(self, *args, **kwargs):
        semester = kwargs.pop('semester', None)  # Get semester if passed
        course_id = kwargs.get('data', {}).get('course')  # Get course ID from form data

        super(MarksForm, self).__init__(*args, **kwargs)

        # Set initial value for semester
        if semester:
            self.fields['semester'].initial = semester

        # Filter the registerId (students) based on the semester
        if semester:
            if semester in ['semester-1', 'semester-2']:
                self.fields['registerId'].queryset = Student.objects.filter(Class='1st Year')
            elif semester in ['semester-3', 'semester-4']:
                self.fields['registerId'].queryset = Student.objects.filter(Class='2nd Year')
            else:
                self.fields['registerId'].queryset = Student.objects.filter(Class='3rd Year')

            # Optionally filter courses based on semester (if needed)
            self.fields['course'].queryset = Course.objects.all()  # Adjust if necessary
              # **Filter subjects based on selected course**
        if course_id:
            self.fields['subject'].queryset = Subject.objects.filter(course_id=course_id)
        else:
            self.fields['subject'].queryset = Subject.objects.none()  # Default to empty queryset

