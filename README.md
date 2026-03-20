# 🛒 Supermercados Dana

Aplicación web de supermercado desarrollada con **Django** y templates HTML/CSS artesanal. Permite a los usuarios explorar un catálogo de productos, gestionar un carrito de compras y simular una compra con datos bancarios.

---

## Autor

**Esteban Rodolfo Scaramuzza**
Proyecto — Marzo 2026


## 📋 Tabla de contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Tecnologías](#tecnologías)
- [Instalación](#instalación)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Apps de Django](#apps-de-django)
- [Modelos](#modelos)
- [Categorías de productos](#categorías-de-productos)
- [Capturas de pantalla](#capturas-de-pantalla)
- [Seguridad](#seguridad)
- [Autor](#autor)

---

## Descripción

Supermercados Dana es un proyecto académico que implementa un supermercado local con las funcionalidades esenciales de una tienda online: catálogo de productos por categoría, buscador global, carrito de compras, sistema de usuarios con perfiles personalizados y un checkout simulado.

---

## Características

- **Catálogo de productos** con grid responsivo y filtrado por categoría
- **Buscador global** de productos desde el navbar
- **Sistema de usuarios** con registro, login y perfil personalizable
- **Avatar de usuario** con validación de formato y tamaño
- **Cliente Premium** con descuento del 30% en todos los productos
- **Carrito de compras** con control de cantidad y eliminación de items
- **Checkout simulado** con validación de datos bancarios
- **Historial de compras** visible desde el perfil
- **Soporte** — formulario para solicitar eliminación de cuenta
- **Panel de administración** con acciones personalizadas
- **Logo SVG** generado programáticamente con C++

---

## Tecnologías

| Tecnología | Uso |
|---|---|
| Python 3.12 | Lenguaje principal |
| Django 5 | Framework web |
| SQLite | Base de datos en desarrollo |
| Pillow | Procesamiento de imágenes |
| HTML5 / CSS3 | Frontend artesanal sin frameworks |
| Visual C++ | Generación del logo SVG |

---

## Instalación

### Requisitos previos

- Python 3.10 o superior
- pip

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/ERScara/supermercados-dana.git
cd supermercados-dana

# 2. Crear y activar el entorno virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
# Crear archivo .env en la raíz con:
# SECRET_KEY=tu-clave-secreta
# DEBUG=True

# 5. Aplicar migraciones
python manage.py migrate

# 6. Crear superusuario
python manage.py createsuperuser

# 7. Ejecutar el servidor
python manage.py runserver
```

Accedé a `http://127.0.0.1:8000` en el navegador.

---

## Estructura del proyecto

```
supermercados_dana/
│
├── dana/                       ← configuración principal
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── productos/                  ← catálogo y categorías
├── clientes/                   ← usuarios y perfiles
├── carrito/                    ← carrito de compras
├── compras/                    ← checkout y historial
│
├── templates/                  ← templates HTML
│   ├── base.html
│   ├── navbar.html
│   ├── inicio.html
│   ├── productos/
│   ├── clientes/
│   ├── carrito/
│   └── compras/
│
├── static/                     ← archivos estáticos
│   ├── img/
│   │   ├── logo.svg
│   │   └── avatar_default.svg
│   ├── css/
│   └── js/
│
├── media/                      ← archivos subidos por usuarios
│   ├── productos/
│   └── avatares/
│
├── .env                        ← variables sensibles (no en repo)
├── .gitignore
└── requirements.txt
```

---

## Apps de Django

### `productos`
Gestiona el catálogo de productos y sus categorías. Incluye vistas para listar, filtrar por categoría, ver detalle y buscar productos globalmente.

### `clientes`
Extiende el sistema de usuarios de Django con perfil personalizable, avatar, estado Premium, preferencias de categorías y tickets de soporte.

### `carrito`
Maneja el carrito de compras por usuario. Permite agregar productos, modificar cantidades y eliminar items. Aplica descuentos Premium automáticamente.

### `compras`
Gestiona el proceso de checkout con validación de datos bancarios simulados. Genera un historial de compras por cliente y actualiza el stock de productos.

---

## Modelos

```
User (Django)
└── Cliente
    ├── edad
    ├── es_cliente_premium
    ├── saldo_a_favor
    ├── avatar
    └── preferencias (M2M → Categoria)

Categoria
└── Producto
    ├── nombre
    ├── descripcion
    ├── precio
    ├── stock
    └── imagen

Carrito
└── ItemCarrito
    ├── producto (FK)
    ├── cantidad
    └── precio_unitario

Compra
└── ItemCompra
    ├── producto (FK)
    ├── cantidad
    └── precio_unitario

SupportTicket
    ├── username
    ├── email
    ├── reason
    └── resolved
```

---

## Categorías de productos

| # | Categoría | Descripción |
|---|---|---|
| 1 | 🥦 Frutas y Verduras | Productos frescos de la huerta |
| 2 | 🥛 Lácteos y Huevos | Leche, yogur, queso y huevos frescos |
| 3 | 🥩 Carnes y Pescados | Carnes vacunas, pollo, pescados y fiambres |
| 4 | 🥫 Almacén | Arroz, fideos, conservas, aceite y harinas |
| 5 | 🧴 Limpieza y Hogar | Productos de limpieza y cuidado personal |
| 6 | 🥤 Bebidas | Agua, jugos, gaseosas y bebidas alcohólicas |

---

## Seguridad

- `SECRET_KEY` almacenada en `.env` — nunca en el código fuente
- Protección **CSRF** en todos los formularios POST
- Validación de archivos subidos (formato y tamaño) en el servidor
- Contraseñas hasheadas por Django
- `@login_required` en todas las vistas protegidas
- Datos bancarios **nunca almacenados** — solo los últimos 4 dígitos
- Defensa en profundidad en la lógica de descuentos Premium
- Mismo mensaje de respuesta en reset de contraseña para evitar **user enumeration**

---


