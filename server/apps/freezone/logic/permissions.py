from rest_framework.permissions import BasePermission


class IsAdminOrOwner(BasePermission):
    """Permission to check if user is admin or owner of the object."""

    def has_object_permission(self, request, view, obj):
        """Check if user is admin or owner of the object."""
        return request.user.is_staff or obj.user == request.user
