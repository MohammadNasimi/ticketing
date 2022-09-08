from genericpath import exists
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from accounts.models import CustomerUser # If used custom user model
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer ,LoginSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
class CreateUserView(CreateAPIView):

    model = CustomerUser
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer

 
class MyTokenObtainPairView(generics.GenericAPIView):
    queryset = CustomerUser.objects.all()
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        def get_token(user):
                refresh = RefreshToken.for_user(user)
                return {
                    'refresh':str(refresh),
                    'access':str(refresh.access_token)
                }

        user = authenticate(username = request.data['username'],password = request.data['password'])
        print(user)
        if user :
            token=get_token(user)
            data =LoginSerializer(user).data
            data['refresh']=token['refresh']
            data['access']=token['access']

            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response({'user':'wrong username or password'}, status=status.HTTP_200_OK)


    