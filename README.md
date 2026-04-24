# 🛒 Supermercados Dana

Aplicación web de supermercado desarrollada con **Django** y templates HTML/CSS. Permite a los usuarios explorar un catálogo de productos, gestionar un carrito de compras y simular una compra con datos bancarios.

---

## Autor

**Esteban Rodolfo Scaramuzza**
Proyecto — Marzo 2026

## 📋 Tabla de contenidos

- [🛒 Supermercados Dana](#-supermercados-dana)
  - [Autor](#autor)
  - [📋 Tabla de contenidos](#-tabla-de-contenidos)
  - [Descripción](#descripción)
  - [Características](#características)
  - [Tecnologías](#tecnologías)
  - [Instalación](#instalación)
    - [Requisitos previos](#requisitos-previos)
    - [Pasos](#pasos)
  - [Apps de Django](#apps-de-django)
    - [`productos`](#productos)
    - [`clientes`](#clientes)
    - [`carrito`](#carrito)
    - [`compras`](#compras)
    - [`atencion_cliente`](#atencion_cliente)
    - [`acerca_de`](#acerca_de)
  - [Modelos](#modelos)
  - [Categorías de productos](#categorías-de-productos)
  - [Seguridad](#seguridad)
  - [Video](#video)

---

## Descripción

Supermercados Dana es un proyecto que implementa un supermercado local con las funcionalidades esenciales de una tienda online: catálogo de productos por categoría, buscador global, carrito de compras, sistema de usuarios con perfiles personalizados y un checkout simulado.

---

## Características

- **Catálogo de productos** con grid responsivo y filtrado por categoría.
- **Buscador global** de productos desde el navbar.
- **Sistema de usuarios** con registro, login y perfil personalizable.
- **Avatar de usuario** con validación de formato y tamaño.
- **Cliente Premium** con descuento del 30% en todos los productos.
- **Carrito de compras** con control de cantidad y eliminación de items.
- **Checkout simulado** con validación de datos bancarios.
- **Historial de compras** visible desde el perfil.
- **Soporte** — formulario para solicitar eliminación de cuenta.
- **Panel de administración** con acciones personalizadas.
- **Logo SVG** generado con Visual C++.

---

## Tecnologías

| Tecnología | Uso |
|---|---|
| Python 3.13.7 | Lenguaje principal |
| Django 6 | Framework web |
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
Crear archivo .env en la raíz con:
- SECRET_KEY=tu-clave-secreta
- DEBUG=True

# 5. Aplicar migraciones
python manage.py migrate

# 6. Crear superusuario
python manage.py createsuperuser

# 7. Ejecutar el servidor
python manage.py runserver
```

Accedé a `http://127.0.0.1:8000` en el navegador.

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

### `atencion_cliente`

Ofrece un espacio para que los clientes puedan expresar sus inquietudes, tiene un sitio de preguntas frecuentes y una sección de comentarios.

### `acerca_de`

Sección especial acerca del creador del sitio. Aquí se encuentra una imagen del autor, una breve biografía del mismo y una descripción del proyecto.

---

## Modelos

```
User (Django)
├── Cliente
│   ├── usuario (O2O -> User)
│   ├── edad
│   ├── es_cliente_premium
│   ├── saldo_a_favor
│   ├── preferencias (M2M → Categoria)    
│   └── avatar
└── SupportTicket
    ├── username 
    ├── email
    ├── reason
    ├── created_at
    └── resolved
 
Categoria
├── Categoria
│   ├── nombre
│   └── descripcion
└── Producto
    ├── nombre
    ├── descripcion
    ├── precio
    ├── stock
    ├── categoria (FK)
    └── imagen

Atencion_cliente
├── PreguntasFrecuentes
│   ├── titulo
│   ├── respuesta
│   └── orden
├── Comentario
│   ├── user (FK)
│   ├── parent (FK)
│   ├── puntuacion
│   ├── titulo
│   ├── mensaje
│   ├── fecha
│   ├── is_deleted
│   └── reportes (M2M -> User)
└── VotoComentario
    ├── comentario (FK)
    ├── cliente (FK)
    └── voto

Carrito
├── Carrito
│   ├── cliente
│   ├── creado_en
│   └── actualizado_en
│
└── ItemCarrito
    ├── carrito (FK)
    ├── producto (FK)
    ├── cantidad
    ├── precio_unitario
    └── precio_original
    

Compra
├── Compra   
│   ├── cliente (FK)
│   ├── fecha
│   ├── estado
│   └── ultimos_4_digitos
│
└── ItemCompra
    ├── compra (FK)
    ├── producto (FK)
    ├── cantidad
    ├── precio_unitario
    └── precio_original

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

- `SECRET_KEY` almacenada en `.env` — nunca en el código fuente.
- Protección **CSRF** en todos los formularios POST.
- Validación de archivos subidos (formato y tamaño) en el servidor.
- `@login_required` en todas las vistas protegidas.
- Datos bancarios **nunca almacenados** — solo los últimos 4 dígitos.
- Defensa en profundidad en la lógica de descuentos Premium.
- Mismo mensaje de respuesta en reset de contraseña para evitar **user enumeration**.

---

## Video e Instructivo

Aquí se proporciona un video de presentación y un instructivo del proyecto.

Video: https://mega.nz/file/ViYATYjC#jujNY4tcO5r9PyP12hvzNCJKPhycPXqq5zvoiSQ4vXY
Instructivo: https://mega.nz/file/IzwChDoA#lRrz2y-dKkrwk05-Ic3rEnC_ohkJqyeEFwGI4vk4Ex4

---
