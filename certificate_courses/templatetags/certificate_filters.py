# certificate_courses/templatetags/certificate_filters.py
from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def has_certificate(enrollment):
    return hasattr(enrollment, 'certificate')

@register.filter
def count_with_certificates(enrollments):
    count = 0
    for enrollment in enrollments:
        if hasattr(enrollment, 'certificate'):
            count += 1
    return count

@register.filter
def percentage(value, total):
    if total == 0:
        return 0
    return int((value / total) * 100)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, False)

@register.filter
def days(timedelta_str):
    # This is a simple approximation - in a real app you would want a more robust solution
    try:
        # Try to extract the number of days from the timedelta string
        days_str = timedelta_str.split(',')[0]
        if 'day' in days_str:
            return int(days_str.split()[0])
        return 0
    except:
        return 0
    
@register.filter
def get_dict_item(dictionary, key):
    """Get an item from a dictionary."""
    if dictionary is None:
        return False
    try:
        return dictionary.get(key, False)
    except (AttributeError, TypeError):
        return False

@register.filter
def multiply(value, arg):
    """Multiply the value by the argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def divide(value, arg):
    """Divide the value by the argument."""
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0