from flask import request, jsonify
from settings import connection, logger, handle_exceptions
from functions import app

"""Admin API"""
@app.route("/app/v1/<int:product_id>/vendor_rating/insert", methods = ["POST"], endpoint="add_new_vendor_ratings_of_product")
@handle_exceptions
def add_new_vendor_ratings_of_product(product_id):
    # starting the database connection
    cur, conn = connection()
    # log connection details
    logger(__name__).warning("Start the db connection to insert values in vendor ratings table")

    # Check if the parameters given in the url is available or not
    if not product_id:
        error_msg = "Product id not given"
        raise Exception(error_msg)

    # Get values from the user
    data = request.get_json()
    vendor_id = data.get('vendorId')
    user_id = data.get('userId')
    ratings = data.get('ratings')
    review = data.get("review")
    time = data.get('time')
    feedback = data.get('feedback')

    # {
    #     "vendorId": 101,
    #     "userId": 20,
    #     "ratings": 3.0,
    #     "review": "Nice work",
    #     "time": "2011-08-29",
    #     "feedback": "Thanks for the feedback"
    # }

    if not all([vendor_id, user_id, ratings, review, time, feedback]):
        # raise Exception("data is insufficient")
        return jsonify({"error": "Given data is insufficient, check all the values properly"})

    query = """INSERT INTO vendor_ratings (vendor_id, user_id, ratings, review, 
                    time, vendor_feedback, product_id) VALUES(%s, %s, %s, %s, %s, %s, %s)"""
    values = (vendor_id, user_id, ratings, review, time, feedback, product_id)

    # Execute the query using values
    cur.execute(query, values)

    # Commit the changes to the table
    conn.commit()
    logger(__name__).warning("Inserting value successful, hence closing the connection")
    return jsonify({"message": "New vendor ratings added", "details": data})
