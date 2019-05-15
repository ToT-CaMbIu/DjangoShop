from django.contrib import admin
from polls import views

# Register your models here.
admin.site.register(views.Category)
admin.site.register(views.Brand)
admin.site.register(views.Product)
admin.site.register(views.Cart)
admin.site.register(views.CartItem)
admin.site.register(views.Order)
admin.site.register(views.ShopCharacteristic)
admin.site.register(views.Coupon)
