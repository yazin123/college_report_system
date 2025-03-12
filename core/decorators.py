# core/decorators.py
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib import messages

def department_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'department'):
            messages.error(request, 'You need to be associated with a department to access this page.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff and not request.user.is_superuser:
            return HttpResponseForbidden("You don't have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper