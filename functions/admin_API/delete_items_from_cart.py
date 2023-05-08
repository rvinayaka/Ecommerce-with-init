from flask import Flask, jsonify
from settings import connection, logger, handle_exceptions

app = Flask(__name__)
"""Admin API"""
@app.route("/app/v1/<int:user_id>/items/<int:product_id>", methods = ["DELETE"], endpoint="deleting_products_from_cart_of_user")
@handle_exceptions
def deleting_products_from_cart_of_user(user_id, product_id):
    # starting the database connection
    cur, conn = connection()
    # log connection details
    logger(__name__).warning("Start the db connection to deleting items of user in wishlist table")

    # Check if the parameters given in the url is available or not
    if not (user_id and product_id):
        error_msg = "User id and product id is not available"
        raise Exception(error_msg)

    cur.execute("SELECT * FROM order_items WHERE user_id = %s AND product_id = %s", (user_id, product_id ))
    get_user = cur.fetchone()[0]

    if not get_user:
        logger(__name__).warning(f"User with id.{user_id} not found or the product with id. {product_id} is missing")
        return jsonify({"message": f"User with id.{user_id} not found or the product with id. {product_id} is missing"})

    cur.execute("DELETE FROM order_items WHERE user_id = %s AND product_id = %s")
    logger(__name__).warning(f"Products from the cart has been deleted of user id. {user_id}")
    return jsonify({"message": f"Products from the cart has been deleted of user id. {user_id}"})

