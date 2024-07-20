from django.contrib import admin

# Register your models here.
from .models import Product
from .models import Cart
from .models import Order

# @admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','price','category','description','is_active','product_image']

admin.site.register(Product,ProductAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display=['userid','pid','qty']

admin.site.register(Cart)

class OrderAdmin(admin.ModelAdmin):
    list_display=['order_id','user_id','p_id','qty','amt']

admin.site.register(Order)