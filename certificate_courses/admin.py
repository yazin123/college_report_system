# certificate_courses/admin.py
from django.contrib import admin
from .models import (
    Student, CertificateCourse, CourseEnrollment, 
    AttendanceRecord, Certificate, CourseReport
)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'registration_number', 'department')
    search_fields = ('name', 'registration_number')
    list_filter = ('department',)

@admin.register(CertificateCourse)
class CertificateCourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_code', 'department', 'start_date', 'end_date', 'status')
    search_fields = ('name', 'course_code')
    list_filter = ('department', 'status')

@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date')
    list_filter = ('course',)

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'date', 'is_present')
    list_filter = ('date', 'is_present')

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'issue_date')

@admin.register(CourseReport)
class CourseReportAdmin(admin.ModelAdmin):
    list_display = ('course', 'generated_at')