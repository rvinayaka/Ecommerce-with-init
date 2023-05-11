from flask import jsonify
from settings import connection, logger, handle_exceptions
from functions import app

"""Functional API"""
@app.route("/app/v1/<int:product_id>/vendor_rating/<int:vendor_id>", methods=["GET"], endpoint='vendor_ratings_of_current_product')    # Calculate the total price
@handle_exceptions
def vendor_ratings_of_current_product(product_id, vendor_id):
    # starting the database connection
    cur, conn = connection()
    # log connection details
    logger(__name__).warning("Starting the db connection to get all vendor")

    # Check if the parameters given in the url is available or not
    if not (product_id and vendor_id):
        error_msg = "Product id and vendor id is not available"
        raise Exception(error_msg)


    cur.execute("SELECT * from vendor_ratings WHERE vendor_id = %s", (vendor_id,))
    get_vendor = cur.fetchone()

    if not get_vendor:
        return jsonify({"message": "Vendor not found"}), 200
        # return jsonify({"message": f"Product ratings with vendor id.{vendor_id} not found"}), 200

    # Execute the query
    cur.execute("""SELECT rating_id, ratings, review, vendor_feedback 
                    FROM vendor_ratings JOIN ON products 
                    WHERE product_id = %s AND vendor_id = %s""", (product_id, vendor_id))
    ratings = cur.fetchone()[0]
    id, ratings, review, vendor_feedback = ratings
    data = {
        "id": id,
        "product_id": product_id,
        "vendor_id": vendor_id,
        "ratings": ratings,
        "review": review,
        "vendor_feedback": vendor_feedback
    }
    print("ratings of a product", ratings, data)

    # Log the details into logger file
    logger(__name__).info(f"Ratings of product with id no. {product_id} are {ratings}")

    # close the database connection
    logger(__name__).warning("Hence checkout done, closing the connection")
    return jsonify({"message": f"Ratings of {product_id} are {ratings}",
                    "details": data}), 200
