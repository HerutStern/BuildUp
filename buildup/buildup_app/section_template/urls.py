from django.urls import path
from rest_framework.routers import DefaultRouter
from buildup_app.section_template.views import SectionTemplateViewSet

router = DefaultRouter()
router.register('section_template', SectionTemplateViewSet)

urlpatterns = [
]

urlpatterns.extend(router.urls)