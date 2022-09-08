from rest_framework import serializers
from accounts.models import CustomerUser # If used custom user model

UserModel = CustomerUser


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = UserModel.objects.create(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )


        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)
        

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = UserModel
        fields = ('id', 'username', 'password','email', 'first_name', 'last_name')
        read_only_fields = ('id','email', 'first_name', 'last_name')