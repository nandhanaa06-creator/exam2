from django.contrib import admin
from .models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "stock")
    list_editable = ("stock",)  # allows editing stock directly in product list
    search_fields = ("name",)
    list_filter = ("category",)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
