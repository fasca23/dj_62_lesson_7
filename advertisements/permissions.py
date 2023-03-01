
from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # print(request.user.is_staff)
        if request.method == 'GET':
            # print(request.method)
            return True
        return request.user == obj.creator