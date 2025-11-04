from django.urls import path
from . import views

urlpatterns = [
    # Páginas principales
    path('', views.HomeView.as_view(), name='home'),
    path('menu/', views.MenuView.as_view(), name='menu'),
    path('producto/<int:pk>/', views.ProductoDetailView.as_view(), name='producto_detail'),

    # Proceso de compra
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('pedido-confirmado/', views.PedidoConfirmadoView.as_view(), name='pedido_confirmado'),

     # API endpoints
    path('api/actualizar-carrito/', views.ActualizarCarritoView.as_view(), name='actualizar_carrito'),
]