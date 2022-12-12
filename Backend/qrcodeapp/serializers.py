from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "first_name", "last_name", "username", "email", "password", "password2",
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'password': {'write_only': True, 'required': True},
            'password2': {'write_only': True, 'required': True}
        }

        def validate(self, attrs):
            email = attrs.get('email')
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    {"email": "email already exist"})

            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError(
                    {"password": "password fields didn't match."})
            return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        # saves the following validated data to database
        user.set_password(validated_data['password'])
        user.save()
        return user


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        # define the validated method

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                'The username should only contain alphanumeric characters')

        # return super().validate(attrs)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
