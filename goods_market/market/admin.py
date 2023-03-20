from django.contrib import admin

from .models import CustomUser, Goods, Order

admin.site.register(CustomUser)
admin.site.register(Goods)
admin.site.register(Order)
