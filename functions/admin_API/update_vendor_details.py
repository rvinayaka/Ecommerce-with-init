from flask import request, jsonify
from settings import connection, logger, handle_exceptions
from functions import app

"""Admin API"""
# to update vendor details
@app.route("/app/v1/vendor/<int:vendor_id>", methods = ["PUT"], endpoint="update_vendor_details")
@handle_exceptions
def update_vendor_details(vendor_id):
    # starting the database connection
    cur, conn = connection()
    # log connection details
    logger(__name__).warning("Start the db connection to update values in vendor table")

    # Check if the parameters given in the url is available or not
    if not vendor_id:
        error_msg = "Vendor id is not available"
        raise Exception(error_msg)

    if "name" and "contact" and "address" not in request.json:
        raise Exception("Data is insufficient")

    # Get values from the user
    data = request.get_json()
    vendor_name = data.get('name')
    contact = data.get('contact')
    address = data.get('address')


    if vendor_name:
        cur.execute("UPDATE vendor SET vendor_name = %s WHERE vendor_id = %s", (vendor_name, vendor_id))
    elif contact:
        cur.execute("UPDATE vendor SET vendor_contact = %s WHERE vendor_id = %s", (contact, vendor_id))
    elif address:
        cur.execute("UPDATE vendor SET address = %s WHERE vendor_id = %s", (address, vendor_id))

    # Commit the changes to the table
    conn.commit()
    logger(__name__).warning("Updating value successful, hence closing the connection")
    return jsonify({"message": "Vendor details updated", "details": data})
