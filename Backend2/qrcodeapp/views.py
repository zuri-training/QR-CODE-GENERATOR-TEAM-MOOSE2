from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer
from .models import User
# from django.contrib.auth.models import User
# Class based view to Get User Details using Token Authentication


class UserDetailAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    # Class based view to register user


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# former recent views

# from django.contrib.auth.models import User
# from rest_framework import status, viewsets
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from django.shortcuts import render
# from rest_framework import generics, status
# from qrcodeapp.serializers import RegisterSerializer
# from rest_framework.response import Response
# # from qrcodeapp.serializers import UserSerializer


# class RegisterView(generics.GenericAPIView):
#     serializer_class = RegisterSerializer

#     def post(self, request):
#         user = request.data
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         user_data = serializer.data

#         return Response(user_data, status=status.HTTP_201_CREATED)


# initial oldest Views

# class UserViewSet(viewsets.ModelViewSet):
#     """
#     A viewset that provides the standard actions
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# @action(detail=True, methods=['post'])
# def set_password(self, request, pk=None):
#     user = self.get_object()
#     serializer = PasswordSerializer(data=request.data)
#     if serializer.is_valid():
#         user.set_password(serializer.validated_data['password'])
#         user.save()
#         return Response({'status': 'password set'})
#     else:
#         return Response(serializer.errors,
#                         status=status.HTTP_400_BAD_REQUEST)

# @action(detail=False)
# def recent_users(self, request):
#     recent_users = User.objects.all().order_by('-last_login')

#     page = self.paginate_queryset(recent_users)
#     if page is not None:
#         serializer = self.get_serializer(page, many=True)
#         return self.get_paginated_response(serializer.data)

#     serializer = self.get_serializer(recent_users, many=True)
#     return Response(serializer.data)
