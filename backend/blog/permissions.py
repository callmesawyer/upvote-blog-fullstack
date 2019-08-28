from rest_framework import permissions
from .models import Post, Comment


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):

        # import ipdb
        # ipdb.set_trace()
        if request.method.lower() == 'put':
            # Instance must have an attribute named `owner`.
            return obj.author == request.user
        if request.method.lower() == 'delete':
            # import ipdb
            # ipdb.set_trace()
            if isinstance(obj, Comment):
                return obj.author == request.user or obj.post.author == request.user
            return obj.author == request.user

        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.author == request.user or request.user.is_superuser
