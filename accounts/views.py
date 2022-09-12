from rest_framework import permissions
from rest_framework.views import APIView
from accounts.models import User,Customer # If used custom user model
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import  LoginSerializer 
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
class CreateUserView(APIView):
    def post(self, request, *args, **kwargs):
        if 'email' not in request.data:
            email=""
        else:
            email =request.data['email']
        if 'first_name' not in request.data:
            first_name=""
        else:
            first_name=request.data['first_name']
        if 'last_name' not in request.data:
            last_name=""
        else:
            last_name=request.data['last_name']
        if request.data.get('username') == None or request.data.get('password') == None  or request.data.get('phone') == None:
                return Response({"detail": "اطلاعات ارسالی کامل نیست."} , status=status.HTTP_400_BAD_REQUEST)
        try:
            user =User.objects.create_superuser(username=request.data['username'],password=request.data['password'],
                                    email=email,first_name=first_name,
                                    last_name=last_name,type = '2')
            Customer.objects.create(user =user ,phone =request.data['phone'])
        except:
            return Response({"detail"  : "username exist"} , status=status.HTTP_400_BAD_REQUEST)
        return Response(request.data, status=status.HTTP_201_CREATED)

        
 
class MyTokenObtainPairView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        if "password" not in request.data or "username" not in request.data:
            return Response({"detail": "اطلاعات ارسالی کامل نیست."} , status=status.HTTP_400_BAD_REQUEST)
        def get_token(user):
                refresh = RefreshToken.for_user(user)
                return {
                    'refresh':str(refresh),
                    'access':str(refresh.access_token)
                }

        user = authenticate(username = request.data['username'],password = request.data['password'])
        if user :
            token=get_token(user)
            data =LoginSerializer(user).data
            data['refresh']=token['refresh']
            data['access']=token['access']

            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response({'user':'wrong username or password'}, status=status.HTTP_200_OK)
