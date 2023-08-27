from django.contrib import admin
from home.models import *
# Register your models here.
admin.site.register(AppointmentRequest)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(Orderitem)
admin.site.register(Profile)
admin.site.register(Feedback)