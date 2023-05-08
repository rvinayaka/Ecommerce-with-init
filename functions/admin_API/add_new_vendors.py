from flask import Flask, request, jsonify
from settings import connection, logger, handle_exceptions

app = Flask(__name__)

"""Admin API"""
# to add vendor details
@app.route("/app/v1/vendor", methods = ["POST"], endpoint="add_new_vendors")
@handle_exceptions
def add_new_vendors():
    # starting the database connection
    cur, conn = connection()
    # log connection details
    logger(__name__).warning("Start the db connection to insert values in vendor table")

    # Get values from the user
    data = request.get_json()
    vendor_name = data.get('name')
    contact = data.get('contact')
    address = data.get('address')

    # {
    #     "name": "XYZ Company",
    #     "contact": 90245252,
    #     "address": "402, street, colony"
    # }

    if not all([vendor_name, contact, address]):
        return jsonify({"error": "Given data is insufficient, check all the values properly"})

    query = """INSERT INTO vendor (vendor_name, vendor_contact, address) VALUES(%s, %s, %s)"""
    values = (vendor_name, contact, address)

    # Execute the query using values
    cur.execute(query, values)

    # Commit the changes to the table
    conn.commit()
    logger(__name__).warning("Inserting value successful, hence closing the connection")
    return jsonify({"message": "New vendor added", "details": data})