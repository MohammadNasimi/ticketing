from rest_framework.permissions import BasePermission ,SAFE_METHODS
class Ticketpermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        
        if request.method  == 'POST' and request.user.type =='2':
            return True
