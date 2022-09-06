import imp
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomerUser
# Register your models here.

 
class CustomerUserAdmin(UserAdmin):
    model = CustomerUser
    list_display = ['email', 'username', 'type', 'is_staff', ] 
    fieldsets = (
        ('General' , {'fields':['email', 'username',  'is_staff', ]}),
        ('type',{'fields': ['type']})
        )
    

    list_filter = ['email', 'username', 'type', 'is_staff']
    search_fields = ['email', 'username', 'type', 'is_staff']

admin.site.register(CustomerUser,CustomerUserAdmin)