from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission
from buildup_app.models import Profile

# The ManagerPermission is for when anyone csn use "list" and "retrieve",
# otherwise you have to be a 'COMPANY_MANAGER'

class ManagerPermission(BasePermission):

    def has_permission(self, request, view):
        # User Profile -
        profile = get_object_or_404(Profile, user=request.user.id)

        # Condition -
        if view.action == 'create':
            # Only COMPANY_MANAGER can create -
            return profile.role == 'COMPANY_MANAGER' # Returns True for company managers

        # Otherwise -
        return True

    def has_object_permission(self, request, view, obj):
        # User Profile -
        profile = get_object_or_404(Profile, user=request.user.id)

        # Condition -
        if view.action in ['update', 'partial_update', 'destroy']:

            # Only COMPANY_MANAGER can update, partial_update, and destroy -
            return profile.role == 'COMPANY_MANAGER' # Returns True for company managers

        # Otherwise -
        return True
