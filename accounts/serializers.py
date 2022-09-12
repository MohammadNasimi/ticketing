from rest_framework import serializers
from accounts.models import User,Customer # If used custom user model

class Customerserilizer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('user','phone')
            

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'password','email', 'first_name', 'last_name')
        read_only_fields = ('id','email', 'first_name', 'last_name')