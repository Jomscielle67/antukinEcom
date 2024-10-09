from django.contrib import admin
from .models import Category, Customer, Product, Order, Profile
from django.contrib.auth.models import User

# Custom admin titles
admin.site.site_header = "GROUP 5 Admin"
admin.site.site_title = "GROUP 5"
admin.site.index_title = "Welcome to GROUP 5 Portal"

# Registering models
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Profile)

# Mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile
    
# Extending user model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "first_name", "last_name", "email"]  # Changed 'field' to 'fields'
    inlines = [ProfileInline]

# Custom ProductAdmin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_sale', 'sale_price')
    fields = ('name', 'price', 'category', 'description', 'image_url', 'is_sale', 'sale_price')  # Use image_url field


# Unregister the old User admin
admin.site.unregister(User)

# Re-register the new User admin
admin.site.register(User, UserAdmin)
