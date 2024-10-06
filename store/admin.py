from django.contrib import admin
from .models import Category,Customer,Product,Order,Profile
from django.contrib.auth.models import User

admin.site.site_header = "GROUP 5 Admin"
admin.site.site_title = "GROUP 5"
admin.site.index_title = "Welcome to GROUP 5 Portal"
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)

# Mix profile info and user info
class ProfileInline (admin.StackedInline):
    model = Profile
    
# Extends user model
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]
    
#Unregister the old way
admin.site.unregister(User)

#Re-register the new way
admin.site.register(User, UserAdmin)