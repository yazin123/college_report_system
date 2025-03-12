# certificate_courses/urls.py (updated)
from django.urls import path
from . import views

urlpatterns = [
    # Certificate Course CRUD
    path('courses/', views.course_list, name='course_list'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('courses/<int:pk>/update/', views.course_update, name='course_update'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),
    path('courses/<int:pk>/outcome/', views.update_course_outcome, name='update_course_outcome'),
    
    # Student Management
    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:pk>/update/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    
    # Course Enrollment
    path('courses/<int:course_pk>/enrollment/', views.manage_enrollment, name='manage_enrollment'),
    
    # Attendance Management
    path('courses/<int:course_pk>/attendance/', views.attendance_list, name='attendance_list'),
    path('courses/<int:course_pk>/attendance/take/', views.take_attendance, name='take_attendance'),
    
    # Certificate Generation
    path('courses/<int:course_pk>/certificates/', views.generate_certificates, name='generate_certificates'),
    path('certificates/<int:certificate_pk>/', views.view_certificate, name='view_certificate'),
    
    # Report Generation
    path('courses/<int:course_pk>/report/', views.generate_report, name='generate_report'),
    path('reports/<int:report_pk>/', views.view_report, name='view_report'),

    path('students/import/', views.import_students, name='import_students'),

    path('courses/<int:pk>/status/', views.update_course_status, name='update_course_status'),
  
    path('courses/<int:pk>/export/', views.export_course_data, name='export_course_data'),

    path('templates/', views.template_list, name='template_list'),
    path('templates/create/', views.template_create, name='template_create'),
    path('templates/<int:pk>/update/', views.template_update, name='template_update'),
    path('templates/<int:pk>/delete/', views.template_delete, name='template_delete'),
    
]