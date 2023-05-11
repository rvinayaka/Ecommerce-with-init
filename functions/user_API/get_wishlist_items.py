from flask import jsonify
from settings import connection, logger, handle_exceptions
from functions import app

"""Functional API"""
@app.route("/app/v1/wishlist/<int:user_id>", methods = ["GET"], endpoint="get_items_of_user_in_wishlist")
@handle_exceptions
def get_items_of_user_in_wishlist(user_id):
    # starting the database connection
    cur, conn = connection()
    # log connection details
    logger(__name__).warning("Start the db connection to get items of user from wishlist table")

    # Check if the parameters given in the url is available or not
    if not user_id:
        error_msg = "User id is not available"
        raise Exception(error_msg)


    cur.execute("SELECT w.product_id, p.product_name, p.price, p.description "
                "FROM wishlist w JOIN products p ON w.product_id = p.product_id "
                "WHERE user_id = %s", (user_id, ))
    get_user = cur.fetchone()[0]

    product_id, name, price, desc = get_user

    data = {
        "product_id": product_id,
        "product_name": name,
        "price": price,
        "desc": desc
    }

    if not get_user:
        logger(__name__).warning(f"User with id.{user_id} not found")
        return jsonify({"message": f"User with id.{user_id} not found"})

    logger(__name__).warning(f"Wishlist items of user with id. {user_id} has been displayed")
    return jsonify({"message": f"Wishlist items of user with id. {user_id} has been displayed",
                    "details": data})
