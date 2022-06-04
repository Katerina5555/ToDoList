from rest_framework.permissions import BasePermission, SAFE_METHODS


class EditNotePermission(BasePermission):
    def author_permission(self, request, obj):
        if request.method in SAFE_METHODS:
            return request.user == obj.author


class EditPublicNotePermission(BasePermission):
    def public_permission(self, request, obj):
        if request.method in SAFE_METHODS:
            if obj.is_public:
                return True
            else:
                return False
