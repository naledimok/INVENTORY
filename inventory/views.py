from datetime import datetime
from io import BytesIO
from django.utils import timezone
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from .models import InventoryItem, Category, Supplier, UsedStock
from django.db import  transaction
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def inventory_list(request):
    items = InventoryItem.objects.all()
    return render(request, 'index.html', {'items': items})
def save_inventory(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        item_name = request.POST.get('item_name')
        category_name = request.POST.get('category')
        supplier_name = request.POST.get('supplier')
        quantity_in_stock = request.POST.get('quantity_in_stock')
        unit_of_measure = request.POST.get('unit_of_measure')
        reorder_level = request.POST.get('reorder_level')
        reorder_quantity = request.POST.get('reorder_quantity')
        purchase_price = request.POST.get('purchase_price')
        selling_price = request.POST.get('selling_price')
        date_of_last_order = request.POST.get('date_of_last_order')
        expiration_date = request.POST.get('expiration_date')
        storage_location = request.POST.get('storage_location')
        notes = request.POST.get('notes')
        
        # Fetch or create the category and supplier
        category, created = Category.objects.get_or_create(name=category_name)
        supplier, created = Supplier.objects.get_or_create(name=supplier_name)
        
        # Create a new inventory item
        InventoryItem.objects.create(
            item_id=item_id,
            item_name=item_name,
            category=category,
            supplier=supplier,
            quantity_in_stock=quantity_in_stock,
            unit_of_measure=unit_of_measure,
            reorder_level=reorder_level,
            reorder_quantity=reorder_quantity,
            purchase_price=purchase_price,
            selling_price=selling_price,
            date_of_last_order=date_of_last_order,
            expiration_date=expiration_date,
            storage_location=storage_location,
            notes=notes
        )
        
        return HttpResponseRedirect(reverse('inventory_list'))
    return HttpResponseRedirect(reverse('inventory_list'))


def update_inventory(request):
    items = InventoryItem.objects.all()
    used_stocks = UsedStock.objects.all()
    return render(request, 'update_inventory.html', {'items': items, 'used_stocks': used_stocks})

def save_updated_inventory(request):
    if request.method == 'POST':
        items = InventoryItem.objects.all()
        try:
            with transaction.atomic():
                for item in items:
                    new_quantity = request.POST.get(f'new_quantity_{item.item_id}')
                    if new_quantity is not None:
                        new_quantity = int(new_quantity)
                        if new_quantity < item.quantity_in_stock:
                            quantity_used = item.quantity_in_stock - new_quantity
                            UsedStock.objects.create(
                                item=item,
                                quantity_used=quantity_used,
                                date=timezone.now()
                            )
                        item.quantity_in_stock = new_quantity
                        item.save()
        except Exception as e:
            print(f"Error updating inventory: {e}")
            return redirect('update_inventory')  # Redirect to the same page on error

    return redirect('inventory_list')

def delete_inventory_item(request, item_id):
    item = get_object_or_404(InventoryItem, item_id=item_id)
    item.delete()
    return redirect('inventory_list')

def inventory_pdf(request):
    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()
    
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Header
    p.setFont("Helvetica", 14)
    p.drawString(200, height - 40, "Inventory List")

    # Add the current date at the top right corner
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    p.setFont("Helvetica", 10)
    p.drawString(width - 150, height - 40, f"Date: {current_date}")

    # Table Header
    y_position = height - 80
    p.setFont("Helvetica", 10)
    p.drawString(30, y_position, "Item ID")
    p.drawString(100, y_position, "Item Name")
    p.drawString(200, y_position, "Category")
    p.drawString(300, y_position, "Supplier")
    p.drawString(400, y_position, "Quantity")
    
    # Table Content
    y = y_position - 20
    items = InventoryItem.objects.all()
    for item in items:
        p.drawString(30, y, item.item_id)
        p.drawString(100, y, item.item_name)
        p.drawString(200, y, str(item.category))
        p.drawString(300, y, str(item.supplier))
        p.drawString(400, y, str(item.quantity_in_stock))
        y -= 20
        if y < 40:
            p.showPage()
            y = height - 40

    # Close the PDF object cleanly, and return the buffer's contents.
    p.showPage()
    p.save()
    
    # File response
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

def delete_all(request):
    InventoryItem.objects.all().delete()
    return redirect('inventory_list')

def used_stock_pdf(request):
    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()
    
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Header
    p.setFont("Helvetica", 14)
    p.drawString(200, height - 40, "Used Stocks")

    # Add the current date at the top right corner
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    p.setFont("Helvetica", 10)
    p.drawString(width - 150, height - 40, f"Date: {current_date}")

    # Table Header
    y_position = height - 80
    p.setFont("Helvetica", 10)
    p.drawString(30, y_position, "Item ID")
    p.drawString(100, y_position, "Item Name")
    p.drawString(200, y_position, "Quantity Used")
    p.drawString(300, y_position, "Date")
    
    # Table Content
    y = y_position - 20
    used_stocks = UsedStock.objects.all()
    for used_stock in used_stocks:
        p.drawString(30, y, used_stock.item.item_id)
        p.drawString(100, y, used_stock.item.item_name)
        p.drawString(200, y, str(used_stock.quantity_used))
        p.drawString(300, y, used_stock.date.strftime("%Y-%m-%d %H:%M:%S"))
        y -= 20
        if y < 40:
            p.showPage()
            y = height - 40
            
    p.showPage()
    p.save()
    
    # File response
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

def delete_all_used(request):
    UsedStock.objects.all().delete()
    return redirect('update_inventory/')
