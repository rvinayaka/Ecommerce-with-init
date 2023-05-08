import datetime
from flask import Flask, request, jsonify
from settings import connection, logger, handle_exceptions

app = Flask(__name__)

"""Admin API"""     # updating values to order table
@app.route("/app/v1/<int:user_id>/orders/<int:order_id> ", methods = ["PUT"], endpoint="updating_details_in_order_table")
@handle_exceptions
def updating_details_in_order_table(user_id, order_id):
    # starting the database connection
    cur, conn = connection()
    # log connection details
    logger(__name__).warning("Starting the db connection to update order table")

    # Check if the parameters given in the url is available or not
    if not (user_id and order_id):
        error_msg = "User id and order id is not available"
        raise Exception(error_msg)

    # Check whether the user exists in the table or not
    cur.execute("SELECT * FROM order_table WHERE user_id = %s AND order_id = %s", (user_id, order_id))
    get_user = cur.fetchone()[0]

    if not get_user:
        logger(__name__).warning(f"User with id. {user_id} not found")
        return jsonify({"message": f"User with id. {user_id} not found"})

    data = request.get_json()

    # Execute the query to fetch total amount of the cart of given user
    cur.execute("SELECT SUM(subtotal) FROM order_items WHERE user_id = %s", (user_id, ))
    order_total = cur.fetchone()[0][0]

    # Get shipping & billing address from the user table
    cur.execute("SELECT shipping_address, billing_address FROM users WHERE user_id = %s", (user_id, ))
    get_address = cur.fetchone()[0]

    shipping_address = get_address[0]
    billing_address = get_address[1]
    time = datetime.datetime.now()

    get_data = {
        "order_total": order_total,
        "shipping_address": shipping_address,
        "billing_address": billing_address,
        "updated at": time
    }

    query = "UPDATE order_table SET (order_total = %s, shipping_address = %s, billing_address = %s) WHERE user_id = %s AND order_id = %s"
    values = (order_total, shipping_address, billing_address, user_id, order_id)

    logger(__name__).warning(f"Details of user id. {user_id} updated, hence closing the connection")
    return jsonify({"message": f"Details of user id. {user_id} updated",
                    "details": get_data})

