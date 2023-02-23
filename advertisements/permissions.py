from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET'and obj.data.get['status'] != 'DRAFT':
            print(obj.data.get['status'])
            return True
        return request.user == obj.creator