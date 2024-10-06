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

    @api.doc("inventory get one product")
    def get(self):
        return {"message": "Not Implemented"}, 501

    def post(self):
        return saveNewProduct(request.json)


@api.route("/<int:id>")
class Product(Resource):
    @api.doc("inventory get one product")
    def get(self, id):
        product = getOneProduct(id)
        if product:
            return product, 200
        else:
            return {"message": "Product not found"}, 404

    @api.doc("inventory update product")
    def put(self, id):
        # Obtener los datos del producto del request
        product_data = request.json

        # Llamar al servicio de actualización pasando los datos y el ID
        return updateProduct(product_data, id)

    @api.doc("Delete a product")
    def delete(self, id):
        result = deleteProduct(id)
        if result[1] == 200:
            return result
        else:
            return {"message": "Error deleting product"}, result[1]


@api.route("/get-all")
class Products(Resource):

    @api.doc("logout a user")
    @api.marshal_with(product_supplier)
    def get(self):
        return getAllProducts()


@api.route("/get-all-suppliers")
class Supplier(Resource):

    @api.doc("logout a user")
    @api.marshal_with(supplier)
    def get(self):
        return getAllSuppliers()
