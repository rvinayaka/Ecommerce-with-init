from datetime import datetime
from flask import request, jsonify
from settings import connection, logger, handle_exceptions
from functions import app

"""Admin API"""     # add new values to order_items table
@app.route("/app/v1/<int:user_id>/orders/order_items/add_items ", methods = ["POST"], endpoint="add_new_items_to_order_items_table")
@handle_exceptions
def add_new_items_to_order_items_table(user_id):
    # starting the database connection
    cur, conn = connection()
    # log connection details
    logger(__name__).warning("Start the db connection to add new items to cart(order_items) table")

    if not user_id:
        error_msg = "User id not given"
        raise Exception(error_msg)

    if "user_id" and "product_id" and "quantity" not in request.json:
        raise Exception("Data is insufficient")

    # Define a lambda function to extract values from JSON data
    extract_key = lambda key: request.json.get(key)

    # Insert new values taken from the user using the lambda function
    user_id = extract_key('userId')
    product_id = extract_key('productId')
    quantity = extract_key('quantity')
    time = datetime.now()

    # Execute the query to fetch the price of the product with the given
    cur.execute("SELECT price FROM products WHERE product_id = %s", (product_id, ))
    price = cur.fetchone()[0][0]
    subtotal = price * quantity

    # {
    #     "id": user_id,
    #     "product_id": product_id,
    #     "price": price,
    #     "subtotal": subtotal,
    #     "quantity": quantity,
    #     "time_stamp": time,
    # }

    query = """INSERT INTO order_items (user_id, product_id, price, quantity, subtotal, time_stamp) VALUES(%s, %s, %s, %s, %s, %s)"""
    values = (user_id, product_id, price, quantity, subtotal, time)

    # Execute the query using values
    cur.execute(query, values)

    # Commit the changes to the table
    conn.commit()
    logger(__name__).warning("New items had been added to cart, hence closing the connection")
    return jsonify({"message": "New items had been added to cart",
                    "details": extract_key})

