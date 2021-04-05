from django.contrib import admin

# Register your models here.
from .models import myProduct,contact, Orders, OrderUpdate

admin.site.register(myProduct)
admin.site.register(contact)
admin.site.register(Orders)
admin.site.register(OrderUpdate)
