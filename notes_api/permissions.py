from rest_framework.permissions import BasePermission, SAFE_METHODS


class EditNotePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            if obj.is_public:
                return True
            else:
                return request.user == obj.author
        return request.user == obj.author
