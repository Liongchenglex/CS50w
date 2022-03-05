from django.urls import path

from . import views

app_name = 'auctions'
urlpatterns = [
    path("", views.index, name="index"),
    path("create_listing", views.create_listing, name="create"),
    path("listings/<int:item_id>", views.listings, name='listings'),
    path("delete/<int:item_id>", views.delete, name='delete'),
    path("end_auction/<int:item_id>", views.end_auction, name='end_auction'),
    path("comments/<int:item_id>", views.comments, name='comments'),
    path("category/<str:cat>", views.category, name='category'),

    # wishlist
    path("wishlist/add_to_wishlist/<int:item_id>",views.add_wishlist, name='add_wishlist'),
    path("wishlist/<int:item_id>",views.remove_wishlist, name='remove_wishlist'),
    path("wishlist", views.wishlist, name='wishlist'),

    # login/logout/register
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
