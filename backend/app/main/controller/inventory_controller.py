from flask import request
from flask_restx import Resource

from app.main.service.inventory_service import (
    getAllProducts,
    getOneProduct,
    saveNewProduct,
    updateProduct,
    deleteProduct,
    getAllSuppliers,
)
from ..dto.inventory_dto import InventoryDto

api = InventoryDto.api
product_dto = InventoryDto.product
product_supplier = InventoryDto.product_with_supplier
supplier = InventoryDto.supplier


@api.route("/")
class Product(Resource):
    @api.doc("Crear un nuevo producto")
    @api.expect(product_dto)  # Agrega el modelo DTO para la validación
    @api.response(201, "Producto creado")
    @api.response(400, "Error en los datos de entrada")
    def post(self):
        """Crear un nuevo producto en el inventario"""
        return saveNewProduct(request.json)


@api.route("/<int:id>")
class ProductById(Resource):
    @api.doc("Obtener un producto por ID")
    @api.response(200, "Producto encontrado")
    @api.response(404, "Producto no encontrado")
    def get(self, id):
        """Obtener un producto específico por ID"""
        return getOneProduct(id)

    @api.doc("Actualizar un producto por ID")
    @api.expect(product_dto)  # Agrega el modelo DTO para la validación
    @api.response(200, "Producto actualizado")
    @api.response(404, "Producto no encontrado")
    @api.response(400, "Error en los datos de entrada")
    def put(self, id):
        """Actualizar un producto existente"""
        product_data = request.json
        return updateProduct(product_data, id)

    @api.doc("Eliminar un producto por ID")
    @api.response(200, "Producto eliminado")
    @api.response(404, "Producto no encontrado")
    def delete(self, id):
        """Eliminar un producto específico por ID"""
        result = deleteProduct(id)
        return result


@api.route("/get-all")
class Products(Resource):
    @api.doc("Obtener todos los productos")
    @api.marshal_with(product_supplier)
    @api.response(200, "Lista de productos")
    def get(self):
        """Obtener todos los productos en el inventario"""
        return getAllProducts()


@api.route("/get-all-suppliers")
class Supplier(Resource):
    @api.doc("Obtener todos los proveedores")
    @api.marshal_with(supplier)
    @api.response(200, "Lista de proveedores")
    def get(self):
        """Obtener todos los proveedores disponibles"""
        return getAllSuppliers()
