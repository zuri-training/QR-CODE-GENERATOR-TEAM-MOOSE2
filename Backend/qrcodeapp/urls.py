from django.urls import path
from qrcodeapp.views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register")
]
