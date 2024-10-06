import datetime
import logging
from app.main import db
from ..model.product import Product
from ..model.supplier import Supplier


def getAllProducts():
    try:
        response = (
            db.session.query(
                Product.id_product,
                Product.name,
                Product.price_unit,
                Product.quantity,
                Supplier.id_supplier,
                Supplier.name,
            )
            .join(Supplier, Supplier.id_supplier == Product.id_supplier, isouter=True)
            .all()
        )
        keys_response = [
            "id_product",
            "name",
            "price_unit",
            "quantity",
            "id_supplier",
            "supplier",
        ]
        return [dict(zip(keys_response, item)) for item in response]
    except Exception as e:
        logging.error(e)
        response = {"message": "Error: " + str(e)}
        return response, 500
    finally:
        db.session.close()


def getOneProduct(id):
    try:
        response = Product.query.filter(Product.id_product == id).first()
        if response:
            # Serializa el objeto Product en un diccionario
            return {
                "id_product": response.id_product,
                "name": response.name,
                "quantity": response.quantity,
                "price_unit": str(
                    response.price_unit
                ),  # Convertir a string si es necesario
                "id_supplier": response.id_supplier,
            }
        else:
            return {
                "message": "Product not found"
            }, 404  # Manejo del caso en que no se encuentra el producto
    except Exception as e:
        logging.error(e)
        response = {"message": "Error: " + str(e)}
        return response, 500
    finally:
        db.session.close()


def saveNewProduct(product):
    try:
        new_product = Product(
            name=product["name"],
            quantity=product["quantity"],
            price_unit=product["price_unit"],
            id_supplier=product["id_supplier"],
        )
        db.session.add(new_product)
        db.session.commit()
        return {"message": "Product created"}, 201
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        response = {"message": "Error: " + str(e)}
        return response, 500


def updateProduct(product, id_product):
    try:
        # Obtener el producto existente de la base de datos
        existing_product = (
            db.session.query(Product).filter(Product.id_product == id_product).first()
        )

        # Si no se encuentra el producto, devolver un mensaje de error
        if not existing_product:
            return {"message": "Product not found"}, 404

        # Actualizar solo los campos proporcionados
        for key, value in product.items():
            if value is not None:  # Solo actualizar si el valor no es None
                setattr(existing_product, key, value)

        db.session.commit()
        return {"message": "Product updated"}, 200
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        response = {"message": "Error: " + str(e)}
        return response, 500


def deleteProduct(id):
    try:
        db.session.query(Product).filter(Product.id_product == id).delete()
        db.session.commit()
        return {"message": "Product deleted"}, 200
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        response = {"message": "Error: " + str(e)}
        return response, 500


def getAllSuppliers():
    try:
        response = db.session.query(
            Supplier.id_supplier,
            Supplier.name,
        ).all()
        keys_response = [
            "id_supplier",
            "name",
        ]
        return [dict(zip(keys_response, item)) for item in response]
    except Exception as e:
        logging.error(e)
        response = {"message": "Error: " + str(e)}
        return response, 500
    finally:
        db.session.close()
