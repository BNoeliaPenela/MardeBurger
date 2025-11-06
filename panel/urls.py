from django.urls import path
from . import views

urlpatterns = [
    # Autenticación
    path('login/', views.PanelLoginView.as_view(), name='panel_login'),
    path('logout/', views.PanelLogoutView.as_view(), name='panel_logout'),
    
    # Dashboard
    path('', views.DashboardView.as_view(), name='panel_dashboard'),
    
    # Categorías
    path('categorias/', views.CategoriaListView.as_view(), name='panel_categoria_list'),
    path('categorias/crear/', views.CategoriaCreateView.as_view(), name='panel_categoria_create'),
    path('categorias/<int:pk>/editar/', views.CategoriaUpdateView.as_view(), name='panel_categoria_update'),
    path('categorias/<int:pk>/eliminar/', views.CategoriaDeleteView.as_view(), name='panel_categoria_delete'),
    
    # Productos
    path('productos/', views.ProductoListView.as_view(), name='panel_producto_list'),
    path('productos/crear/', views.ProductoCreateView.as_view(), name='panel_producto_create'),
    path('productos/<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='panel_producto_update'),
    path('productos/<int:pk>/eliminar/', views.ProductoDeleteView.as_view(), name='panel_producto_delete'),
    
    # Pedidos
    path('pedidos/', views.PedidoListView.as_view(), name='panel_pedido_list'),
    path('pedidos/<int:pk>/cancelar/', views.PedidoDeleteView.as_view(), name='panel_pedido_delete'),
]