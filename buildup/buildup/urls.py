from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Users:
    path('api/buildup/', include('buildup_app.users.urls')),

    # Company Files:
    path('api/buildup/', include('buildup_app.company_file.urls')),

    # File Template:
    path('api/buildup/', include('buildup_app.file_template.urls')),

    # Section Template:
    path('api/buildup/', include('buildup_app.section_template.urls')),

    # Building Permit:
    path('api/buildup/', include('buildup_app.building_permit.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)