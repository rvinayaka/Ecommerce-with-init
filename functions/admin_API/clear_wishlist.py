from flask import jsonify
from settings import connection, logger, handle_exceptions
from functions import app

"""Admin API"""
@app.route("/app/v1/wishlist/<int:user_id>/clear", methods = ["DELETE"], endpoint="clear_wishlist_of_user")
@handle_exceptions
def clear_wishlist_of_user(user_id):
    # starting the database connection
    cur, conn = connection()
    # log connection details
    logger(__name__).warning("Start the db connection to deleting all items of user in wishlist table")

    # Check if the parameters given in the url is available or not
    if not user_id:
        error_msg = "User id not given"
        raise Exception(error_msg)

    cur.execute("SELECT * FROM wishlist WHERE user_id = %s", (user_id, ))
    get_user = cur.fetchone()[0]

    if not get_user:
        logger(__name__).warning(f"User with id.{user_id} not found")
        return jsonify({"message": f"User with id.{user_id} not found"})

    cur.execute("DELETE FROM wishlist WHERE user_id = %s")
    logger(__name__).warning(f"Wishlist of user with id. {user_id} has been cleared")
    return jsonify({"message": f"Wishlist of user with id. {user_id} has been cleared",
                    "details": get_user})
