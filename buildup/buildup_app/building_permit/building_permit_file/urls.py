from django.urls import path
from rest_framework.routers import DefaultRouter
from buildup_app.building_permit.building_permit_file.views import BuildingPermitFileViewSet

router = DefaultRouter()
router.register('building_permit_file', BuildingPermitFileViewSet)

urlpatterns = [
]

urlpatterns.extend(router.urls)