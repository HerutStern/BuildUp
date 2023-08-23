from django.urls import path
from rest_framework.routers import DefaultRouter
from buildup_app.building_permit.views import BuildingPermitViewSet

router = DefaultRouter()
router.register('building_permit', BuildingPermitViewSet)

urlpatterns = [
]

urlpatterns.extend(router.urls)
