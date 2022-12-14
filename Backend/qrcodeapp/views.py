from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.response import Response
from ipware.ip import get_client_ip
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.




class TestApi(APIView):
    login_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
       
    )

    @swagger_auto_schema(
        operation_description="Test to the API",
        tags=['Test API'],

        responses={200: login_response_schema}
    )
    def get(self, request):
        ip_address = get_client_ip(request)
        data = {'status': f'Everything is okay {ip_address[0]}', 'code': 200}
        return Response(data)
