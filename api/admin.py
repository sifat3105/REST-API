from django.contrib import admin
from .models import Book, Product, Review

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    
    list_display = ('name', 'price', 'slug')  # Display these fields in the list view
    search_fields = ('name', 'slug')  # Enable search on 'name' and 'slug'

# Register the Product model with the custom admin configuration


admin.site.register(Book)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review)

