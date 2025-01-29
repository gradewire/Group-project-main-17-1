from django.db import models

# Create your models here.

class Teacher(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField(unique=True)
    teacher_id=models.CharField(max_length=20,unique=True)
    mobile = models.CharField(max_length=10,default='mobile')  # Changed from IntegerField to CharField
    password=models.CharField(max_length=15)
    department=models.CharField(max_length=30)

from django.db import models
from django.db.models import Count, Q


class Student(models.Model):
    name = models.CharField(max_length=30)
    Class = models.CharField(max_length=20)
    department = models.CharField(max_length=30)
    register_id = models.CharField(max_length=30,unique=True)
    mobile = models.CharField(max_length=10)  # Changed from IntegerField to CharField
    email = models.EmailField(unique=True)
    parent = models.CharField(max_length=30)
    parent_no = models.CharField(max_length=10)  # Changed from IntegerField to CharField
    password = models.CharField(max_length=15)
    full_day_attendance = models.PositiveIntegerField(default=0)  # To store full-day attendance count

    def __str__(self):
        return self.name
    
    def update_full_day_attendance(self):
        """Updates the full-day attendance count for the student."""
        full_day_count = (
            Attendance.objects.filter(student=self, is_present=True)
            .values('date')  # Group by date
            .annotate(hours_present=Count('hour', filter=Q(is_present=True)))  # Count the hours present per day
            .filter(hours_present=5)  # Only include days where 5 hours are present
            .count()
        )
        self.full_day_attendance = full_day_count
        self.save()

class Attendance(models.Model):
    """Represents attendance for a specific student, date, and hour."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    hour = models.PositiveSmallIntegerField(choices=[(i, f"Hour {i}") for i in range(1, 6)])  # Choices for hours 1 to 5
    is_present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'date', 'hour')  # Ensures no duplicate attendance for the same date and hour

    def __str__(self):
        return f"Attendance: {self.student} on {self.date} - Hour {self.hour}: {'Present' if self.is_present else 'Absent'}"
    
class Course(models.Model):
    course_id = models.CharField(max_length=30,unique=True)
    course_name = models.CharField(max_length=30,unique=True,default= ' ')
    def __str__(self):
        return self.course_name
    


class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)  # e.g., 'semester-1', 'semester-2'
    exam_name = models.CharField(max_length=50)  # e.g., 'internal-1', 'model', etc.
    subject = models.CharField(max_length=100)  # Using course name as subject
    internal_marks = models.IntegerField()
    external_marks = models.IntegerField()

    def __str__(self):
        # Display the student register_id and subject in the mark's string representation
        return f"{self.student.register_id} - {self.subject} ({self.semester})"