from flask import Flask, request, jsonify
from settings import connection, logger, handle_exceptions

app = Flask(__name__)

"""Admin API"""
# to delete vendor details
@app.route("/app/v1/<int:product_id>/vendor_rating/<int:vendor_id>", methods = ["DELETE"], endpoint="delete_vendor_details")
@handle_exceptions
def delete_vendor_details(product_id, vendor_id):
    # starting the database connection
    cur, conn = connection()

    # log connection details
    logger(__name__).warning("Start the db connection to delete values in vendor ratings table")

    # Check if the parameters given in the url is available or not
    if not (vendor_id and product_id):
        error_msg = "Vendor id and product id is not available"
        raise Exception(error_msg)


    query = "DELETE FROM vendor_ratings WHERE product_id =%s AND vendor_id = %s"
    cur.execute(query, (product_id, vendor_id))

    # Commit the changes to the table
    conn.commit()

    logger(__name__).warning(f"Deleting ratings with vendor id. {vendor_id} of product with id.{product_id}")
    return jsonify({f"Deleting ratings with vendor id. {vendor_id} of product with id.{product_id}"})

