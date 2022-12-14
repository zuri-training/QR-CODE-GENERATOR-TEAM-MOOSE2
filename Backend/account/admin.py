from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from account.models import User


# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):  # (UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'phone_number',
                    'temp_password', 'is_staff', 'is_superuser', 'created', 'updated')
    search_fields = ['username', 'email', 'first_name', 'last_name']
    # list_filter = ['user_type']


admin.site.register(User, CustomUserAdmin)
