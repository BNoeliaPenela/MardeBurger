from django.db import models

class Categoria(models.Model):
    """Categorías de productos (Hamburguesas, Bebidas, Acompañamientos, etc.)"""
    nombre = models.CharField(max_length=100)
    orden = models.IntegerField(
        default=0,
        help_text="Orden de visualización (menor número aparece primero)"
    )
    
    class Meta:
        verbose_name_plural = "Categorías"
        ordering = ['orden', 'nombre']
    
    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """Productos del menú"""
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(
        help_text="Descripción completa del producto"
    )
    precio = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Precio en pesos argentinos"
    )
    imagen = models.ImageField(
        upload_to='productos/',
        help_text="Imagen del producto (recomendado: 800x600px)"
    )
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.CASCADE, 
        related_name='productos'
    )
    disponible = models.BooleanField(
        default=True,
        help_text="¿Está disponible para la venta?"
    )
    destacado = models.BooleanField(
        default=False,
        help_text="¿Mostrar en la página principal?"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['categoria', 'nombre']
        verbose_name_plural = "Productos"
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio}"


class Pedido(models.Model):
    """Pedidos realizados por los clientes"""
    
    METODO_PAGO = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia Bancaria'),
        ('mercadopago', 'Mercado Pago'),
    ]
    
    TIPO_ENTREGA = [
        ('retiro', 'Retiro en local'),
        ('delivery', 'Delivery'),
    ]
    
    # Información del cliente
    nombre_cliente = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    direccion = models.TextField(
        blank=True,
        help_text="Solo necesario para delivery"
    )
    
    # Detalles del pedido
    tipo_entrega = models.CharField(
        max_length=20, 
        choices=TIPO_ENTREGA,
        default='retiro'
    )
    metodo_pago = models.CharField(
        max_length=20, 
        choices=METODO_PAGO,
        default='efectivo'
    )
    total = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Total del pedido"
    )
    notas = models.TextField(
        blank=True,
        help_text="Aclaraciones o instrucciones especiales"
    )
    
    # Metadata
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha']
        verbose_name_plural = "Pedidos"
    
    def __str__(self):
        return f"Pedido #{self.id} - {self.nombre_cliente} (${self.total})"
    
    def cantidad_items(self):
        """Retorna la cantidad total de items en el pedido"""
        return sum(item.cantidad for item in self.items.all())


class ItemPedido(models.Model):
    """Items individuales dentro de un pedido"""
    pedido = models.ForeignKey(
        Pedido, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    producto = models.ForeignKey(
        Producto, 
        on_delete=models.CASCADE
    )
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Precio al momento de la compra"
    )
    
    class Meta:
        verbose_name_plural = "Items de Pedido"
    
    def subtotal(self):
        """Calcula el subtotal del item"""
        return self.cantidad * self.precio_unitario
    
    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} (Pedido #{self.pedido.id})"
