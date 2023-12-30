from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminUserOrReadOnly(BasePermission):
    """Allow access to admin users and read-only for others."""

    def has_permission(self, request, view):
        """Check if user is admin or request is safe."""
        return bool(request.method in SAFE_METHODS or request.user and request.user.is_staff)
