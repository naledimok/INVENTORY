from datetime import date
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField(blank=True)

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    item_id = models.CharField(max_length=100, unique=True)
    item_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity_in_stock = models.IntegerField()
    unit_of_measure = models.CharField(max_length=100)
    reorder_level = models.IntegerField()
    reorder_quantity = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_last_order = models.DateField(default=date.today)
    expiration_date = models.DateField()
    storage_location = models.CharField(max_length=100)
    notes = models.TextField()

    def __str__(self):
        return self.item_name

class InventoryUpdate(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    new_quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.item_name} - Updated to {self.new_quantity} on {self.date}"
    
    
class UsedStock(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity_used = models.IntegerField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.item.item_name} - {self.quantity_used} used on {self.date}"

# class InventoryHistory(models.Model):
#     date_saved = models.DateField()
#     file_path = models.CharField(max_length=255)

#     @property
#     def file_url(self):
#         return f'/media/{self.file_path}'

#     def __str__(self):
#         return f"Inventory saved on {self.date_saved}"
