from django.contrib import admin
from .models import ClothType, ServiceType, Address, Orders, OrderNumber, Discounds

# Register your models here.

admin.site.register(ClothType)
admin.site.register(ServiceType)
admin.site.register(Orders)
admin.site.register(Address)
admin.site.register(OrderNumber)
admin.site.register(Discounds)