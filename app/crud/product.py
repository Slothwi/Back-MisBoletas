from app.schemas.product import Product
from fastapi import HTTPException
from datetime import date

# Lista temporal de productos para almacenamiento en memoria
products_list = [
    Product(ProductoID=1, NombreProducto="Laptop", FechaCompra=date(2022, 5, 20), DuracionGarantia=24, Marca="Dell", Modelo="XPS 13", Tienda="Best Buy", Notas="Buen estado", UsuarioID=1),
    Product(ProductoID=2, NombreProducto="Smartphone", FechaCompra=date(2023, 1, 15), DuracionGarantia=12, Marca="Apple", Modelo="iPhone 13", Tienda="Apple Store", Notas="Con funda", UsuarioID=2)
]

# Función para buscar un producto por ID
# CORREGIDO: Cambió de p.id a p.ProductoID para usar el campo correcto del modelo
def search_product(product_id: int):
    for p in products_list:
        if p.ProductoID == product_id:
            return p
    return None

# Función para crear un nuevo producto
# CORREGIDO: Cambió de product.id a product.ProductoID
def create_product(product: Product):
    if search_product(product.ProductoID):
        raise HTTPException(status_code=400, detail="Producto ya existe")
    products_list.append(product)
    return product

# Función para actualizar un producto existente
# CORREGIDO: Cambió de p.id a p.ProductoID
def update_product(product: Product):
    for index, p in enumerate(products_list):
        if p.ProductoID == product.ProductoID:
            products_list[index] = product
            return product
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# Función para eliminar un producto por ID
# CORREGIDO: Cambió de p.id a p.ProductoID
def delete_product(product_id: int):
    for index, p in enumerate(products_list):
        if p.ProductoID == product_id:
            del products_list[index]
            return {"message": "Producto eliminado"}
    raise HTTPException(status_code=404, detail="Producto no encontrado")