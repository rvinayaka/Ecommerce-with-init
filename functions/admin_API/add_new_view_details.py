import datetime
from flask import Flask, request, jsonify, flash, redirect, url_for
from settings import connection, logger, handle_exceptions

app = Flask(__name__)

"""Admin API"""
@app.route("/app/v1/users/<int:user_id>/recently_viewed/add", methods = ["POST"])
@handle_exceptions
def adding_views_in_recently_viewed_list(user_id):
    # starting the database connection
    cur, conn = connection()
    # log connection details
    logger(__name__).warning("Start the db connection to insert values in recently viewed table")

    # Check if the parameters given in the url is available or not
    if not user_id:
        error_msg = "User id not given"
        raise Exception(error_msg)

    # Define a lambda function to extract values from JSON data
    extract_key = lambda key: request.json.get(key)

    # Insert new values taken from the user using the lambda function
    user_id = extract_key('userId')
    product_id = extract_key('productId')
    reviews_count = extract_key('reviewsCount')
    time = datetime.datetime.now()

    # {
    #     "user_id": 1,
    #     "product_id": 93,
    #     "time": '1993-07-21'
    # }
    cur.execute("SELECT  FROM recently_viewed WHERE user_id =%s", (user_id, ))
    user_already_exists = cur.fetchone()

    if user_already_exists:
        flash(f"User with id {user_id} already exists")
        return redirect(url_for("update_details_of_user_in_recently_viewed", user_id=user_id, product_id=product_id, reviews_count = reviews_count))


    query = """INSERT INTO recently_viewed (user_id, product_id, reviews_count, time_stamp) VALUES(%s, %s, %s, %s)"""
    values = (user_id, product_id, reviews_count, time)

    # Execute the query using values
    cur.execute(query, values)

    # Commit the changes to the table
    conn.commit()
    logger(__name__).warning("Inserting views successful, hence closing the connection")
    return jsonify({"message": "Views has been added",
                    "details": extract_key})
