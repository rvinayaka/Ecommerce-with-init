from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'

from functions.user_API import get_order_details_of_user, get_order_details_by_order_id, get_wishlist_items,\
    get_ratings_of_product, get_avg_ratings_of_vendor, get_all_ratings_of_vendor

from functions.admin_API import add_items_to_wishlist, add_new_items_in_cart, add_new_orders, add_new_vendors,\
    add_new_vendor_ratings, add_new_view_details, clear_all_views, clear_wishlist, delete_items_from_cart, \
    delete_items_from_wishlist, delete_vendor_ratings, deleting_views, update_cart, update_orders, \
    update_vendor_details, update_views_count


if __name__ == "__main__":
    app.run(debug=True, port=5000)
