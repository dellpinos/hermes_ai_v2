# TusListasWeb - Overview

TusListasWeb es una plataforma para gestionar inventario, productos y precios en un comercio o empresa. También permite administrar un grupo de trabajo y acceder a estadísticas sobre la actividad, las finanzas e incluso un modo "Cajero" para agilizar las ventas.

## Funcionalidades principales

- **Buscador**: listar, filtrar y ordenar productos. Buscar por nombre o código único.
- **Ingreso de Mercadería**: registrar productos recibidos, actualizar precios y fechas, aplicar descuentos temporales, marcar productos como pendientes.
- **Nuevo Producto**: ingresar producto con código único, categorías, proveedores, fabricantes y cotización del dólar.
- **Precio de Venta**: cálculo automático con IVA (21%), ganancia y redondeo a múltiplos de 10.
- **Fraccionado**: crear versiones fraccionadas de un producto con código único y ganancia extra.
- **Aumentos Generales**: aplicar aumentos masivos por categoría, proveedor o fabricante. También por cotización de dólar.
- **Agenda**: administrar categorías, proveedores y fabricantes. Cada uno puede tener índice de ganancia y contacto.
- **Herramientas de Administrador (Owner)**:
  - Invitar usuarios a la empresa.
  - Listar y eliminar usuarios.
  - Cambiar nombre de la empresa.
  - Aplicar Aumentos Generales.
  - Ver estadísticas (en desarrollo).
- **Accesibilidad**: funciona en cualquier navegador, optimizado para escritorio y móvil.

## Conceptos clave

### Buscador

- Lista todos los productos.
- Permite filtrar y ordenar.
- Código único generado automáticamente.

### Ingreso de Mercadería

- Basado en facturas o remitos de proveedores.
- Dos buscadores: por código y por nombre.
- Precio ingresado con o sin IVA.
- Actualiza fecha y mantiene precios vigentes.
- Descuentos temporales: porcentaje + duración en semanas.
- Productos pendientes: guardados temporalmente, luego agregados al catálogo.

### Nuevo Producto

- Código único generado automáticamente.
- Categorías, proveedores y fabricantes asignables.
- Cotización del dólar por producto.
- Ganancia asignada por:
  - Categoría.
  - Proveedor.
  - Personalizada (índice por producto).

### Precio de Venta

- Calculado = costo * IVA * ganancia.
- Redondeo siempre hacia arriba en múltiplos de 10.
- Descuentos también redondeados.

### Fraccionado

- Producto derivado con código propio.
- Comparte datos con el original.
- Precio de costo = costo original / total de unidades.
- Ganancia extra opcional para la fracción.

### Aumentos Generales

- Aplican sobre lotes de productos.
- Por categoría, proveedor o fabricante.
- Por cotización de dólar.
- No se pueden revertir.
- Registro de últimos 50 aumentos.

### Agenda

- **Categoría**: clasifica productos, define ganancia, soporta aumentos masivos.
- **Proveedor**: datos de contacto + índice de ganancia.
- **Fabricante**: datos de contacto + índice de ganancia.

### Herramientas del Administrador

- Crear empresa y ser Owner.
- Invitar y eliminar usuarios.
- Cambiar nombre de la empresa.
- Ver estadísticas (en desarrollo).
- Acceder desde cualquier dispositivo.
