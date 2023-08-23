from django.urls import path
from rest_framework.routers import DefaultRouter
from buildup_app.building_permit.building_permit_section.views import BuildingPermitSectionViewSet

router = DefaultRouter()
router.register('building_permit_section', BuildingPermitSectionViewSet)

urlpatterns = [
]

urlpatterns.extend(router.urls)
