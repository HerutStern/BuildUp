from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS

from buildup_app.models import Profile
from buildup_app.users.serializers import ProfileSerializer


class ManagerPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            profile = get_object_or_404(Profile, user=request.user.id)
            return profile.role == 'COMPANY_MANAGER'
        return True
    def has_object_permission(self, request, view, obj):
        if view.action == 'destroy' or view.action == 'update':
            profile = get_object_or_404(Profile, user=request.user.id)
            return profile.role == 'COMPANY_MANAGER'
        return True
