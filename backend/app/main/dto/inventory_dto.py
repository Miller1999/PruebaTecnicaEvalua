from flask_restx import Namespace, fields


class InventoryDto:
    api = Namespace(
        "inventory", description="Operaciones relacionadas con el inventario"
    )

    product_with_supplier = api.model(
        "product_supplier",
        {
            "id_product": fields.Integer(required=True, description="ID del producto"),
            "name": fields.String(required=True, description="Nombre del producto"),
            "quantity": fields.Integer(required=True, description="Cantidad en stock"),
            "price_unit": fields.Float(
                required=True, description="Precio unitario del producto"
            ),
            "id_supplier": fields.Integer(
                required=True, description="ID del proveedor"
            ),
            "supplier": fields.String(
                required=True, description="Nombre del proveedor"
            ),
        },
    )

    product = api.model(
        "product",
        {
            "id_product": fields.Integer(required=True, description="ID del producto"),
            "name": fields.String(required=True, description="Nombre del producto"),
            "quantity": fields.Integer(required=True, description="Cantidad en stock"),
            "price_unit": fields.Float(
                required=True, description="Precio unitario del producto"
            ),
        },
    )

    supplier = api.model(
        "supplier",
        {
            "id_supplier": fields.Integer(
                required=True, description="ID del proveedor"
            ),
            "name": fields.String(required=True, description="Nombre del proveedor"),
        },
    )
