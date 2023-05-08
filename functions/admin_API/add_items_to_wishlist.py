from flask import Flask, request, jsonify
from settings import connection, logger, handle_exceptions

app = Flask(__name__)

"""Admin API"""
@app.route("/app/v1/wishlist/add", methods = ["POST"])
@handle_exceptions
def add_items_to_wishlist():
    # starting the database connection
    cur, conn = connection()
    # log connection details
    logger(__name__).warning("Start the db connection to insert values in wishlist table")

    # Define a lambda function to extract values from JSON data
    extract_key = lambda key: request.json.get(key)

    # Get values from the user using the lambda function
    user_id = extract_key('userId')
    product_id = extract_key('productId')
    time = extract_key('time')
    # {
    #     "user_id": 1
    #     "product_id": 2
    #     "time": '2021-02-04'
    # }


    query = """INSERT INTO wishlist (user_id, product_id, time) VALUES(%s, %s, %s)"""
    values = (user_id, product_id, time)

    # Execute the query using values
    cur.execute(query, values)

    # Commit the changes to the table
    conn.commit()
    logger(__name__).warning("Inserting value successful, hence closing the connection")
    return jsonify({"message": "New items added to wishlist", "details": extract_key})

