import datetime
from flask import request, jsonify
from settings import connection, logger, handle_exceptions
from functions import app

"""Admin API"""     # updating values to order_items table
@app.route("/app/v1/<int:user_id>/orders/update_items", methods = ["PUT"], endpoint="updating_details_in_order_items_table")
@handle_exceptions
def updating_details_in_order_items_table(user_id):
    # starting the database connection
    cur, conn = connection()
    # log connection details
    logger(__name__).warning("Starting the db connection to updating items in cart(order_items) table")

    # Check if the parameters given in the url is available or not
    if not user_id:
        error_msg = "User id is not available"
        raise Exception(error_msg)

    # Check whether the user exists in the table or not
    cur.execute("SELECT * FROM order_items WHERE user_id = %s", (user_id, ))
    get_user = cur.fetchone()[0]
    time = datetime.datetime.now()
    data = request.get_json()

    # if exists check whether product id is given or not
    if get_user:
        # Check which product user wants to update accordingly update that product details
        product_id = data.get('productId')

        if product_id:
            cur.execute("UPDATE order_items SET product_id = %s, time_stamp = %s AND user_id = %s", (product_id, time))

            # Execute the query to fetch the price from the product table
            cur.execute("SELECT price FROM products WHERE product_id = %s", (product_id,))
            price = cur.fetchone()[0][0]
            quantity = data.get('quantity')

            if price:
                cur.execute("UPDATE order_items SET price = %s, time_stamp = %s WHERE product_id = %s AND user_id = %s", (price, product_id, user_id, time))
            if quantity:
                cur.execute("UPDATE order_items SET quantity, time_stamp = %s = %s WHERE product_id = %s AND user_id = %s", (quantity, product_id, user_id, time))

            if price and quantity:
                subtotal = price * quantity
                cur.execute("UPDATE order_items SET subtotal, time_stamp = %s = %s WHERE product_id = %s AND user_id = %s", (subtotal, product_id, user_id, time))

            else:
                return jsonify({"error": "Please provided valid quantity to update subtotal"})
        else:
            return jsonify({"error": "Product doesn't exists please provided valid product id"})

        logger(__name__).warning(f"Details of user with id. {user_id} has been updated in the order_items table, hence closing connection")
        return jsonify({f"Details of user with id. {user_id} has been updated in the order_items table"})

    else:
        logger(__name__).warning(f"User with id. {user_id} not found")
        return jsonify({"message": f"User with id. {user_id} not found"})
