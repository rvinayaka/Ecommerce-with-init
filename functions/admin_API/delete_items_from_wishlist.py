from flask import jsonify
from settings import connection, logger, handle_exceptions
from functions import app

"""Admin API"""
@app.route("/app/v1/wishlist/<int:user_id>/remove/<int:product_id>", methods = ["DELETE"], endpoint="delete_items_of_user_in_wishlist")
@handle_exceptions
def delete_items_of_user_in_wishlist(user_id, product_id):
    # starting the database connection
    cur, conn = connection()
    # log connection details
    logger(__name__).warning("Start the db connection to deleting items of user in wishlist table")

    # Check if the parameters given in the url is available or not
    if not (user_id and product_id):
        error_msg = "User id and product id is not available"
        raise Exception(error_msg)


    cur.execute("SELECT * FROM wishlist WHERE user_id = %s AND product_id = %s", (user_id, product_id ))
    get_user = cur.fetchone()[0]

    if not get_user:
        logger(__name__).warning(f"User with id.{user_id} not found or the product with id. {product_id} is missing")
        return jsonify({"message": f"User with id.{user_id} not found or the product with id. {product_id} is missing"})

    cur.execute("DELETE FROM wishlist WHERE user_id = %s AND product_id = %s")
    logger(__name__).warning(f"Wishlist items of user with id. {user_id} has been deleted")
    return jsonify({"message": f"Wishlist items of user with id. {user_id} has been deleted",
                    "details": get_user})

