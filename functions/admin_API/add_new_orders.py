from settings import connection, logger, handle_exceptions
from functions import app
import datetime

"""Admin API"""     # add new values to order_table
@app.route("/app/v1/<int:user_id>/orders/add_order", methods = ["POST"], endpoint="add_new_order_to_order_table")
@handle_exceptions
def add_new_order_to_order_table(user_id):
    # starting the database connection
    cur, conn = connection()
    # log connection details
    logger(__name__).warning("Start the db connection to add new orders to order table")

    # Check if the parameters given in the url is available or not
    if not user_id:
        error_msg = "User id not given"
        raise Exception(error_msg)

    # Get shipping & billing address from the user table
    cur.execute("SELECT shipping_address, billing_address FROM user WHERE user_id = %s", (user_id, ))
    get_address = cur.fetchone()[0]

    shipping_address = get_address[0]
    billing_address = get_address[1]
    time = datetime.datetime.now()

    # Execute the query to fetch total amount of the cart of given user
    cur.execute("SELECT SUM(subtotal) FROM order_items WHERE user_id = %s", (user_id, ))
    order_total = cur.fetchone()[0][0]

    # {
    #     "order_total": order_total,
    #     "shipping_address": shipping_address,
    #     "billing_address": billing_address,
    #     "time": time,
    # }

    query = """INSERT INTO order_table (user_id, order_total, shipping_address, billing_address, time_stamp) VALUES(%s, %s, %s, %s, %s)"""
    values = (user_id, order_total, shipping_address, billing_address, time)

    # Execute the query using values
    cur.execute(query, values)

    # Commit the changes to the table
    conn.commit()
    logger(__name__).warning("New orders has been added, hence closing the connection")
    return jsonify({"message": "New orders has been added",
                    "details": order_total})
