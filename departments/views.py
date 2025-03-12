# departments/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import DepartmentLoginForm

from django.utils import timezone
from certificate_courses.models import CourseEnrollment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = DepartmentLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = DepartmentLoginForm()
        
    return render(request, 'departments/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# departments/views.py (updated dashboard view)
@login_required
def dashboard(request):
    department = request.user.department
    certificate_courses = department.certificate_courses.all()
    
    # Get status counts for visual representation
    planning_count = certificate_courses.filter(status='planning').count()
    ongoing_count = certificate_courses.filter(status='ongoing').count()
    completed_count = certificate_courses.filter(status='completed').count()
    
    # Get total students in the department
    total_students = department.students.count()
    
    # Get total enrollments across all courses
    total_enrollments = CourseEnrollment.objects.filter(course__department=department).count()
    
    # Get recent courses (last 5)
    recent_courses = certificate_courses.order_by('-created_at')[:5]
    
    # Get upcoming courses (courses starting in the future)
    today = timezone.now().date()
    upcoming_courses = certificate_courses.filter(start_date__gt=today).order_by('start_date')[:5]
    
    context = {
        'department': department,
        'certificate_courses': certificate_courses,
        'planning_count': planning_count,
        'ongoing_count': ongoing_count,
        'completed_count': completed_count,
        'total_students': total_students,
        'total_enrollments': total_enrollments,
        'recent_courses': recent_courses,
        'upcoming_courses': upcoming_courses,
    }
    
    return render(request, 'departments/dashboard.html', context)