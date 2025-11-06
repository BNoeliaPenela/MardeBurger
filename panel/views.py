from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from menu.models import Producto, Categoria, Pedido
from django.db.models import Q

# ============================================
# AUTENTICACIÓN
# ============================================

class PanelLoginView(LoginView):
    """Vista de login personalizada"""
    template_name = 'panel/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('panel_dashboard')


class PanelLogoutView(LogoutView):
    """Vista de logout"""
    next_page = reverse_lazy('panel_login')


# ============================================
# DASHBOARD
# ============================================

class DashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard principal del panel"""
    template_name = 'panel/dashboard.html'
    login_url = reverse_lazy('panel_login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_productos'] = Producto.objects.count()
        context['total_categorias'] = Categoria.objects.count()
        context['total_pedidos'] = Pedido.objects.count()
        context['productos_disponibles'] = Producto.objects.filter(disponible=True).count()
        context['ultimos_pedidos'] = Pedido.objects.all()[:5]
        return context


# ============================================
# GESTIÓN DE CATEGORÍAS
# ============================================

class CategoriaListView(LoginRequiredMixin, ListView):
    """Lista de categorías"""
    model = Categoria
    template_name = 'panel/categoria_list.html'
    context_object_name = 'categorias'
    login_url = reverse_lazy('panel_login')
    ordering = ['orden', 'nombre']


class CategoriaCreateView(LoginRequiredMixin, CreateView):
    """Crear categoría"""
    model = Categoria
    template_name = 'panel/categoria_form.html'
    fields = ['nombre', 'orden']
    success_url = reverse_lazy('panel_categoria_list')
    login_url = reverse_lazy('panel_login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Categoría creada exitosamente')
        return super().form_valid(form)


class CategoriaUpdateView(LoginRequiredMixin, UpdateView):
    """Editar categoría"""
    model = Categoria
    template_name = 'panel/categoria_form.html'
    fields = ['nombre', 'orden']
    success_url = reverse_lazy('panel_categoria_list')
    login_url = reverse_lazy('panel_login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Categoría actualizada exitosamente')
        return super().form_valid(form)


class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    """Eliminar categoría"""
    model = Categoria
    template_name = 'panel/categoria_confirm_delete.html'
    success_url = reverse_lazy('panel_categoria_list')
    login_url = reverse_lazy('panel_login')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Categoría eliminada exitosamente')
        return super().delete(request, *args, **kwargs)


# ============================================
# GESTIÓN DE PRODUCTOS
# ============================================

class ProductoListView(LoginRequiredMixin, ListView):
    """Lista de productos"""
    model = Producto
    template_name = 'panel/producto_list.html'
    context_object_name = 'productos'
    login_url = reverse_lazy('panel_login')
    ordering = ['categoria', 'nombre']
    paginate_by = 12


class ProductoCreateView(LoginRequiredMixin, CreateView):
    """Crear producto"""
    model = Producto
    template_name = 'panel/producto_form.html'
    fields = ['nombre', 'descripcion', 'precio', 'imagen', 'categoria', 'disponible', 'destacado']
    success_url = reverse_lazy('panel_producto_list')
    login_url = reverse_lazy('panel_login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Producto creado exitosamente')
        return super().form_valid(form)


class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    """Editar producto"""
    model = Producto
    template_name = 'panel/producto_form.html'
    fields = ['nombre', 'descripcion', 'precio', 'imagen', 'categoria', 'disponible', 'destacado']
    success_url = reverse_lazy('panel_producto_list')
    login_url = reverse_lazy('panel_login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Producto actualizado exitosamente')
        return super().form_valid(form)


class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    """Eliminar producto"""
    model = Producto
    template_name = 'panel/producto_confirm_delete.html'
    success_url = reverse_lazy('panel_producto_list')
    login_url = reverse_lazy('panel_login')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Producto eliminado exitosamente')
        return super().delete(request, *args, **kwargs)


# ============================================
# GESTIÓN DE PEDIDOS
# ============================================

class PedidoListView(LoginRequiredMixin, ListView):
    """Lista de pedidos con búsqueda y filtros"""
    model = Pedido
    template_name = 'panel/pedido_list.html'
    context_object_name = 'pedidos'
    login_url = reverse_lazy('panel_login')
    ordering = ['-fecha']
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Búsqueda por número de orden o nombre
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(id__icontains=search) | 
                Q(nombre_cliente__icontains=search)
            )
        
        # Filtro por tipo de entrega
        tipo_entrega = self.request.GET.get('tipo_entrega')
        if tipo_entrega:
            queryset = queryset.filter(tipo_entrega=tipo_entrega)
        
        return queryset

class PedidoDeleteView(LoginRequiredMixin, DeleteView):
    """Cancelar/Eliminar pedido"""
    model = Pedido
    success_url = reverse_lazy('panel_pedido_list')
    login_url = reverse_lazy('panel_login')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, f'Pedido #{self.get_object().id} cancelado exitosamente')
        return super().delete(request, *args, **kwargs)
