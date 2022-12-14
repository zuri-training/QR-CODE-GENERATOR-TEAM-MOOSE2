from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from account.models import User
from account.serializers import LoginSerializer, RegistrationSerializer
from account.tokens import creat_jwt_pair_for_user
from rest_framework import generics, status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.request import Request


# Create your views here.

class LoginView(APIView):
    # Create the view and use the @swagger_auto_schema decorator

    login_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'token': openapi.Schema(type=openapi.TYPE_STRING),
        }
    )

    @swagger_auto_schema(
        operation_description="Login to the API",
        request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    }
),
        tags=['account'],

        responses={200: login_response_schema}
    )
    def post(self, request):
        try:
            username = request.data.get('username', '')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:

                user_details = User.objects.get(id=user.id)
                userdata = LoginSerializer(instance=user_details).data

                # print(userdata)
                tokens = creat_jwt_pair_for_user(user)
                response = {
                    "user": userdata,
                    "message": "Login successful",
                    "token": tokens,
                }
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                response = {"message": "Invalid username or password"}
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)


class SignUpView(APIView):
    # serializer_class = RegistrationSerializer
    
        # Create the view and use the @swagger_auto_schema decorator

    login_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
            'gender': openapi.Schema(type=openapi.TYPE_STRING),
            'created': openapi.Schema(type=openapi.TYPE_STRING),
            'updated': openapi.Schema(type=openapi.TYPE_STRING),
        }
    )

    @swagger_auto_schema(
        operation_description="Registration API",
        request_body=RegistrationSerializer,
        tags=['account'],

        responses={200: login_response_schema}
    )

    def post(self, request: Request):
        data = request.data
        # print(data)
        serializer = RegistrationSerializer(data=request.data)
        # print(serializer)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "User Created Successfully",
                "data": serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)