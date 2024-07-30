from django.contrib import admin
from .models import Category, Supplier, InventoryItem, UsedStock, InventoryUpdate

admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(InventoryItem)
admin.site.register(InventoryUpdate)
admin.site.register(UsedStock)
# admin.site.register(InventoryHistory)
