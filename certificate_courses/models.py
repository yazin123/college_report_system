# certificate_courses/models.py
from django.db import models
from departments.models import Department

class Student(models.Model):
    name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.registration_number})"

class CertificateCourse(models.Model):
    STATUS_CHOICES = (
        ('planning', 'Planning'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    )
    
    name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='certificate_courses')
    start_date = models.DateField()
    end_date = models.DateField()
    num_modules = models.PositiveIntegerField()
    total_hours = models.PositiveIntegerField()
    brochure = models.FileField(upload_to='brochures/', blank=True, null=True)
    course_objective = models.TextField()
    course_outcome = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.course_code})"
    
    def is_completed(self):
        return self.status == 'completed'
    
    def can_generate_report(self):
        # Check if all required fields are filled and course is completed
        if not self.is_completed():
            return False
        
        if not self.course_outcome:
            return False
            
        # Check if all enrolled students have attendance records and certificates
        for enrollment in self.enrollments.all():
            if not enrollment.has_attendance() or not enrollment.has_certificate():
                return False
                
        return True

class CourseEnrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(CertificateCourse, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'course')
    
    def __str__(self):
        return f"{self.student.name} enrolled in {self.course.name}"
    
    def has_attendance(self):
        return self.attendance_records.exists()
    
    def has_certificate(self):
        return hasattr(self, 'certificate')

class AttendanceRecord(models.Model):
    enrollment = models.ForeignKey(CourseEnrollment, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    is_present = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('enrollment', 'date')
    
    def __str__(self):
        status = "Present" if self.is_present else "Absent"
        return f"{self.enrollment.student.name} - {self.date} - {status}"

class Certificate(models.Model):
    enrollment = models.OneToOneField(CourseEnrollment, on_delete=models.CASCADE, related_name='certificate')
    certificate_file = models.FileField(upload_to='certificates/')
    issue_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Certificate for {self.enrollment.student.name} - {self.enrollment.course.name}"

class CourseReport(models.Model):
    course = models.OneToOneField(CertificateCourse, on_delete=models.CASCADE, related_name='report')
    report_file = models.FileField(upload_to='reports/')
    generated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Report for {self.course.name}"
    

class CertificateTemplate(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='certificate_templates')
    template_file = models.FileField(upload_to='certificate_templates/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name