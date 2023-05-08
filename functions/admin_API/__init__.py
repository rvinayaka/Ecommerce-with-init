from flask import Flask

from add_items_to_wishlist import add_items_to_wishlist
from add_new_items_in_cart import add_new_items_to_order_items_table
from add_new_orders import add_new_order_to_order_table
from add_new_vendor_ratings import add_new_vendor_ratings_of_product
from add_new_vendors import add_new_vendors
from add_new_view_details import adding_views_in_recently_viewed_list

from clear_all_views import clearing_views_of_user
from clear_wishlist import clear_wishlist_of_user
from delete_items_from_cart import deleting_products_from_cart_of_user
from delete_items_from_wishlist import delete_items_of_user_in_wishlist
from delete_vendor_ratings import delete_vendor_details
from deleting_views import deleting_views_of_user

from update_cart import updating_details_in_order_items_table
from update_orders import updating_details_in_order_table
from update_vendor_details import update_vendor_details
from update_views_count import update_details_of_user_in_recently_viewed

app = Flask(__name__)