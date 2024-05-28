# MyForm/urls.py

from django.urls import path
from . import views
from .views import purchase_select_view
from .views import admin_confirm_purchase

urlpatterns = [
    path('', views.form_view, name='buy_vm_form'),
    path('display/', views.display_view, name='display_view'),
    path('select/', purchase_select_view, name='purchase_select_view'),
    path('admin-confirm-purchase/<int:purchase_id>/', views.admin_confirm_purchase, name='admin-confirm-purchase'),
]
