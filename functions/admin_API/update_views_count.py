import datetime
from flask import Flask, request, jsonify, flash, redirect, url_for
from settings import connection, logger, handle_exceptions

app = Flask(__name__)

"""Admin API"""
@app.route("/app/v1/<int:user_id>/recently_viewed/<int:product_id>/counts", methods = ["PUT"], endpoint="update_details_of_user_in_recently_viewed")
@handle_exceptions
def update_details_of_user_in_recently_viewed(user_id, product_id):
    # starting the database connection
    cur, conn = connection()
    # log connection details
    logger(__name__).warning("Start the db connection to insert values in recently viewed table")

    # Check if the parameters given in the url is available or not
    if not (user_id and product_id):
        error_msg = "User id and product id is not available"
        raise Exception(error_msg)


    # Fetch count of recently viewed products for current user
    cur.execute("SELECT COUNT(*) FROM recently_viewed WHERE user_id = %s", (user_id, ))
    count = cur.fetchone()[0][0]

    if not count:
        return jsonify({"message": "User doesn't exist"})

    # If count is greater than or equal to max, delete oldest record
    if count >= 10:
        cur.execute("SELECT MIN(time_stamp) FROM recently_viewed WHERE user_id = %s", (user_id, ))
        oldest_time = cur.fetchone()[0]
        cur.execute("DELETE FROM recently_viewed WHERE user_id = %s AND time_stamp = %s", (user_id, oldest_time))

    # Define a lambda function to extract values from JSON data
    extract_key = lambda key: request.json.get(key)

    # Insert new values taken from the user using the lambda function
    reviews_count = extract_key('reviewsCount')
    time = datetime.datetime.now()

    query = """UPDATE recently_viewed SET product_id = %s, reviews_count = %s, time_stamp = %s WHERE user_id = %s"""
    values = (product_id, reviews_count, time, user_id)

    # Execute the query using values
    cur.execute(query, values)

    # Commit the changes to the table
    conn.commit()
    logger(__name__).warning("Updating views count successful, hence closing the connection")
    return jsonify({"message": "Views has been updated",
                    "details": extract_key})
