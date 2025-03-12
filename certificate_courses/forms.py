# certificate_courses/forms.py
from django import forms
from .models import CertificateCourse, Student, CourseEnrollment, AttendanceRecord, Certificate, CertificateTemplate

class CertificateCourseForm(forms.ModelForm):
    class Meta:
        model = CertificateCourse
        fields = ['name', 'course_code', 'start_date', 'end_date', 
                 'num_modules', 'total_hours', 'brochure', 'course_objective']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'course_code': forms.TextInput(attrs={'class': 'form-control'}),
            'num_modules': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'brochure': forms.FileInput(attrs={'class': 'form-control'}),
            'course_objective': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class CourseOutcomeForm(forms.ModelForm):
    class Meta:
        model = CertificateCourse
        fields = ['course_outcome', 'status']
        widgets = {
            'course_outcome': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'registration_number', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class CourseEnrollmentForm(forms.Form):
    students = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        department = kwargs.pop('department', None)
        super(CourseEnrollmentForm, self).__init__(*args, **kwargs)
        
        if department:
            self.fields['students'].queryset = Student.objects.filter(department=department)

class AttendanceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        enrollments = kwargs.pop('enrollments', None)
        date = kwargs.pop('date', None)
        super(AttendanceForm, self).__init__(*args, **kwargs)
        
        if enrollments:
            for enrollment in enrollments:
                field_name = f'attendance_{enrollment.id}'
                initial = False
                if date:
                    try:
                        record = AttendanceRecord.objects.get(enrollment=enrollment, date=date)
                        initial = record.is_present
                    except AttendanceRecord.DoesNotExist:
                        pass
                
                self.fields[field_name] = forms.BooleanField(
                    label=enrollment.student.name,
                    required=False,
                    initial=initial
                )
class StudentBulkImportForm(forms.Form):
    csv_file = forms.FileField(
        label='CSV File',
        help_text='CSV file should have columns: name, registration_number, email',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )


class CertificateTemplateForm(forms.ModelForm):
    class Meta:
        model = CertificateTemplate
        fields = ['name', 'template_file']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'template_file': forms.FileInput(attrs={'class': 'form-control'}),
        }