from django.urls import path
from rest_framework.routers import DefaultRouter
from buildup_app.file_template.views import FileTemplateViewSet

router = DefaultRouter()
router.register('file_template', FileTemplateViewSet)

urlpatterns = [
]

urlpatterns.extend(router.urls)