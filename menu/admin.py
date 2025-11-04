from django.contrib import admin
from .models import Categoria, Producto, Pedido, ItemPedido

@admin.register(Categoria)  
class CategoriaAdmin(admin.ModelAdmin):
    """Admin para Categorías"""
    list_display = ['nombre', 'orden', 'cantidad_productos']
    list_editable = ['orden']
    search_fields = ['nombre']
    ordering = ['orden', 'nombre']
    
    def cantidad_productos(self, obj):
        """Muestra la cantidad de productos en esta categoría"""
        return obj.productos.count()
    cantidad_productos.short_description = 'Productos'

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    """Admin para Productos"""
    list_display = [
        'nombre', 
        'categoria', 
        'precio', 
        'disponible', 
        'destacado',
        'fecha_creacion'
    ]
    list_filter = ['categoria', 'disponible', 'destacado', 'fecha_creacion']
    list_editable = ['precio', 'disponible', 'destacado']
    search_fields = ['nombre', 'descripcion']
    ordering = ['categoria', 'nombre']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'categoria', 'descripcion')
        }),
        ('Precio e imagen', {
            'fields': ('precio', 'imagen')
        }),
        ('Estado', {
            'fields': ('disponible', 'destacado')
        }),
    )
    
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']

class ItemPedidoInline(admin.TabularInline):
    """Inline para mostrar items dentro del pedido"""
    model = ItemPedido
    extra = 0
    readonly_fields = ['subtotal']
    fields = ['producto', 'cantidad', 'precio_unitario', 'subtotal']
    
    def subtotal(self, obj):
        return f"${obj.subtotal()}"
    subtotal.short_description = 'Subtotal'

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    """Admin para Pedidos"""
    list_display = [
        'id',
        'nombre_cliente',
        'telefono',
        'tipo_entrega',
        'metodo_pago',
        'total',
        'cantidad_items',
        'fecha'
    ]
    list_filter = [
        'tipo_entrega', 
        'metodo_pago', 
        'fecha'
    ]
    search_fields = [
        'nombre_cliente', 
        'telefono', 
        'id'
    ]
    readonly_fields = ['fecha', 'total']
    ordering = ['-fecha']
    date_hierarchy = 'fecha'
    
    inlines = [ItemPedidoInline]
    
    fieldsets = (
        ('Información del cliente', {
            'fields': ('nombre_cliente', 'telefono', 'direccion')
        }),
        ('Detalles del pedido', {
            'fields': ('tipo_entrega', 'metodo_pago', 'total', 'notas')
        }),
        ('Metadata', {
            'fields': ('fecha',),
            'classes': ('collapse',)
        }),
    )
    
    def cantidad_items(self, obj):
        """Cantidad total de items en el pedido"""
        return obj.cantidad_items()
    cantidad_items.short_description = 'Items'
    
@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    """Admin para Items de Pedido (vista separada)"""
    list_display = [
        'pedido',
        'producto',
        'cantidad',
        'precio_unitario',
        'subtotal'
    ]
    list_filter = ['pedido__fecha', 'producto']
    search_fields = [
        'pedido__id',
        'pedido__nombre_cliente',
        'producto__nombre'
    ]
    readonly_fields = ['subtotal']