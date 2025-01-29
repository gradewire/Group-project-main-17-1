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
        fields = '__all__'  


from .models import Marks, Student, Course

class MarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = ['student', 'semester', 'exam_name', 'subject', 'internal_marks', 'external_marks']

    # Semester and Exam Name options
    semester = forms.ChoiceField(choices=[('semester-1', 'Semester 1'),
                                          ('semester-2', 'Semester 2'),
                                          ('semester-3', 'Semester 3'),
                                          ('semester-4', 'Semester 4'),
                                          ('semester-5', 'Semester 5'),
                                          ('semester-6', 'Semester 6')], required=True)

    exam_name = forms.ChoiceField(choices=[('internal-1', 'Internal Exam 1'),
                                           ('internal-2', 'Internal Exam 2'),
                                           ('model', 'Model Exam'),
                                           ('sem-exam', 'Semester Exam')], required=True)

    # Dynamically populate the student field based on selected semester
    student = forms.ModelChoiceField(queryset=Student.objects.none(), required=True)

    # Subject (Course) field with all courses available
    subject = forms.ModelChoiceField(queryset=Course.objects.all(), required=True)

    internal_marks = forms.IntegerField(min_value=0, max_value=20, required=True)
    external_marks = forms.IntegerField(min_value=0, max_value=40, required=True)

    def __init__(self, *args, **kwargs):
        semester = kwargs.pop('semester', None)
        super().__init__(*args, **kwargs)

        # Dynamically update the student queryset based on selected semester
        if semester:
            if semester in ['semester-1', 'semester-2']:
                self.fields['student'].queryset = Student.objects.filter(Class='1st Year')
            elif semester in ['semester-3', 'semester-4']:
                self.fields['student'].queryset = Student.objects.filter(Class='2nd Year')
            else:
                self.fields['student'].queryset = Student.objects.filter(Class='3rd Year')