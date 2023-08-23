from django.urls import path
from rest_framework.routers import DefaultRouter
from buildup_app.company_file.views import CompanyFileViewSet

router = DefaultRouter()
router.register('company_file', CompanyFileViewSet)

urlpatterns = [
]

urlpatterns.extend(router.urls)
