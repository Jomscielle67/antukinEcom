from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User #incase na kailangan hahah 

# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

class OrderItemInline (admin.StackedInline):
    model =  OrderItem
    extra = 0
    
#extend our order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    fields = ["user", "full_name", "email", "shipping_address", "amount_paid", "date_ordered", "shipped", "date_shipped", "invoice", "paid"] #para pili lang lalabas hahaha
    inlines = [OrderItemInline]
    
    #tangena bat di gumana...
    #try kaya unregister tong hayop nato tas register ulet
    
admin.site.unregister(Order)

#re-register this shits
admin.site.register(Order, OrderAdmin)