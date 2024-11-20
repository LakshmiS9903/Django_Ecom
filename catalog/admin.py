from django.contrib import admin
from .models import ParentProduct, ChildProduct, AddToCart, WishList

@admin.register(ParentProduct)
class ParentProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')

@admin.register(ChildProduct)
class ChildProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'price', 'created_at', 'updated_at')

admin.site.register(AddToCart)
admin.site.register(WishList)