from rest_framework import serializers
from account.models import User


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65, min_length=8, write_only=True)
    username = serializers.CharField(max_length=225, min_length=4)

    class Meta:
        model = User
        fields = ['username', 'password']




class RegistrationSerializer(serializers.ModelSerializer):
    
        class Meta:
            model = User
            fields = ['username', 'first_name', 'last_name', 'email',
                  'phone_number', 'gender', 'created', 'updated']