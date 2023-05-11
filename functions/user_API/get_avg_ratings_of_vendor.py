from flask import jsonify
from settings import connection, logger, handle_exceptions
from functions import app

"""Functional API"""
@app.route("/app/v1/vendor_rating/<int:vendor_id>/average", methods=["GET"], endpoint='get_average_ratings_of_current_vendor_id')
@handle_exceptions
def get_average_ratings_of_current_vendor_id(vendor_id):
    # starting the database connection
    cur, conn = connection()
    # log connection details
    logger(__name__).warning(f"Starting the db connection to get average ratings of vendor id. {vendor_id}")

    # Check if the parameters given in the url is available or not
    if not vendor_id:
        error_msg = "vendor id is not available"
        raise Exception(error_msg)


    cur.execute("SELECT COUNT(*) from vendor_ratings WHERE vendor_id = %s", (vendor_id,))
    get_vendor_ratings_count = cur.fetchone()[0]

    if not get_vendor_ratings_count:
        return jsonify({"message": "Vendor not found"}), 200

    # query = """SELECT vendor_ratings.ratings, vendor.vendor_name, vendor.address,
    #                 vendor.vendor_contact FROM vendor_ratings JOIN vendor
    #                 on vendor.vendor_id = vendor_ratings.vendor_id"""

    query = """SELECT SUM(r.ratings) AS average_ratings, 
                v.vendor_name, v.vendor_contact 
                FROM vendor_ratings r JOIN vendor v 
                ON r.vendor_id = v.vendor_id 
                WHERE vendor_id =  %s"""

    cur.execute(query, (vendor_id, ))
    get_sum_ratings = cur.fetchall()[0]


    avg_ratings, name, contact = get_sum_ratings
    get_average = get_sum_ratings / get_vendor_ratings_count
    print("See", get_sum_ratings, get_vendor_ratings_count, get_average)


    data = {
        "average ratings": get_average,
        "vendor name": name,
        "contact info": contact
    }

    # Log the details into logger file
    logger(__name__).info(f"Ratings of vendor with id. {vendor_id} has been showed")

    # close the database connection
    logger(__name__).warning("Hence checkout done, closing the connection")
    return jsonify({"message": f"Average ratings of vendor with id. {vendor_id} are {get_average}",
                    "details": data}), 200
