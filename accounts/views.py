from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from accounts.models import CustomerUser # If used custom user model

from .serializers import UserSerializer


class CreateUserView(CreateAPIView):

    model = CustomerUser
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer
