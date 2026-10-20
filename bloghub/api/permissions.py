from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """Anyone can read. Only the author can edit/delete."""

    def has_object_permission(self,request,view, obj):
        # Anyone can read
        if request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True

        return obj.author == request.user