# Mar de Burger

## 1. Descripción general  
Mar de Burger es un sistema web desarrollado para la gestión de pedidos en línea de mi emprendimiento. Permite a los clientes ver el menú del día, armar un carrito de compras y completar un checkout. Desde el lado administrativo se podrá gestionar el catálogo de comidas, el estado de los pedidos y los datos de los clientes.

Este repositorio contiene la versión **backend + frontend integrado** desarrollada con **Django** para el backend, y uso de plantillas HTML + JavaScript para el frontend.

---

## 2. Tecnologías empleadas  
- Python 3.x  
- Django (versión usada en el proyecto)  
- HTML5 / CSS3 / Bootstrap 5 (para los estilos y componentes frontend)  
- JavaScript (vanilla) para interactividad del carrito  
- SQLite como base de datos (versión de desarrollo)  
- Git para control de versiones  
- GitHub para alojamiento del repositorio

---

## 3. Estructura del proyecto  
Mar­de­Burger/
│ manage.py
│ requirements.txt
│ db.sqlite3
│
├── config/ ← configuración de Django (settings, urls, wsgi, etc)
├── menu/ ← app principal: modelos de productos, vistas de cliente, carrito
├── panel/ ← app administrativa (gestión interna, empleados, etc)
├── media/ ← archivos de medios (imágenes de productos, uploads)
└── templates/ ← plantillas HTML para vistas


## 4. Funcionalidades implementadas  
### 4.1 Para el cliente  
- Visualización del menú de productos (hamburguesas, complementos, etc)  
- Detalle de producto (`<int:pk>`) para ver más información  
- Gestión del carrito de compras: añadir, quitar productos, ver total, subtotales  
- Formulario de checkout para completar datos del cliente (nombre, teléfono, tipo de entrega, dirección, notas)  
- Envío del pedido mediante formulario y redirección a página de confirmación  

### 4.2 Para la administración  
- Sección de panel (desde la app `panel`) para que empleados/gerentes puedan ver reservas/pedidos generados
- End-point API para actualizar el carrito (`/api/actualizar-carrito/`) que guarda el estado del carrito en sesión  

---

## 5. Instalación y ejecución en local  
1. Cloná el repositorio:  
   ```bash
   git clone https://github.com/BNoeliaPenela/MardeBurger.git
   cd MardeBurger
Crear y activar un entorno virtual:

python3 -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate

Instalar dependencias:
pip install -r requirements.txt

Aplicar migraciones de Django:
python manage.py migrate

Crear superusuario para administración:
python manage.py createsuperuser

Ejecutar el servidor de desarrollo:
python manage.py runserver

Acceder al navegador:
Cliente: http://127.0.0.1:8000/menu/
Administración: http://127.0.0.1:8000/panel/

## 6. Autoría
Desarrolladora: Noelia Penela – Estudiante de Desarrollo de Software
Proyecto realizado como parte de práctica profesional / proyecto final de carrera
