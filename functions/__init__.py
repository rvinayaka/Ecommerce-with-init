from flask import Flask
from admin_API import *
from user_API import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'

# from user_API.get_all_ratings_of_vendor import get_all_ratings_of_current_vendor_id
# from user_API.get_avg_ratings_of_vendor import get_average_ratings_of_current_vendor_id
# from user_API.get_order_details_by_order_id import get_order_details_of_order_id
# from user_API.get_order_details_of_user import get_order_details_of_user
# from user_API.get_ratings_of_product import vendor_ratings_of_current_product
# from user_API.get_wishlist_items import get_items_of_user_in_wishlist
#
# from admin_API.add_items_to_wishlist import add_items_to_wishlist
# from admin_API.add_new_items_in_cart import add_new_items_to_order_items_table
# from admin_API.add_new_orders import add_new_order_to_order_table
# from admin_API.add_new_vendor_ratings import add_new_vendor_ratings_of_product
# from admin_API.add_new_vendors import add_new_vendors
# from admin_API.add_new_view_details import adding_views_in_recently_viewed_list
#
# from admin_API.clear_all_views import clearing_views_of_user
# from admin_API.clear_wishlist import clear_wishlist_of_user
# from admin_API.delete_items_from_cart import deleting_products_from_cart_of_user
# from admin_API.delete_items_from_wishlist import delete_items_of_user_in_wishlist
# from admin_API.delete_vendor_ratings import delete_vendor_details
# from admin_API.deleting_views import deleting_views_of_user
#
# from admin_API.update_cart import updating_details_in_order_items_table
# from admin_API.update_orders import updating_details_in_order_table
# from admin_API.update_vendor_details import update_vendor_details
# from admin_API.update_views_count import update_details_of_user_in_recently_viewed





if __name__ == "__main__":
    app.run(debug=True, port=5000)
