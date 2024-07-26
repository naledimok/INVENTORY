"""
URL configuration for inventory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.conf import settings
# from django.conf.urls.static import static
from django.urls import path
from .views import inventory_list, save_inventory, update_inventory, save_updated_inventory, delete_inventory_item, inventory_pdf, delete_all, used_stock_pdf, delete_all_used

urlpatterns = [
    path('', inventory_list, name='inventory_list'),
    path('save/', save_inventory, name='save_inventory'),
    path('update_inventory/', update_inventory, name='update_inventory'),
    path('save_updated_inventory/', save_updated_inventory, name='save_updated_inventory'),
    path('delete/<str:item_id>/', delete_inventory_item, name='delete_inventory_item'),
    path('inventory_pdf/', inventory_pdf, name='inventory_pdf'),
    path('delete_all/', delete_all, name='delete_all'),
    path('used_stock_pdf/', used_stock_pdf, name='used_stock_pdf'),
    path('delete/', delete_all_used, name='delete_all_used'),
    # path('history/', history, name='history'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
