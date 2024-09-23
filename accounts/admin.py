from django.contrib import admin

# Register your models here.
#created 
# from .models import Customer,Products,Order
# instead
from .models import *
admin.site.register(Customer)
admin.site.register(Products)
admin.site.register(Tag)
admin.site.register(Order)

