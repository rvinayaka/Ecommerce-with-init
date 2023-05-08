from flask import Flask, jsonify
from settings import connection, logger, handle_exceptions

app = Flask(__name__)

"Functional API"
@app.route("/app/v1/<int:user_id>/orders/", methods = ["GET"], endpoint="get_order_details_of_user")
@handle_exceptions
def get_order_details_of_user(user_id):
    # starting the database connection
    cur, conn = connection()
    # log connection details
    logger(__name__).warning("Starting the db connection to update order table")

    # Check if the parameters given in the url is available or not
    if not user_id:
        error_msg = "User id is not available"
        raise Exception(error_msg)

    cur.execute("""SELECT u.user_name, u.phone, u.email,
                o.order_id, o.order_total,
                u.shipping_address, u.billing_address, o.time_stamp 
                FROM order_table o JOIN users u 
                ON order_table.user_id = users.user_id
                WHERE user_id = %s""", (user_id, ))
    get_order = cur.fetchone()[0]
    user_name, phone, email, order_id, order_total, shipping_addr, billing_addr, time = get_order
    data = {
        "id": order_id,
        "user_name": user_name,
        "mobile": phone,
        "email": email,
        "total amt": order_total,
        "shipping_addr": shipping_addr,
        "billing_addr": billing_addr,
        "updated at": time
    }
    logger(__name__).warning(f"Order details of user id. {user_id} displayed, hence closing the connection")
    return jsonify({"message": f"Order details of user id. {user_id} displayed",
                    "details": data})

