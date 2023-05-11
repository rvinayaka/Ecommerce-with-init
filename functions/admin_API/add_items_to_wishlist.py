from _datetime import datetime
from flask import request, jsonify
from settings import connection, logger, handle_exceptions
from functions import app

"""Admin API"""
@app.route("/app/v1/wishlist/add", methods = ["POST"], endpoint="add_items_to_wishlist")
@handle_exceptions
def add_items_to_wishlist():
    # starting the database connection
    cur, conn = connection()
    # log connection details
    logger(__name__).warning("Start the db connection to insert values in wishlist table")
    print("CHECKING SUCCESSFUL API IS RUNNING")

    if "userId" and "productId" not in request.json:
        raise Exception("Data is insufficient")

    # Define a lambda function to extract values from JSON data
    extract_key = lambda key: request.json.get(key)

    # Get values from the user using the lambda function
    user_id = extract_key('userId')
    product_id = extract_key('productId')
    time = datetime.now()
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

