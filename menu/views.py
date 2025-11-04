from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views import View
from .models import Producto, Categoria, Pedido, ItemPedido
from .forms import PedidoForm
import json
import urllib.parse

class HomeView(TemplateView):
    """Vista principal del sitio"""
    template_name = 'menu/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['destacados'] = Producto.objects.filter(
            destacado=True, 
            disponible=True
        )[:4]
        return context
    
class MenuView(ListView):
    """Vista del menú completo con todos los productos"""
    model = Producto
    template_name = 'menu/menu.html'
    context_object_name = 'productos'
    
    def get_queryset(self):
        return Producto.objects.filter(disponible=True).select_related('categoria')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context


class ProductoDetailView(DetailView):
    """Vista de detalle de un producto específico"""
    model = Producto
    template_name = 'menu/producto_detail.html'
    context_object_name = 'producto'


class CheckoutView(FormView):
    """Vista para finalizar el pedido"""
    template_name = 'menu/checkout.html'
    form_class = PedidoForm
    success_url = reverse_lazy('pedido_confirmado')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos'] = Producto.objects.all()
        return context
    
    def form_valid(self, form):
        # Obtener carrito de la sesión
        carrito = self.request.session.get('carrito', {})
        
        if not carrito:
            return redirect('menu')
        
        # Guardar el pedido
        pedido = form.save(commit=False)
        
        # Calcular total y crear items
        total = 0
        items_data = []
        
        for producto_id, cantidad in carrito.items():
            try:
                producto = Producto.objects.get(id=producto_id)
                subtotal = producto.precio * cantidad
                total += subtotal
                items_data.append({
                    'producto': producto,
                    'cantidad': cantidad,
                    'precio': producto.precio
                })
            except Producto.DoesNotExist:
                continue
        
        pedido.total = total
        pedido.save()
        
        # Crear items del pedido
        for item in items_data:
            ItemPedido.objects.create(
                pedido=pedido,
                producto=item['producto'],
                cantidad=item['cantidad'],
                precio_unitario=item['precio']
            )
        
        # Guardar ID del pedido en sesión
        self.request.session['ultimo_pedido'] = pedido.id
        
        # Limpiar carrito
        self.request.session['carrito'] = {}
        
        return super().form_valid(form)


class PedidoConfirmadoView(TemplateView):
    """Vista de confirmación del pedido"""
    template_name = 'menu/pedido_confirmado.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pedido_id = self.request.session.get('ultimo_pedido')
        
        if pedido_id:
            try:
                pedido = Pedido.objects.get(id=pedido_id)
                context['pedido'] = pedido
                
                # Generar mensaje para WhatsApp
                items = "\n".join([
                    f"• {item.cantidad}x {item.producto.nombre} (${item.precio_unitario})"
                    for item in pedido.items.all()
                ])
                
                mensaje = f"""¡Hola! Quiero confirmar mi pedido #{pedido.id}:

{items}

💰 Total: ${pedido.total}
📦 Entrega: {pedido.get_tipo_entrega_display()}
💳 Pago: {pedido.get_metodo_pago_display()}

👤 Nombre: {pedido.nombre_cliente}
📱 Teléfono: {pedido.telefono}
"""
                
                if pedido.direccion:
                    mensaje += f"📍 Dirección: {pedido.direccion}\n"
                
                if pedido.notas:
                    mensaje += f"\n📝 Notas: {pedido.notas}"
                
                # Codificar para URL
                context['mensaje_whatsapp'] = urllib.parse.quote(mensaje)
                
            except Pedido.DoesNotExist:
                pass
        
        return context


class ActualizarCarritoView(View):
    """API para actualizar el carrito en la sesión"""
    def post(self, request):
        try:
            data = json.loads(request.body)
            carrito = data.get('carrito', {})
            request.session['carrito'] = carrito
            return JsonResponse({'success': True})
        except:
            return JsonResponse({'success': False}, status=400)
