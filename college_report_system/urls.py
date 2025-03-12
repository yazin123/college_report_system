# college_report_system/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('departments.urls')),
    path('departments/', include('departments.urls')),
    path('certificates/', include('certificate_courses.urls')),
]

# Add this to handle media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)