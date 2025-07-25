# from django.contrib import admin
# from .models import Category, FoodItem, Cart, Order, OrderItem
# admin.site.register(FoodItem)
# admin.site.register(Category)
# admin.site.register(Cart)
# admin.site.register(Order)
# admin.site.register(OrderItem)


from django.contrib import admin
from .models import Category, FoodItem, Cart, Address, Order, OrderItem
from .models import ContactMessage

# ✅ Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image')
    search_fields = ('name',)

# ✅ FoodItem Admin
@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'image')
    list_filter = ('category',)
    search_fields = ('name',)

# ✅ Cart Admin
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'food_item', 'quantity')
    search_fields = ('user__username', 'food_item__name')

# ✅ Address Admin
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address_line', 'phone', 'city', 'pincode', 'created_at')
    search_fields = ('user__username', 'phone', 'city')
    list_filter = ('city',)

# ✅ Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'status')

# ✅ OrderItem Admin
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'food_item', 'quantity', 'price', 'name', 'mobile')
    search_fields = ('order__id', 'food_item__name', 'name', 'mobile')




@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email", "message")