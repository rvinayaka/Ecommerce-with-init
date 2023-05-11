from flask import jsonify
from settings import connection, logger, handle_exceptions
from functions import app

"""Functional API"""
@app.route("/app/v1/vendor_rating/<int:vendor_id>", methods=["GET"], endpoint='get_all_ratings_of_current_vendor_id')
@handle_exceptions
def get_all_ratings_of_current_vendor_id(vendor_id):
    # starting the database connection
    cur, conn = connection()
    # log connection details
    logger(__name__).warning(f"Starting the db connection to get ratings of vendor id. {vendor_id}")

    # Check if the parameters given in the url is available or not
    if not vendor_id:
        error_msg = "vendor id is not available"
        raise Exception(error_msg)

    cur.execute("SELECT ratings, review from vendor_ratings WHERE vendor_id = %s", (vendor_id,))
    get_vendor = cur.fetchone()[0]

    if not get_vendor:
        return jsonify({"message": "Vendor not found"}), 200

    cur.execute("SELECT v.vendor_name, v.vendor_contact, v.address, r.ratings, r.review "
                "FROM vendor_ratings r JOIN vendor v ON r.vendor_id = r.vendor_id;")

    get_details = cur.fetchall()[0]

    name, contact, address, ratings, review = get_details

    data = {
        "name": name,
        "contact": contact,
        "address": address,
        "ratings": ratings,
        "review": review
    }

    # Log the details into logger file
    logger(__name__).info(f"Ratings of vendor with id. {vendor_id} has been showed")

    # close the database connection
    logger(__name__).warning("Hence ratings shown, closing the connection")
    return jsonify({"message": f"Ratings of vendor with id. {vendor_id} has been showed",
                    "details": data}), 200
